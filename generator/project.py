import jsonpickle
import os
import string
import random
import getopt
import sys
from model.project import Project

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/projects.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_prefix(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def random_value(enum):
    return random.choice([e.value for e in enum])


testdata = \
    [Project(
        name=random_prefix("name", 10)
        , status=random.choice([e.name for e in Project.Status])
        , view_state=random.choice([e.name for e in Project.ViewState])
        , description=random_prefix("description", 100)
        , inherit_global=random.choice([True, False]))
        for i in range(n)]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)
with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))
