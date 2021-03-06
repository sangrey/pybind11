#!/usr/bin/env python
from __future__ import print_function
import sys
sys.path.append('.')

from example.issues import print_cchar, print_char
from example.issues import DispatchIssue, dispatch_issue_go
from example.issues import Placeholder, return_vec_of_reference_wrapper
from example.issues import iterator_passthrough
from example.issues import ElementList, ElementA, print_element
from example.issues import expect_float, expect_int
from example.issues import A, call_f
from example.issues import StrIssue
from example.issues import NestA, NestB, NestC, print_NestA, print_NestB, print_NestC
import gc

print_cchar("const char *")
print_char('c')


class PyClass1(DispatchIssue):
    def dispatch(self):
        print("Yay..")


class PyClass2(DispatchIssue):
    def dispatch(self):
        try:
            super(PyClass2, self).dispatch()
        except Exception as e:
            print("Failed as expected: " + str(e))
        p = PyClass1()
        dispatch_issue_go(p)

b = PyClass2()
dispatch_issue_go(b)

print(return_vec_of_reference_wrapper(Placeholder(4)))

print(list(iterator_passthrough(iter([3, 5, 7, 9, 11, 13, 15]))))

el = ElementList()
for i in range(10):
    el.add(ElementA(i))
gc.collect()
for i, v in enumerate(el.get()):
    print("%i==%i, " % (i, v.value()), end='')
print()

try:
    print_element(None)
except Exception as e:
    print("Failed as expected: " + str(e))

try:
    print(expect_int(5.2))
except Exception as e:
    print("Failed as expected: " + str(e))

print(expect_float(12))

class B(A):
    def __init__(self):
        super(B, self).__init__()

    def f(self):
        print("In python f()")

print("C++ version")
a = A()
call_f(a)

print("Python version")
b = B()
call_f(b)

print(StrIssue(3))
try:
    print(StrIssue("no", "such", "constructor"))
except TypeError as e:
    print("Failed as expected: " + str(e))

a = NestA()
b = NestB()
c = NestC()
a += 10
b.a += 100
c.b.a += 1000
b -= 1
c.b -= 3
c *= 7
print_NestA(a)
print_NestA(b.a)
print_NestA(c.b.a)
print_NestB(b)
print_NestB(c.b)
print_NestC(c)
abase = a.as_base()
print(abase.value)
a.as_base().value += 44
print(abase.value)
print(c.b.a.as_base().value)
c.b.a.as_base().value += 44
print(c.b.a.as_base().value)
del c
gc.collect()
del a # Should't delete while abase is still alive
gc.collect()
print(abase.value)
del abase
gc.collect()
