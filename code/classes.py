class Lecturer:
    def __init__(self, name, degree, year, unit):
        self.name = name
        self.degree = degree
        self.year = year
        self.unit = unit
    def setKeyword(self, keyword):
        self.keyword = keyword
    def getNumKey(self):
        return len(self.keyword)

class Topic:
    def __init__(self, content, lecturer, keyword):
        self.content = content
        self.lecturer = lecturer
        self.keyword = keyword

class Committee:
    def __init__(self, chair: Lecturer, capacity):
        self.member = []
        self.member.append(chair)
        self.not_in = 0
        self.keyword = chair.keyword
        self.capacity = capacity
    def updateKeyword(self, mem : Lecturer):
        temp = []
        for key in self.keyword:
            same = False
            for word in mem.keyword:
                if( word == key):
                    same = True
                    break
            if(same == False):
                temp.append(key)
        for key in temp:
            self.keyword.remove(key)

    def addMember(self, mem: Lecturer):
        if(mem.unit == 1 or (mem.unit == 0 and self.not_in < 2)):
            self.member.append(mem)
            self.updateKeyword(mem)

        if(mem.unit == 0):
            self.not_in += 1

    def lecturer_heuristic(self, mem: Lecturer, prio : list):
        k = len(prio)
        if(mem.unit == 0 and self.not_in == 2 or len(self.member) == 5):
            return 1
        else:
            result = chung(self.keyword, mem.keyword)
            if(result != 0):
                list_common = list_chung(self.keyword, mem.keyword)
                for kw in list_common:
                    for i in range(k):
                        if(kw == prio[i]):
                            result = result + k - i
            return -result
    
    def topic_heuristic(self, topic: Topic):
        k = chung(self.keyword, topic.keyword)
        for mem in self.member:
            if(mem.name == topic.lecturer and k > 0):
                return -21
            elif(k > 0):
                return -1
        return 0
    def set_chairman(self, lecturer: Lecturer):
        self.chairman = lecturer
    def set_vicechairman(self, lecturer: Lecturer):
        self.vicechairman = lecturer
    def set_secretary(self, lecturer: Lecturer):
        self.secretary = lecturer
    
    def has_mem(self, lecturer):
        for mem in self.member:
            if(mem.name == lecturer):
                return True
        return False  



def chung(a_list: list, b_list: list):
    common = 0
    for a in a_list:
        for b in b_list:
            if (a == b):
                common += 1
    return common

def list_chung(a_list: list, b_list:list):
    common = []
    for a in a_list:
        for b in b_list:
            if(a == b):
                common.append(a)
    return common

def sub_chair_heu(sub: Lecturer, chair: Lecturer, prio: list):
    k = len(prio)
    result = chung(sub.keyword, chair.keyword)
    if(result != 0):
        list_common = list_chung(sub.keyword, chair.keyword)
        for kw in list_common:
            for i in range(k):
                if(kw == prio[i]):
                    result = result + k - i

    return result

def lec_topic_h(lecturer: Lecturer, topic: Topic):
    common = chung(lecturer.keyword, topic.keyword)
    if(common == 0):
        return 0
    else:
        return -1