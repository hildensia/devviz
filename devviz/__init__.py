__author__ = 'johannes'

from flask import Flask
from .session_handler import RedisSessionInterface

app = Flask(__name__)

app.session_interface = RedisSessionInterface()
app.secret_key = 'qwedxcyujnfr6yhbnm0sa7rt9;p74ty[989'
app.config['SERVER_NAME'] = "localhost:5000"
app.views = {}

from .data_handling import DataHandler
data_handler = DataHandler()

from .app import *
from .views import *


