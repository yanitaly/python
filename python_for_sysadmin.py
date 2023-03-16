#!/usr/bin/env python3.6 
### ACG online training: Python 3 Scripting for System Administrators

## chapter7: using std lib 

#!/usr/bin/env python3.6 
from time import localtime, strftime, mktime

starttime = localtime()
print(f"Timer started at {strftime('%X', starttime)}")
input("Press 'Enter' to stop timer ")
stoptime = localtime()
print(f"Timer stopped at {strftime('%X', starttime)}")
difference = mktime(stoptime) - mktime(starttime)
print(f"Total time: {difference} seconds")

## Others 
# loop through yaml nested data
# disks = ['disk%d' % i for i in range(yaml_file['parent_key']['a_key'])]
# for t_disk in disks:
  