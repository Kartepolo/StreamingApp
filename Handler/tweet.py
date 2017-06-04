from base import BaseHandler





class TweetHandler(BaseHandler):


    def get(self):
        self.render("index.html", messages=global_message_buffer.cache)