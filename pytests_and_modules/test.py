import pytest, os, sys, requests, json, re
from modules import calculations as calc

#pytest test methods (called by pytest) have a name that is prefixed by "test_"
#methods without this prefix are internal to this test file

#an explanation of mocking with examples for mocking out slow/remote functions can be found here: https://changhsinlee.com/pytest-mock/

####### HELPER METHODS #####################
def HTTPGET(url): #called by functions below
    response = None
    err = None
    try:
        response = requests.get(url)
    except requests.exceptions.Timeout:
        err = "HTTPGET: timeout reached: {}".format(url)
    except requests.exceptions.TooManyRedirects: 
        err = "HTTPGET: too many redirects: {}".format(url)
    except requests.exceptions.RequestException as e:
        err = "HTTPGET: unable to connect: {}".format(url)
    return err, response

def HTTPPOST(url,data,headers): #called by functions below
    response = None
    err = None
    try:
        response = requests.post(url, data=data, headers=headers)
    except requests.exceptions.Timeout:
        err = "HTTPPOST: timeout reached: {}".format(url)
    except requests.exceptions.TooManyRedirects: 
        err = "HTTPPOST: too many redirects: {}".format(url)
    except requests.exceptions.RequestException as e:
        err = "HTTPPOST: unable to connect: {}".format(url)
    return err, response

########## TESTS #############
def test_installation():
    errors = []
    #check that myapp.py exists
    if not os.path.exists("myapp.py"):
        errors.append("myapp.py not found")
    #check that the runtime is Python3
    if not sys.version_info[0] == 3:
        errors.append("The Python runtime version must be v3")

    #assert that errors list is empty
    #if errors is not empty, print out the list of errors as a string.
    assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

#test that pertinent API calls work
def test_GET_TODOAPI(): #test an arbitrary HTTP GET 
    url = "http://jsonplaceholder.typicode.com/todos"
    err,response = HTTPGET(url)
    assert not err, "Error: {}\n".format(err)
    assert not response or response.ok

def test_GET_BACKENDAPI_HEROKU():
    url = "https://cjk-flask-backend.herokuapp.com/api/getmsg/?msg=Bob"
    err,response = HTTPGET(url)
    assert not err, "Error: {}\n".format(err)
    assert not response or response.ok

def test_GET_BACKENDAPI_LOCAL():
    PORT = os.getenv("PORT")
    url = "http://localhost:{}/api/getmsg/?msg=Bob".format(PORT)
    err,response = HTTPGET(url)
    assert not err, "Error: {}\n".format(err)
    assert not response or response.ok

def test_POST_BACKENDAPI_HEROKU():
    val1 = "cjk1"
    val2 = "cjk2"
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "acckey": val1,
        "seckey": val2
    }
    url = 'https://cjk-flask-backend.herokuapp.com/api/keys'
    err,response = HTTPPOST(url, json.dumps(data), headers)
    assert not err, "Error: {}\n".format(err)
    if response:
        assert "Content-Type" in response.headers and response.headers["Content-Type"] == mimetype
        assert "MESSAGE" in response.json()
        if "MESSAGE" in response.json():
            respstr = response.json()['MESSAGE']
            assert re.search(r"(.*){} and {}(.*)".format(val1,val2), respstr)
        assert not response or response.ok

def test_POST_BACKENDAPI_LOCAL():
    PORT = os.getenv("PORT")
    url = "http://localhost:{}/api/keys".format(PORT)
    val1 = "cjk3"
    val2 = "cjk4"
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "acckey": val1,
        "seckey": val2
    }
    err,response = HTTPPOST(url, json.dumps(data), headers)
    assert not err, "Error: {}\n".format(err)
    if response:
        assert "Content-Type" in response.headers and response.headers["Content-Type"] == mimetype
        assert "MESSAGE" in response.json()
        if "MESSAGE" in response.json():
            respstr = response.json()['MESSAGE']
            assert re.search(r"(.*){} and {}(.*)".format(val1,val2), respstr)
        assert not response or response.ok

#test methods in your modules
def test_multiply():
    input = [2, 10, 4, 7]
    result = calc.multiply(input)
    assert(result == 560)

def test_multiply_badinput():
    with pytest.raises(NameError, match=r".* not defined"):
        input = [2, 10, a, 1]
        result = calc.multiply(input)

def test_sum():
    input = [2, 2, 4, 0, -1]
    result = calc.summation(input)
    assert(result == 7)

def test_print(capsys): #capsys is a pytest fixture that captures stdout and stderror
    op = "sum"
    res = 7
    calc.print_result(op,res)
    out, err = capsys.readouterr()
    assert(out == "Your {} operation result = {}\n".format(op,res))

