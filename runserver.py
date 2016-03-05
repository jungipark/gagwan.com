# -*- coding: utf-8 -*-
__author__ = 'Jun'


import sys
import os
from app import create_app

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app('default')

if __name__ == '__main__':
    print "server start"

    app.run(debug=True)