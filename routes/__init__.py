from flask import Flask

app = Flask(__name__)
# app.config["JSON_SORT_KEYS"] = False
import routes.square
import routes.trivia
import routes.blanks
import routes.spy
import routes.ticketing_agent
import routes.safeguard
# import routes.princess
import routes.trading_formula
import routes.archive
import mage