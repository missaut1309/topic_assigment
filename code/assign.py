import sys
import numpy as np
import scipy.optimize
from classes import *


def assign(committee_list, topic_list):
    sum_capacity = 0
    for c in committee_list:
        sum_capacity += c.capacity
    if(len(topic_list) > sum_capacity):
        print("Number of topic is greater than the max number of topic that committees can be assigned")
        sys.exit()
    asm = []
    for i in range(len(committee_list)):
        asm.append([])
    
    not_assign_list = []
    for i in range(len(topic_list)):
        assigned = False
        for j in range(len(committee_list)):
            if(committee_list[j].has_mem(topic_list[i].lecturer) and chung(committee_list[j].keyword,topic_list[i].keyword) != 0 and committee_list[j].capacity > 0):
                asm[j].append(topic_list[i])
                committee_list[j].capacity -= 1
                assigned = True
                break
        if(assigned == False):
            not_assign_list.append(topic_list[i])
    
    if(len(not_assign_list) > 0):
               
        assign_1(committee_list, not_assign_list,asm)
    
    return asm, not_assign_list

def assign_1(committeeList,not_assigned_list ,assignment):
    numberOfTopic = len(not_assigned_list)
    numberOfCommittee = len(committeeList)
   
    for i in range(numberOfCommittee - 1):
        swapped = False
        for j in range(0, numberOfCommittee - i - 1):
            if(committeeList[j].capacity < committeeList[j+1].capacity):
                temp = committeeList[j]
                temp_asm = assignment[j]
                committeeList[j] = committeeList[j+1]
                assignment[j] = assignment[j+1]
                committeeList[j+1]= temp
                assignment[j+1] = temp_asm
                swapped = True
        if(swapped == False):
            break
    
       
    H = np.zeros((numberOfTopic, numberOfCommittee), dtype=int)

    for i in range(numberOfTopic):
        for j in range(numberOfCommittee):
            H[i,j] = committeeList[j].topic_heuristic(not_assigned_list[i])

    committeeMap = []
    t = 0
    capacities = []
    for c in committeeList:
        capacities.append(c.capacity)
    for i in range(numberOfTopic):
        while(capacities[t % numberOfCommittee] == 0):
            t += 1
        committeeMap.append(t % numberOfCommittee)
        capacities[t % numberOfCommittee] -= 1
        t += 1
    C = np.zeros((numberOfTopic, numberOfTopic), dtype=int)

    for i_topic in range(numberOfTopic):
        for i_committee in range(numberOfTopic):
            C[i_topic,i_committee] = H[i_topic, committeeMap[i_committee]]

    row_ind, col_ind = scipy.optimize.linear_sum_assignment(C)
    assigned = []
    for r, c in zip(row_ind, col_ind):
        committee_ind = committeeMap[c]
        a = H[r][committee_ind]
        if(a != 0):
            assignment[committee_ind].append(not_assigned_list[r])
            committeeList[committee_ind].capacity -= 1
        else:
            for i in range(numberOfCommittee):
                if(H[r,i] != 0):
                    if(committeeList[i].capacity > 0):
                        assignment[i].append(not_assigned_list[r])
                        committeeList[i].capacity -= 1                    
                    else:
                        for tp in assignment[i]:
                            if(committeeList[committee_ind].topic_heuristic(tp) < 0):
                                assignment[i].append(not_assigned_list[r])
                                committeeList[i].capacity -= 1
                                assignment[committee_ind].append(tp)
                                committeeList[committee_ind].capacity -= 1
                                assignment[i].remove(tp)
                                committeeList[i].capacity += 1
                                break    

        assigned.append(not_assigned_list[r])
    for tp in assigned:
        not_assigned_list.remove(tp)   

def reviewer_assign(lecturer_list, topic_list):
    H = np.zeros((len(lecturer_list), len(topic_list)), dtype= int)
    for i in range(len(lecturer_list)):
        for j in range(len(topic_list)):
            H[i,j] = lec_topic_h(lecturer_list[i], topic_list[j])
    reviewer_asm = []
    row_ind, col_ind = scipy.optimize.linear_sum_assignment(H)
    for r, c in zip(row_ind, col_ind):
        reviewer_asm.append((topic_list[c], lecturer_list[r]))

    return reviewer_asm
