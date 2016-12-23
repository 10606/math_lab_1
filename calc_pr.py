from declaration import *

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

INF = 10**10
def zfunc(s, t):
    '''
    find t in s with start min balans
    return posinion ans min balans
    '''
    s = s[::-1]
    t = t[::-1]
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
        ind = len(s)-i-1
        if (z[i] == tLen):
            if (min_ > balans[ind - tLen + 1]):
                min_ = balans[ind - tLen + 1]
                pos = ind - tLen + 1
    return [min_, pos]


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
    #print("parser ", a, b)
    global s
    temp = s[a : b + 1]
    if (check(temp)):
        #print("number")
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

            #print("response ", index_l, arg_1_end, arg_2_begin, index_r)
            #print("part")
            #print("argument 1:", s[index_l : arg_1_end + 1])
            #print("argument 2:", s[arg_2_begin : index_r + 1])

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

    #print("get pr on segment ", a, b)
    #print("string = ", s[a : b+ 1])
    ans = ""
    a_ = 1
    while (a_):
        a_ = 0
        resp = parser(a, b)
        if (resp.index_f == -1):
            return ans
        i = resp.index_f
        #print("index operator", i)
        #print("typ operator", tabl_pr[i].typ)
        s_ = s[0:resp.index_s0] + s[resp.index_s1:]

        for result_ in tabl_pr[i].result:
            #print("result", result_)
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
    #s = s.replace("arctg", "arg")
    #s = s.replace("arcsin", "arcin")
    #s = s.replace("ctg", "cg")
    s = unar_minus(s)
    out = get(0, len(s) - 1)
    out = out.replace('^', '**')
    #out = out.replace("arg", "arctg")
    #out = out.replace("arcin", "arcsin")
    #out = out.replace("cg", "ctg")
    #s__ = unar_minus(s)
    #testout.write(out + "\n" + s + "\n")
    testout.write(out + "\n")
    #print(out)
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
