from flask import Flask

app = Flask(__name__)
import routes.square
import routes.trivia
import routes.blanks
import routes.spy
import routes.ticketing_agent
import routes.safeguard
# import routes.princess