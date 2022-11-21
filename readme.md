ngrok http 5000 

add link to your agent

 
$env:FLASK_APP = main.py
flask run

docker build -t flow-actions .
docker run -it -p 5000:5000 flow-actions
