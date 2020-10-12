import os
from subprocess import Popen, PIPE, STDOUT
from src import calculations as calc

def test_installation():
    result = os.system("CS148 --help")
    assert(result == 0)


def test_welcome():
    p = Popen(["CS148", "welcome"], shell = True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out, err = (p.communicate(input=b'Shereen'))
    result = out.decode()
    assert(result.find("Hello Shereen"))

# Test the whole flow
def test_calculations():
    p = Popen(["CS148", "calculate", "--operation=sum", "1 2 3 4 5"], shell = True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out, err = p.communicate()
    result = out.decode()
    assert(result.find("Your sum operation result = 15"))

# Test specific method
def test_sum():
    input = [2, 2, 4, 0, -1]
    result = calc.summation(input)
    assert(result == 7)
