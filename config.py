# -*- coding:utf-8 -*-

import os

SECRET_KEY = "ot]4H]9t.4<IHS5_tIU<Z]Zoont59t9t"

if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = os.path.join(basedir, 'database.db')
else:
    DATABASE_URI = os.environ['DATABASE_URL']