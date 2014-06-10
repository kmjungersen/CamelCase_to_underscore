__author__ = 'kurtisjungersen'

import re

def convert(var_name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', var_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

print 'Please enter phrase you would like to convert from\n'
print 'CamelCase to_underscores! '
var_name = raw_input()