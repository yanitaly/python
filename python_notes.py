# loop through yaml nested data
disks = ['disk%d' % i for i in range(yaml_file['parent_key']['a_key'])]
for t_disk in disks:
