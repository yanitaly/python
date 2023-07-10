#!/usr/bin/env 

# week23.27 ====================================

# 1. Python Basics ===================

# py interpreter 
# help(something) or # dir(someClass) returns details of a class

# basic data types: int, float, bool, none, 
print('lower_To_Upper_Case'.upper())
# name and variable (variable has type, name doesn't)
a = 'aString'
print("aString has type: ", type(a))
b = 20
print("20 has type: ", type(b))

# py collects garbage automatically, no need to manage memory explictly 
var1 = 3 
var2 = var1 
var1 = 4
print("var1 = ", var1, " and var2 = ", var2)

# careful about overwriting, e.g. str = 'bla' str
print('20 has type: ', type(20), ', str(20) has type: ', type(str(20)))

# List: methods: create, modify, indicing, slicing, 
myList = [1, 2]
myList.append("Third")
del myList[1]
print(myList)

cute_animals = ['cat', 'dog', 'panda', 'raccon', 'elephant', 'gorilla']
print(cute_animals[::-1])  # revert list
print(cute_animals[::2])    # skip every other item

# Everything (List) in py is an object
# names points objects, some objects are unique, others not
list1 = [1,2,3]
list2 = [1,2,3]
print(type(list1))
print(list1 is list2) # False, two names point to two different obj that have same value. 
print(list1 == list2) # True

list3 = list1 
print(list3 is list1) # True, two names points to a unique obj
print(list3 == list1) # True

# mutable inside imutable 
mytuple = ([1,2,3],[4,5,6],[7,8,9])
mytuple[1][1] = 'changed' # this is ok, but changing mytuple[1] is not OK 
print(mytuple)

# swap can be done directly 
x, y = 0, 1
x, y = y, x # unlike in c/c++ that a temp is needed
print(x, y)

# if, for, switch/case, while
name = 'Bro'
fromWho = 'Ning'
print("Hello, {}! -- {}".format(name, fromWho))  # f string

#### Exercise1: fitler event nr and sort list
def filter_even_sort(alist):
    '''
    for anum in alist[:]:  # alist[:] creates a copy of list. Otherwise looping and removing at the same time is problematic
        if anum % 2:
            alist.remove(anum)
    alist.sort() 
    return alist  # modifies original list
    '''
    return sorted( num for num in alist if not num%2)  #  modify a copy, keep original list unchanged.

alist = [1,-20, -19, 66, 88, 5,5,2,3,4,4]
print(filter_even_sort(alist))
print(alist)

# sort() vs sorted
print(sorted(alist))  # [1, -20, -19, 66, 88, 5, 5, 2, 3, 4, 4], sorted creates a new copy of the list and modifies it
print(alist) # [1,-20, -19, 66, 88, 5,5,2,3,4,4]

alist.sort()  # sort changes on the original list
print(alist) # [1, -20, -19, 66, 88, 5, 5, 2, 3, 4, 4]

# list comprehensions 
lista = [2, 3, 4]
listb = [n*2 for n in lista]  # [4,6,8]

# sets: unique, not ordered, can operate with union/intersection/diff etc
seta = {1,2,3}
setb = {3,4,5}
setc = seta & setb # {3}

# dictionary
adict = {
    "france":"paris",
    "china":"beijing"
}
print(adict.get("france"))  # paris
for country, capital in adict.items():
    print(country, capital)

#### Exercise 2: calculate dinner for two 
def calculate_dinner(order):
    total = 0
    for item in my_order:
        # total += PRICE_LIST[item]
        total += PRICE_LIST.get(item, 0) # if not defined, give 0
    return total 
PRICE_LIST = {
    'steak':5,
    'banana':0.5,
    'brown rice': 2,
    'green salad': 1
}
my_order = ('steak', 'brown rice', 'banana', 'banana', 'noodles')
print(calculate_dinner(my_order))  # 8.0

#  more on func
def power(a, b=2):
    return a ** b
print(power(5)) # 25

# default arguments, variable length arg, named/keywords args. 
def varfunc(some_arg, *args, **kwargs): 
    print("some_arg: ", some_arg, '\n', "*args: ", args,'\n' ,"kwargs: ", kwargs)
varfunc('hello', 1,2,3, name='Bob', age=22) # hello (1, 2, 3) {'name': 'Bob', 'age': 22}
# some_arg = 'hello'
# *args = 1,2,3
# **kwargs = {'name':'Bob', 'age':12 }

# OOP 
# everything in python are objects. 
import math 
class Vector2:
    def __init__(self, x,y):
        self.x = x 
        self.y = y 
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
spam = Vector2(3,4) 
print (spam.x)
print (spam.length())

# python private variable are not that "private", it is more indicative than strict not-modifiable
class Vector:
    def __init__(self, x,y,z, __secret_coord = None):
        self.x = x 
        self.y = y 
        self.z = z 
        self.__secret_coord = __secret_coord 
    def _coords(self):
        return[coord for coord in (self.x, self.y, self.z, self.__secret_coord)]
    def length(self):
        return sum(coord**2 for coord in self._coords()) ** 0.5
spam = Vector(1.0,2.0,5.0,6.0) 
print (spam._coords()) # [1.0, 2.0, 5.0, 6.0]
print (spam.length())

print(dir(spam)) 
spam._Vector__secret_coord = 3.0 # this changes the private val 
print (spam._coords()) # [1.0, 2.0, 5.0, 3.0]

# inheritance 
class Person():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    def name(self):
        return self.first_name, self.last_name 
a_european = Person('John','Anderson') 
print(a_european.name())

class Chinese(Person): # inherit Person class
    def name(self): # overwrites name from parent
        return self.last_name, self.first_name
a_chinese = Chinese('Bruce','Li') 
print(a_chinese.name())

# Exceptions
# try / except / else / finally 
try: 
    alist = [1,2,3]
    alist[4]
except (IOError, OSError) as err:
    print("Couldn't read from file: ", err)
except Exception as err:
        print("Something else went wrong: ", err)
else:
    print("This is else")
finally:
    print("This is finally")

# user defined exception
# Duck typing 

# 2. Testing:
# Unit test & test driven development
#  write test first, then code
# three phases: red > green > refactor 
# setup > execute > verify > teardown 

class ShoppingAssistant():
    def __init__(self, starting_balance):
        self.__balance = starting_balance 
    def increase_balance(self, amount):
        self.__balance += amount
assistant = ShoppingAssistant(100) # initial balance 
assistant.increase_balance(50)
print(assistant._ShoppingAssistant__balance) # class name is needed, as balance is private

import unittest 
class TestShoppingAssistant(unittest.TestCase):
    INITIAL_BALANCE = 100
    def setUp(self):
        self.sa = ShoppingAssistant(self.INITIAL_BALANCE)
    def tearDown(self):
        del self.sa 
    def test_increase_balance(self): # name needs to start with "test_xxx"
        self.sa.increase_balance(50)
        cur_bal = self.sa._ShoppingAssistant__balance
        self.assertEqual(cur_bal, self.INITIAL_BALANCE + 50)
if __name__ == '__main__':
    unittest.main()
# output:
# ----------------------------------------------------------------------
# Ran 1 test in 0.001s
#
