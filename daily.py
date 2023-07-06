#!/usr/bin/env python3.6 
### ACG online training: Python 3 Scripting for System Administrators
### 17.03.2023 

## Others changes TBD ============================
# loop through yaml nested data
# disks = ['disk%d' % i for i in range(yaml_file['parent_key']['a_key'])]
# for t_disk in disks 

print("Hello world")


# week23.27 ====================================

# default arguments, variable length arg, keywords args. 
def varfunc(some_arg, *args, **kwargs) # 
    {
        # blabla
    }
varfunc('hello', 1,2,3, name='Bob', age=22) 
# some_arg = 'hello'
# *args = 1,2,3
# **kwargs = {'name':'Bob', 'age':12 }
