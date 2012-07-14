# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

#import sys
#sys.path.insert(0, '/home/niwi/devel/sse')


from gevent.pywsgi import WSGIServer
from wsgi import application

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 8888), application)
    server.serve_forever()
