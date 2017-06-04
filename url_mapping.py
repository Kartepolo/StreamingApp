from home import HomeHandler
from tweet import TweetHandler
from input_coord import InputHandler
from tornado.web import url

handlers = [
    url(r"/", HomeHandler, name="index"),
    url(r"/nearby_tweet", TweetHandler, name="nearby"),
    url(r"/input_coord", InputHandler, name="input_coord")
]