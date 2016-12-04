import math
import sys
from collections import deque

qq = open("input.txt", "r")
s = qq.readline()
n = len(s)

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

balans = []
def psp (l, r):
    '''
    create list balance on segment [l r]
    '''
    global balans
    global n
    balans = []
    global s
    temp = 0
    ans = 1e9
    for i in range(l, r + 1):

        if (s[i] == ')'):
            temp -= 1
        elif (s[i] in char_map):
            ans = min(ans, temp)
        balans.append(temp)
        if (s[i] == '('):
            temp += 1
    return ans

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

INF = 10**10
def zfunc(s, t):
    '''
    find t in s with start min balans
    return posinion ans min balans
    '''
    splust = t + '#' + s
    tLen = len(t)
    s = splust
    z = [0] * len(s)
    x, _len = 0, 0
    pos = -1
    min_ = INF # мин вхождение balans
    for i in range(1, len(s)):
        if i < x + _len:
            z[i] = min(z[i - x], x + _len - i)
        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] = z[i] + 1
        if i + z[i] > x + _len:
            x = i
            _len = z[i]
        if (z[i] == tLen):
            if (min_ > balans[i - tLen - 1]):
                min_ = balans[i - tLen - 1]
                pos = i - tLen - 1
    return [min_, pos]

def check(a):
    '''
    check a is number
    ( (99 ) is number
    '''
    for j in range(len(a)):
        i = a[j]
        if (i != '(' and i != ')' and i != '.' and (i > '9' or i < '0') and i != '\n' and i != ' '):
            return 0
    return 1

splitt = [0, 0]

def spliten(a, b, min_):
    '''
    a - left iter of string
    b - right iter of string
    min_ - min balans in operator posiniot
    return 2 iter with correct permut "(" ")"
    '''
    index_l = 0
    index_r = 0
    j = a
    i = 0
    while (i < len(balans) and balans[i] < min_):
        i += 1
        j += 1
    index_l = j
    j = b
    i = b - a
    while (i >= 0 and balans[i] < min_):
        i -= 1
        j -= 1
    index_r = j
    splitt[0] = index_l
    splitt[1] = index_r
    return

def parser(a, b):
    '''
    a - left iter of string
    b - right iter of string
    slit str on part of ( ) and operator in table_pr.txt
    return class <response>
        1 or 2 arg and code operator
    '''
    if (a > b):
        answer = response_(-1, -1, -1)
        answer.index_f = -1
        answer.index_l = -1
        answer.index_r = -1
        answer.arg_l = []
        answer.arg_r = []

        return answer
    print("parser ", a, b)
    global s
    temp = s[a : b + 1]
    if (check(temp)):
        print("number")
        if (s[a] == '(' and s[b] != ')'):
            a += 1
        answer = response_(-1, -1, -1)
        answer.index_f = len(tabl_pr) - 1
        answer.index_l = a
        answer.index_r = b
        answer.arg_l = []
        answer.arg_r = []

        return answer
    min_ = psp(a, b)
    ans = [INF] * len(tabl_pr)
    pos = [INF] * len(tabl_pr)
    j = -1
    for i in tabl_pr:
        j += 1
        if (j == len(tabl_pr) - 1):
            break
        resp = zfunc(temp, i.typ)
        resp[1] += a
        if resp[1] == -1:
            continue
        if (ans[j] > resp[0]):
            ans[j] = resp[0]
            pos[j] = resp[1]
    spliten(a, b, min_)
    index_l = splitt[0]
    index_r = splitt[1]
    for i in range(len(ans) - 1):
        if (ans[i] == min_):
            answer = response_(i, index_l, index_r)
            answer.index_f = i
            answer.index_l = index_l
            answer.index_r = index_r
            answer.arg_l = []
            answer.arg_r = []

            arg_1_end = pos[i] - 1
            arg_2_begin = pos[i] + len(tabl_pr[i].typ)

            print("response ", index_l, arg_1_end, arg_2_begin, index_r)
            print("part")
            print("argument 1:", s[index_l : arg_1_end + 1])
            print("argument 2:", s[arg_2_begin : index_r + 1])

            if (tabl_pr[i].size_arg_l != 0):
                if ((index_l != arg_1_end) or ((s[arg_1_end] != ')') and (s[arg_1_end] != '('))):
                    if (index_l <= arg_1_end):
                        answer.arg_l.append(index_l)
                        answer.arg_r.append(arg_1_end)

            if (tabl_pr[i].size_arg_r != 0):
                if ((index_r != arg_2_begin) or ((s[index_r] != ')') and (s[index_r] != '('))):
                    if (arg_2_begin <= index_r):
                        answer.arg_l.append(arg_2_begin)
                        answer.arg_r.append(index_r)
            return answer
    answer = response_(-1, -1, -1)
    answer.index_f = -1
    answer.index_l = -1
    answer.index_r = -1
    answer.arg_l = []
    answer.arg_r = []
    return answer


def get(a, b):
    '''
    a - left iter of string
    b - right iter of string
    return string result of differ
    on table_pr.txt rules
    get code operator from rarser
    '''
    global s

    print("get pr on segment ", a, b)
    print("string = ", s[a : b+ 1])
    ans = ""
    a_ = 1
    while (a_):
        a_ = 0
        resp = parser(a, b)
        if (resp.index_f == -1):
            return ans
        i = resp.index_f
        print("index operator", i)
        print("typ operator", tabl_pr[i].typ)
        s_ = s[0:resp.index_s0] + s[resp.index_s1:]

        for result_ in tabl_pr[i].result:
            print("result", result_)
            if (result_[0] == '$'):
                temp = (int)(result_[1:])
                temp -= 1
                ans += get(resp.arg_l[temp], resp.arg_r[temp])
            elif (result_[0] == '@'):
                temp = (int)(result_[1:])
                temp -= 1
                ans += s[resp.arg_l[temp]:resp.arg_r[temp] + 1]
            else:
                ans += result_
    return ans


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

        if (s_[i] == '-' and (i == 0 or s_[i - 1] == '(' or s_[i] in char_unar)):
            s_ = s_[:i] + '(0' + s_[i:]
            i += 3
            bal_ += 1
            stack.append(bal_)

        elif (s_[i] ==')' or s_[i] in char_unar):
            while (len(stack) != 0):
                _temp = stack.pop()
                print("unar ", s_[i], _temp, bal_)

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


'''
main function
read from input.txt
write in output.txt
'''
testout = open("output.txt", "w")
testin = open("input.txt", "r")
for i in testin:
    s = i
    if (s[len(s) - 1] == '\n'):
        s = s[:len(s) - 1]
    s = s.replace("**", "^")
    s = unar_minus(s)
    out = get(0, len(s) - 1)
    out = out.replace('^', '**')
    #s__ = unar_minus(s)
    #testout.write(out + "\n" + s + "\n")
    testout.write(out + "\n")
    print(out)
'''
s = "(-(-123*-x+x**-3)**x)/-sin(-tg(-x))"
s = s.replace("**", "^")
s = unar_minus(s)
out = get(0, len(s) - 1)
out = out.replace('^', '**')
print(out)
print(s)
s = "-(-(-123*-x+-x**-3)**x)/-sin(-tg(-x))"
s = s.replace("**", "^")
s_ = unar_minus(s)
print(s)
print(s_)

#(0-((0-((0-123)*(0-x)+(0-x)^(0-3)))^x))/(0-sin((0-tg((0-x)))))
'''
