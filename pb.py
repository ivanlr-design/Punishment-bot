import re

compiler = re.compile(r"[0-9][0-9]/[0-9][0-9]/[0-9][0-9] [0-6][0-9]:[0-6][0-9]")
string = "12/02/24 40:32"

if re.match(compiler, string):
    print("dawd")