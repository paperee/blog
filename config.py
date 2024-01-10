# config.py

bind="127.0.0.1:1234"
workers=3
daemon=True
backlog=2048
worker_connections=1000
pidfile="logs/gunicorn.pid"
accesslog="logs/access.log"
errorlog="logs/gunicorn.log"