import numpy as np
import sys, csv

from classes import *
from group import *
from assign import *

with open(sys.argv[1]) as gvfile:
    gv_rows = list(csv.reader(gvfile))

num_lecturer = int(gv_rows[0][0])
num_committee = int(gv_rows[0][1])
max_number_of_topic = int(gv_rows[0][2])
people = gv_rows[1:]

lecturer_list = []
for i in range(num_lecturer):
    a = Lecturer(people[2 * i][0], int(people[2 * i][1]), int(people[2 * i][2]), int(people[2 * i][3]))
    kw_list = people[2 * i + 1]
    for j in range(len(kw_list)):
        kw_list[j] = int(kw_list[j])
    a.setKeyword(kw_list)
    lecturer_list.append(a)

with open(sys.argv[2]) as dtfile:
    dt_rows = list(csv.reader(dtfile))

topic_list = []

for topic in dt_rows:
    tp_kw = topic[2:]
    topic_kw = []
    for k in tp_kw:
        topic_kw.append(int(k))
    a = Topic(topic[0],topic[1], topic_kw)
    topic_list.append(a)

prio = []
find_prio(topic_list,prio)

committee_list, lecList = make_committee(lecturer_list, prio, num_committee, max_number_of_topic)
choose_mem(lecList,committee_list,prio)

check_cmt, can_not_assign = check_committee(committee_list, topic_list)

while(check_cmt == False):
    prio_1 = []
    find_prio(can_not_assign, prio_1)
    prio_2 = []
    find_prio(topic_list, prio_2)
    for i in range(int(len(prio_2)/2)):
        prio_2.pop(-1)
    prio_1 = prio_1 + prio_2
    committee_list, lecList = make_committee(lecturer_list, prio_1, num_committee, max_number_of_topic)
    choose_mem(lecList, committee_list, prio_1)
    check_cmt, can_not_assign = check_committee(committee_list, topic_list)

for c in committee_list:
    c.set_chairman(c.member[0])
    c.set_vicechairman(c.member[1])
    for i in range(2,5):
        if(c.member[i].unit == 1):
            c.set_secretary(c.member[i])
            break

print("Committee list:")
for c in committee_list:
    for mem in c.member:
        print(mem.name)
    print(c.keyword)
    print(c.not_in)
    print("-------")

asm, not_asm = assign(committee_list, topic_list)
print("%d topics are not assigned" %(len(not_asm)))
print("Topic assign")
for i in range(num_committee):
    print( "chairman is: %s" %(committee_list[i].member[0].name))
    for tp in asm[i]:
        print(tp.content)
    print("___")

reviewer_asm = reviewer_assign(lecturer_list, topic_list)
print("Reviewer assign:")
for pair in reviewer_asm:
    print("%s, %s" %(pair[0].content, pair[1].name))