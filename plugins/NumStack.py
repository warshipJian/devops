#!/usr/bin/env python
#coding:utf8

def checkStr(str):
    left = ['(','{','[']
    right = {')':'(','}':'{',']':'['}
    stack = []

    try:
        for i in str:
            if i in left:
                stack.append(i)
            if i in right and stack[-1] == right[i]:
                stack.pop()
    except IndexError:
        return False

    return stack == []

#print(checkStr('[fdsfdsf((fsdfsd{})fdsfds)]'))

def qmdj(arr):
    """
    outputArr = arr.pop(0)
    while True:
        arr = list(zip(*arr))
        if len(arr) <= 0:
            break
        outputArr.extend(arr.pop(-1))
        arr.reverse()
    print(outputArr)
    """
    outPutArr = []
    while arr:
        outPutArr.extend(arr.pop(0))
        arr = list(zip(*arr))
        arr.reverse()
    print(outPutArr)

def rgbToHex(r,g,b):
    return "{:02X} {:02X} {:02X}".format(r,g,b)

print(rgbToHex(255,244,233))

