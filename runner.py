# coding=utf-8

import os, sys

import concurrent.futures
import tornado.ioloop
import tornado.web

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from config import config
from url_mapping import handlers
from .Handler.tornadis_session import SessionManager
# configs for tornado server
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
)

def db_poll_init():
    engine_config = config['database']['engine_url']
    engine = create_engine(engine_config, **config['database']["engine_setting"])
    config['database']['engine'] = engine
    db_poll = sessionmaker(bind=engine)
    return db_poll


class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **settings)
        self.session_manager = SessionManager(config['redis_session'])
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(config['max_threads_num'])
        self.db_pool = db_poll_init()
        self.pubsub_manager = None

def parse_command_line():
    pass


if __name__ == '__main__':
    parse_command_line()
    application = Application()
    application.listen(config['port'])
    loop = tornado.ioloop.IOLoop.current()
    loop.start()