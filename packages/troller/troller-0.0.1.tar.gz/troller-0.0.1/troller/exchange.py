"""Cryptocurrency exchanges

Provides features like trading, fetching price, etc.
"""
import time
from abc import ABCMeta, abstractmethod

import requests

from .type import Price

from .type import Price, Trading


class Exchange(metaclass=ABCMeta):
  """Cryptocurrency exchange base class

  Provides features for trading cryptocurrency.

  This class is a abstract class and need to be implemented.

  Need keys to use the exchange API.
  """
  NAME = "abstract"


  def __init__(self, access_key: str, secret_key: str):
    self.access_key = access_key
    self.secret_key = secret_key


  @abstractmethod
  def fetch_price(self, order_currency: str, payment_currency: str) -> Price:
    """Fetch price from the exchange API

    Returns Price object.

    Raises ConnectionError when failed to fetch price from the API.
    """
    raise NotImplementedError


  @abstractmethod
  def buy_all(self, order_currency: str, payment_currency: str) -> Trading:
    """Buy maximum amount at the exchange

    Returns Trading object.

    Raises ConnectionError when failed to buy.
    """
    raise NotImplementedError


  @abstractmethod
  def sell_all(self, order_currency: str, payment_currency: str) -> Trading:
    """Sell maximum amount at the exchange

    Returns Trading object.

    Raises ConnectionError when failed to sell.
    """
    raise NotImplementedError


  @abstractmethod
  def fetch_estimated_balance(self) -> float:
    """Fetch balance and return estimated value in KR

    Fetch all assets from exchange and calculated estimated value in KRW.

    Raises ConnectionError when failed to fetch assets.
    """
    raise NotImplementedError


class SimExchange(Exchange):
  """Exchange for simulation

  SimExchange does not communicate with the API when buying or selling. This
  class is only for testing purpose.

  This class is abstract class and need to be implemented.
  """
  NAME = "abstract"


  def __init__(self, access_key: str, secret_key: str, fee: float=0.0005):
    super().__init__(access_key, secret_key)
    self.fee = fee
    self.cash = 1_000_000.0
    self.coin = 0.0


  def buy_all(self, order_currency: str, payment_currency: str) -> Trading:
    price = self.fetch_price(order_currency, payment_currency).price
    quantity = self.cash / price * (1 / (1 + self.fee))

    self.coin += quantity
    self.cash = 0

    return Trading(
      timestamp=int(time.time()),
      trader=self.NAME,
      price=price,
      quantity=quantity,
      order_currency=payment_currency,
      payment_currency=order_currency,
    )


  def sell_all(self, order_currency: str, payment_currency: str) -> Trading:
    price = self.fetch_price(order_currency, payment_currency).price
    quantity = self.coin * price * (1 - self.fee)

    self.cash += quantity
    self.coin = 0

    return Trading(
      timestamp=int(time.time()),
      trader=self.NAME,
      price=price,
      quantity=quantity,
      order_currency=payment_currency,
      payment_currency=order_currency,
    )


  def fetch_estimated_balance(self) -> float:
    """Fetch balance and return estimated value in KRW

    Fetch all assets from exchange and calculated estimated value in KRW.
    In SimExchange we assume that coin property has value of Bitcoin.

    Raises ConnectionError when failed to fetch assets.
    """
    price = self.fetch_price("BTC", "KRW").price
    return self.cash + self.coin * price


class Bithumb(Exchange):
  """Bithumb

  Provides features for trading cryptocurrency using Bithumb.
  """
  NAME = "Bithumb"


  def __init__(self, access_key: str, secret_key: str):
    super().__init__(access_key, secret_key)


  def fetch_price(self, order_currency: str, payment_currency: str) -> Price:
    try:
      headers = {"accept": "application/json"}
      response = requests.get(
        f"https://api.bithumb.com/public/ticker/{order_currency}_{payment_currency}",
        headers=headers,
        timeout=1,
      )
      data = response.json()["data"]
      timestamp = int(data["date"])
      price = int(data["closing_price"])
    except:
      raise ConnectionError
    return Price(timestamp, price, order_currency, payment_currency)


class Upbit(Exchange):
  """Upbit

  Provides features for trading cryptocurrency using Upbit.
  """
  NAME = "Upbit"


  def __init__(self, access_key: str, secret_key: str):
    super().__init__(access_key, secret_key)


  def fetch_price(self, order_currency: str, payment_currency: str) -> Price:
    try:
      headers = {"accept": "application/json"}
      response = requests.get(
        f"https://api.upbit.com/v1/ticker?markets={payment_currency}-{order_currency}",
        headers=headers,
        timeout=1,
      )
      data = response.json()[0]
      timestamp = int(data["timestamp"])
      price = int(data["trade_price"])
    except:
      raise ConnectionError
    return Price(timestamp, price, order_currency, payment_currency)


class SimBithumb(SimExchange, Bithumb):
  """Bithumb exchange for simulation

  Run simulation based on bithumb price data
  """
  def __init__(self, access_key: str, secret_key: str):
    SimExchange.__init__(self, access_key, secret_key, fee=0.001)


class SimUpbit(SimExchange, Upbit):
  """Upbit exchange for simulation

  Run simulation based on upbit price data
  """
  def __init__(self, access_key: str, secret_key: str):
    SimExchange.__init__(self, access_key, secret_key, fee=0.0005)
