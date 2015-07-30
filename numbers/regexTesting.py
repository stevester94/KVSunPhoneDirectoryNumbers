#reg ex testing 

import re

regex = r"[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"
compiledReg = re.compile(regex)

print compiledReg.search("Youngman, Richard   4608 Lake Isabella Blvd #11, Lk Isbl	379-6364")