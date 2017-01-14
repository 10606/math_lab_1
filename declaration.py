import math
import sys
from collections import deque

s = ""

class format:
    '''
    typ #string * sin sqrt
    size_arg_l
    size_arg_r
    arg0 = [] #list args before
    arg1 = [] #list args after

    result = [] #list <string> or "$index" with pr (@index without)
    '''
    typ = ""
    templ = ""
    result = []
    size_arg_l = 0
    size_arg_r = 0
    arg0 = []
    arg1 = []
    def __init__(typ_ = "", templ_ = "", size_arg_l_ = 0, size_arg_r_ = 0):
        typ = typ_
        templ = templ_
        result = [0]
        size_arg_l = size_arg_l_
        size_arg_r = size_arg_r_
        arg0 = []
        arg1 = []

class response_:
    '''
    arg_l = [] #list indexex begin
    arg_r = [] #list indexes end

    index_f #index type of funcliun
    index_s0 #index in s
    index_s1 #index in s
    '''
    index_f = 0
    index_s0 = 0
    index_s1 = 0
    arg_l = []
    arg_r = []
    def __init__(self, index_f_ = 0, index_s0_ = 0, index_s1_ = 0):
        index_f = index_f_
        index_s0 = index_s0_
        index_s1 = index_s1_
        arg_l = []
        arg_r = []

tabl_pr = []
char_map = set()


def cout ():
    '''
    cout tabl_pr
    '''
    for i in tabl_pr:
        print(i.typ, i.templ, i.size_arg_l, i.size_arg_r)
        for j in i.result:
            print(j, end = '')
        print("\n")


def pre_parser(a, b, c, sq, ss):
    '''
    parsing of tabl_pr
    '''
    gg = format()
    gg.typ = a;
    gg.result = ss;
    gg.size_arg_l = b;
    gg.size_arg_r = c;
    gg.templ = sq;
    char_map.add(a[0])
    tabl_pr.append(gg)

'''
read tabl_pr.txt
'''
sys.stdin = open("table_pr.txt", "r")
for i in sys.stdin:
    z = i.split()
    a = z[0]
    b = int(z[1])
    c = int(z[2])
    s = z[3]
    ss = z[4:]
    if (c == ""):
        continue
    pre_parser(a, b, c, s, ss)

tabl_pr.append(format())
tabl_pr[len(tabl_pr)-1].result.append("0")


def check(a):
    '''
    check a is number
    ( (9,.9 ) is number
    '''
    for j in range(len(a)):
        i = a[j]
        #if (i != '(' and i != ')' and i != '.' and (i > '9' or i < '0') and i != '\n' and i != ' ' and i != '.' and i != ','):
        if (i == 'x'):
            return 0
    return 1

'''
change str on unar minus
-x -> (0-x)
signed down before char on unar_minus.txt
'''
unar_ = open("unar_minus.txt", "r")
char_unar = set()
for i in unar_:
    char_unar.add(i[0])

def unar_minus(s_):
    stack = deque()
    i = 0
    bal_ = 0
    while (i < len(s_)):

        if (s_[i] == '-' and (i == 0 or s_[i - 1] == '(' or s_[i - 1] in char_unar or s_[i - 1] == '^')):
            s_ = s_[:i] + '(0' + s_[i:]
            i += 3
            bal_ += 1
            stack.append(bal_)

        elif (s_[i] ==')' or s_[i] in char_unar):
            while (len(stack) != 0):
                _temp = stack.pop()
                #print("unar ", s_[i], _temp, bal_)

                if (_temp == bal_):
                    s_ = s_[:i] + ')' + s_[i:]
                    bal_ -= 1
                    i += 1
                else:
                    stack.append(_temp)
                    break
        if (s_[i] == '('):
            bal_ += 1
        if (s_[i] == ')'):
            bal_ -= 1
        i += 1
    while (len(stack) > 0):
        s_ += ')'
        stack.pop()
    return s_
