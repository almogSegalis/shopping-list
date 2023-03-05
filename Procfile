release: python shopping/manage.py migrate
web: sh -c 'cd ./shopping  && exec gunicorn shopping.wsgi'
