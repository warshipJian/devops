#!/usr/bin/env python
#coding:utf8


def test(fc):
    print(fc())

@test
def abc():
    return 'abc'

def dobi(jack):
    return jack()

@dobi
def qinfeng():
    print('dobi')

def func(s):
    count = 10
    def inner_func(age):
        nonlocal count
        count += 1;
        print('age:', count)
    return inner_func

bb = func('the5fire')
bb(12)

def hello1(hello):
    def bao1():
        return '<b>' + hello() + '<b>'
    return bao1

def hello2(hello):
    def bao2():
        return '<i>' + hello() + '<i>'
    return bao2

@hello1
@hello2
def hello():
    return 'hi'

print(hello())
