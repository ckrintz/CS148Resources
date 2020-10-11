# CS148Resources

## backend
This is a sample Python3 Flask app with a simple GET and POST (with CORS setup).  
### One Time Setup
First create a virtual environment in a folder called env and install the packages.
```
cd backend
python3 -m venv env
source env/bin/activate
python -V
python3 -m pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

### Run
Activate the virtual environment if it is not already activated (ie there is no *(env)* in your prompt.
```
cd backend
source env/bin/activate
```

The default PORT that the development server uses is 8118 but you can change this by setting your PORT environment variable.
```
export PORT=8118
cd backend
python myapp.py
```
### Test
Test that it works via
```
curl http://localhost:8118/api/getmsg/?msg=Bob

curl -H "Content-Type: application/json" -X POST -d '{"acckey":"xxx", "seckey":"yyy"}' http://localhost:8118/api/keys/
```
