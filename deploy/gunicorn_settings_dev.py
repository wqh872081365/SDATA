import multiprocessing

bind = "127.0.0.1:8324"
backlog = 2048
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 1000
raw_env = []
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s %(p)s'
accesslog = '/home/wqh/wangqihui/work/wangqihui.me/wangqihui/SDATA_LOG/gunicorn/sdata_gunicorn_access.log'
loglevel = "info"