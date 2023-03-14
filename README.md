

Steps to execute:
-----
1. source ./env/bin/activate  
1.Starts the Flask application server python app.py 
2. to retreive all logs curl -X GET "http://127.0.0.1:5000/api/v1/logs"
3. To retreive  log file curl -X GET "http://127.0.0.1:5000/api/v1/log?filename=keybagd3.log&n=20" 
