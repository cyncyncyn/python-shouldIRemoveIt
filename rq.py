import requests
import sys
from bs4 import BeautifulSoup


filename = sys.argv[1]
print filename

programs_file = open(filename)
programs = programs_file.readlines()
programs_file.close()


programs = [program.rstrip('\n') for program in programs]

should_remove = []
not_found = []
more_than_one_program = []
for program in programs:
    result = requests.get("http://www.shouldiremoveit.com/programs.aspx?q=%s" % program)
    soup = BeautifulSoup(result.content)
    found = soup.find_all(name="div", attrs="programbartxt_keep")
    if found:
        if len(found) > 1:
            more_than_one_program.append(program)
        else:
            percentage = found.text.split("% remove")[0]
            if float(percentage) > 80:
                should_remove.append(program)
    else:
            not_found.append(program)


print "you should remove: %s" % str(should_remove).strip("[]")
print "These programs were not found: %s" % str(not_found).strip("[]")
print "These names match with more than one program: %s" % str(more_than_one_program).strip("[]")
