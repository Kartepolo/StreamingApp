# coding=utf-8

import sys, os


import tornado.ioloop
from tornado.options import options
import concurrent.futures
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# configs for tornado server
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
    default_handler_class=BaseHandler,
)