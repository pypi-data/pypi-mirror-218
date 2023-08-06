"""Types used in artbot
"""


class Price:
  """Price record

  Price of certain cryptocurrency at certain time.
  """

  def __init__(
    self,
    timestamp: int,
    price: int,
    order_currency: str = "BTC",
    payment_currency: str = "KRW",
  ):
    self.timestamp = timestamp
    self.price = price
    self.order_currency = order_currency
    self.payment_currency = payment_currency


class Trading:
  """Trading record

  Record of a certain trading.
  """

  def __init__(
    self,
    timestamp: int,
    exchange: str,
    price: int,
    quantity: float,
    order_currency: str = "BTC",
    payment_currency: str = "KRW",
  ):
    self.timestamp = timestamp
    self.exchange = exchange
    self.price = price
    self.quantity = quantity
    self.order_currency = order_currency
    self.payment_currency = payment_currency
