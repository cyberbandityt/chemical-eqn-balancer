"""
chemical equation balancer by Alabs(https://www.instagram.com/aealabs/)
"""
import re
from itertools import combinations_with_replacement as cwr, combinations as com, permutations as per
import copy

lhs_init = str(input("left hand side of the equation:\n")).split('+')
rhs_init = str(input("right hand side of the equation:\n")).split('+')

def el_sub_ret(hs_init):
    '''
    returns a dictionary that assigns unit to elements and no. of molecules (unit = 1 side of the + sign)
    '''
    el_sub_hs = dict() # returning dictionary
    tot_els = list() #all the elements present in the side
    for i in range(len(hs_init)):
        el_sub = dict()
        j = hs_init[i] # assign elements to no. of molecules
        if '(' not in j:
            sub = re.findall(re.compile("([A-Z][a-z]?)([0-9]*)"), j)
            for k in sub:
                if k[1].isdigit():
                    el_sub[k[0]] = int(k[1])
                else:
                    el_sub[k[0]] = 1 #if no number is given, no. of molecules = 1
        else:
            sub = re.findall(re.compile(r"([A-Z][a-z]?)([0-9]*)"), j[j.index('('):j.index(')')])#
            o_b_sub = re.findall(re.compile("([A-Z][a-z]?)([0-9]*)"), j[j.index(')'):]+j[:j.index('(')])
            whole_sub = [int(l) for l in re.findall(re.compile(r"([0-9]*)"), j[j.index(')'):]) if l != ''][0]#whole subscript
            for k in sub:
                if k[1].isdigit():
                    el_sub[k[0]] = int(k[1]) * whole_sub#the no. of molecules gets times by whole subscript if parentheses are present
                else:
                    el_sub[k[0]] = whole_sub #if no number, whole sub is the no. of molecules
            for k in o_b_sub:
                if k[1].isdigit():
                    el_sub[k[0]] = int(k[1])
                else:
                    el_sub[k[0]] = 1 #if no number, no. of molecules = 1
        el_sub_hs[i] = el_sub
    return el_sub_hs

def total_d(el, tot_els):
    '''returns a dictionary that assigns elment to total no. of molecules'''
    total = dict()
    for k in tot_els: # loop through all elements
        count = 0
        for j in el:
            el_s = el[j].copy()
            for key in el_s: # loop through the current element(s) and its value(s)
                val = el_s[key]
                if k == key: # if the element is equal to the element inside this unit
                    count += val # add its no. of molecules to count
        total[k] = count
    return total

def new_el_sub(hs, s):
    '''returns a new dictionary after multiplying each unit of hs by element of s'''
    ret = copy.deepcopy(hs)
    for i in ret:
        for j in ret[i]:
            ret[i][j] = ret[i][j] * s[i]
    return ret

def convert_str(hs_init, s):
    '''converts to the string version of hs to be output'''
    new_hs_init = ""
    for i in range(len(hs_init)):
      if s[i] == 1:
        new_hs_init += hs_init[i].strip().rstrip()
      else:
        new_hs_init += str(s[i]) + hs_init[i].strip().rstrip()
      if i+1 != len(hs_init):
            new_hs_init += "+"
    return new_hs_init

lhs = el_sub_ret(lhs_init)
rhs = el_sub_ret(rhs_init)

# we need tuples having lists of all possible len(respect side) combinations of 1 to 15 for each side
_ = com(range(1, 16), len(lhs))
combo_l = tuple(j for i in _ for j in per(i)) + tuple(cwr(range(1, 16),len(lhs)))
_ = com(range(1, 16), len(rhs))
combo_r = tuple(j for i in _ for j in per(i)) + tuple(cwr(range(1, 16),len(rhs)))

#all elements present in our equation:
tot = tuple(set([j for i in lhs_init for j in re.findall(re.compile(r'[A-Z][a-z]?'), i)]))

# now, we'll loop over the combinations in such a way that we'll multiply number of molecules for each unit
# by respective element of the current combination list if the total number of molecules on each side of the
# eqn are equal, and total molecules for each element are equal
# then we know that the current combos are the correct combos to balance the eqn
coeff = list()
for r in combo_r:
    for l in combo_l:
        if len(coeff) >= 2:
            break
        el_sub_l = new_el_sub(lhs, l)
        el_sub_r = new_el_sub(rhs, r)
        total_n_l, total_n_r = total_d(el_sub_l, tot), total_d(el_sub_r, tot)
        if total_n_l == total_n_r:
            coeff.append(l)
            coeff.append(r)

#to output our balanced equation:
if len(coeff) >= 2:
    print("\n THE BALANCED EQUATION IS:\n")
    print("{}\t-->\t{}".format(convert_str(lhs_init, coeff[0]), convert_str(rhs_init, coeff[1])))
else:
    print("couldn't find the balanced equation")