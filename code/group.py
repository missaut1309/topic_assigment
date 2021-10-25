import sys
from classes import *
import numpy as np
import scipy.optimize


def make_committee(lecturerList : list, prioKeyword, numberOfCommittee, max_topic):
    if(len(lecturerList) < numberOfCommittee * 5):
        print("Number of lecturer is not enough to make %d committees" %(numberOfCommittee))
        sys.exit()
    lecList = lecturerList.copy()
    canBeChair = []
    for mem in lecList:
        if((mem.degree == 1 or (mem.degree == 2 and mem.year >= 3)) and mem.unit == 1):
            canBeChair.append(mem)
    canBeSub = canBeChair.copy()
    for mem in lecList:
        if((mem.degree == 1 or (mem.degree == 2 and mem.year >= 3)) and mem.unit != 1):
            canBeSub.append(mem)
    

    H = np.zeros((len(canBeSub), len(canBeChair)), dtype=int)
    
    for i in range(len(canBeSub)):
        for j in range(len(canBeChair)):
            if(i <= j):
                H[i,j] = 0
            else:
                H[i,j] = sub_chair_heu(canBeSub[i], canBeChair[j], prioKeyword)
    
    
    temp = []
    while(len(temp) < numberOfCommittee):
        i_max = 0
        j_max = 0

        for i in range(len(canBeSub)):
            for j in range(len(canBeChair)):
                if(H[i,j] >= H[i_max,j_max]):
                    i_max = i
                    j_max = j
        
        if(H[i_max,j_max]> 0):
            temp.append((i_max,j_max, H[i_max,j_max]))
     
        if(i_max < len(canBeChair)):
            for k in range(len(canBeChair)):
                H[i_max, k] = 0
                H[j_max, k] = 0
            for k in range(len(canBeSub)):
                H[k,i_max] = 0
                H[k, j_max] = 0
        else:
            for k in range(len(canBeChair)):
                H[j_max, k] = 0
                H[i_max,k] = 0
            for k in range(len(canBeSub)):
                H[k, j_max] = 0
        

    committeeList =[]   
    for i in range(numberOfCommittee):
        committeeList.append(Committee(canBeChair[temp[i][1]], max_topic))
        lecList.remove(canBeChair[temp[i][1]])
        committeeList[i].addMember(canBeSub[temp[i][0]])
        lecList.remove(canBeSub[temp[i][0]])
    return committeeList, lecList

def choose_mem(lectureList, committeeList, prio):
    if(len(lectureList) <= 0):
        return

    C = np.zeros((len(lectureList), len(committeeList)), dtype=int)
    for i in range(len(lectureList)):
        for j in range(len(committeeList)):
            C[i,j] = committeeList[j].lecturer_heuristic(lectureList[i], prio)
    
    row_ind, col_ind = scipy.optimize.linear_sum_assignment(C)
    temp = []

    for r,c in zip(row_ind, col_ind):
        if(C[r,c] >= 0):
            r_max = 0
            for i in range(len(committeeList)):
                if(committeeList[i].lecturer_heuristic(lectureList[r], prio) > committeeList[r_max].lecturer_heuristic(lectureList[r],prio)):
                    r_max = i
            committeeList[r_max].addMember(lectureList[r])

        else:
            committeeList[c].addMember(lectureList[r])
        temp.append(lectureList[r])

    for t in temp:
        lectureList.remove(t)
    prio.pop(0)

    choose_mem(lectureList, committeeList,prio)

def kw_popularity(topic_list: list, num_keyword : int):    
    A = []
    for i in range(num_keyword):
        A.append(0)
    for topic in topic_list:
        for i in topic.keyword:
            A[i] += 1
    return A
def find_max(N : list):
    max_f = 0
    for i in range(21):
        if(N[i] > N[max_f]):
            max_f = i
    return max_f
def topic_refine(topic_list : list, max_f):
    temp = []
    for topic in topic_list:
        has_max_f = False
        for kw in topic.keyword:
            if(kw == max_f):
                has_max_f = True
        if(has_max_f == False):
            temp.append(topic)
    return temp

def find_prio(topic_list, result:list):
    N = kw_popularity(topic_list,21)
    if(sum(N) > 0):
        max_f = find_max(N)
        temp = topic_refine(topic_list, max_f)
        result.append(max_f)
        find_prio(temp, result)
    else:
        return

def check_committee(committee_list, topic_list):
    check_list = []
    can_not_assign = []
    for topic in topic_list:
        check = False
        for c in committee_list:
            if(chung(topic.keyword, c.keyword) != 0):
                check = True
                break
        if(check == False):
            can_not_assign.append(topic)
        check_list.append(check)
    for c in check_list:
        if(c == False):
            return False, can_not_assign
    return True, can_not_assign
    