# coding=utf-8
import hashlib
import urllib

import datetime
import tornado.web as tw
from tornado import gen
from tornado.escape import url_escape


class BaseHandler(tw.RequestHandler):
    '''
    Implementation of a base handler of all elements
    '''

    @property
    def db(self):
        if not self.db_session:
            self.db_session = self.application.db_pool()
        return self.db_session

    @property
    def pub_sub_manager(self):
        return self.application.pub_sub_manager

    def initialize(self):
        self.session = None
        self.db_session = None
        self.thread_executor = self.application.thread_executor
        self.cache_manager = self.application.cache_manager
        self.async_do = self.thread_executor.submit


    @gen.coroutine
    def on_finish(self):
        pass
