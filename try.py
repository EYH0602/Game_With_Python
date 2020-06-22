import re
text = "1abc 2abc 3aac 4cca 5abc 6aabc ccaaac bacaac"
res = re.sub("a[bc]", "*", text)
print(text)
print(res)

