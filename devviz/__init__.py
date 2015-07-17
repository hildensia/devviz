__author__ = 'johannes'

from flask import Flask
import redis

app = Flask(__name__)

redis_store = redis.StrictRedis(decode_responses=True)
redis_store.flushdb()

from .app import *
