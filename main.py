import logging
import os

import datetime

from flask import Flask, render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from orderbook import BtcdeOrderBook as bok

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Chart(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  open_at = db.Column(db.DateTime())
  trading_pair = db.Column(db.String(255))
  currency = db.Numeric(precision=10, scale=2)
  open = db.Column(currency)
  close = db.Column(currency)
  high = db.Column(currency)
  low = db.Column(currency)
  min_buy_price = db.Column(currency)
  max_sell_price = db.Column(currency)

  def __init__(self, trading_pair, open_at, open=None, close=None, high=None, low=None, min_buy_price=None, max_sell_price=None):
    self.open_at = open_at
    self.trading_pair = trading_pair
    self.open = open
    self.close = close
    self.high = high
    self.low = low
    self.min_buy_price = min_buy_price
    self.max_sell_price = max_sell_price

@app.route('/task/track_btcde')
def track_btcde():
  orderbook = bok(os.environ['BTCDE_API_KEY'], os.environ['BTCDE_API_SECRET'])
  btceur = orderbook.current(trading_pair='btceur', amount=0.2)

  entry = Chart(
      open_at=datetime.datetime.utcnow(),
      trading_pair='btceur',
      open=btceur['min_buy_price'],
      min_buy_price=btceur['min_buy_price'],
      max_sell_price=btceur['max_sell_price']
  )
  db.session.add(entry)
  db.session.commit()

  etheur = orderbook.current(trading_pair='etheur', amount=2)

  entry = Chart(
      open_at=datetime.datetime.utcnow(),
      trading_pair='etheur',
      open=etheur['min_buy_price'],
      min_buy_price=etheur['min_buy_price'],
      max_sell_price=etheur['max_sell_price']
  )
  db.session.add(entry)
  db.session.commit()

  bcheur = orderbook.current(trading_pair='bcheur', amount=2)

  entry = Chart(
      open_at=datetime.datetime.utcnow(),
      trading_pair='bcheur',
      open=bcheur['min_buy_price'],
      min_buy_price=bcheur['min_buy_price'],
      max_sell_price=bcheur['max_sell_price']
  )
  db.session.add(entry)
  db.session.commit()

  entry = Chart(
      open_at=datetime.datetime.utcnow(),
      trading_pair= 'btceur',
      open=btceur['min_buy_price'],
      min_buy_price=btceur['min_buy_price'],
      max_sell_price=btceur['max_sell_price']
  )
  db.session.add(entry)
  db.session.commit()

  return jsonify({'btceur': btceur, 'etheur': etheur, 'bcheur': bcheur})

@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.', 500


if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5000, debug=True)
