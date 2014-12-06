lis = ["find_path.py",
       "game.py",
       "interface.py",
       "main.py",
       "map_display.py",
       "message_box.py",
       "units\\unit_base.py",
       "units\\ammunition.py"]
lines = 0
for e in lis:
    lines += len(open(e).readlines())
print "Total Lines:", lines

no_of_ifs = 0
for e in lis:
    no_of_ifs += sum([q.count("if") for q in open(e).readlines()])

print no_of_ifs

import time
time.sleep(23)

