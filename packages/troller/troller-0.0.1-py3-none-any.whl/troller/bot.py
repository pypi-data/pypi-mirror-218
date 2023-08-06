"""Trading bots

This module contains bots doing algorithm trading.
"""
import statistics

from . import exchange
from .type import Price, Trading


class RisklessArbitrage:
  """Riskless arbitrage trading bot

  Alice and bob is the Exchange object to trade.
  """
  def __init__(
      self,
      alice: exchange.Exchange,
      bob: exchange.Exchange,
      order_currency: str,
      payment_currency: str,
      quantiles: int=200,
      threshold: float=0.003,
      length: int=86400,
  ):
    self.alice = alice
    self.bob = bob
    self.order_currency = order_currency
    self.payment_currency = payment_currency
    self._quantiles = quantiles
    self._threshold = threshold
    self._length = length

    self._price_record: list[tuple[Price, Price]] = []
    self._trading_record: list[Trading] = []
    self._diff_increasing = None


  def fetch_prices(self) -> tuple[Price, Price]:
    """Fetch price of target cryptocurrency in both exchange

    Return tuple of price object in (alice, bob) order.

    Raises Connection Error when failed to fetch prices from the API
    """
    alice = self.alice.fetch_price(self.order_currency, self.payment_currency)
    bob = self.bob.fetch_price(self.order_currency, self.payment_currency)
    return (alice, bob)


  def record_prices(self, prices: tuple[Price, Price]):
    """Add new record to price record

    If the length of the price record exceed predefined length, the first record
    would be removed.
    """
    self._price_record.append(prices)
    if len(self._price_record) > self._length:
      self._price_record.pop(0)


  def run(self):
    """Do arbitrage

    Even if some error occurs during trading, no error will be raised.
    """
    try:
      prices = self.fetch_prices()
      self.record_prices(prices)
    except ConnectionError:
      # TODO: Need to log something
      return

    if self.is_right_time_to_trade():
      self.trade()


  def trade(self):
    """Trade

    Check which exchange is more expensive compared to normal, sell at the more
    expensive one and buy at the other.
    """
    if self.get_latest_price_ratio() > self.calculate_mean_price_ratio():
      expensive, inexpensive = self.alice, self.bob
    else:
      expensive, inexpensive = self.bob, self.alice

    try:
      self._trading_record.append(
        expensive.sell_all(self.order_currency, self.payment_currency)
      )
      self._trading_record.append(
        inexpensive.buy_all(self.order_currency, self.payment_currency)
      )
    except ConnectionError:
      return


  def get_latest_price_ratio(self) -> float:
    """Get latest price ratio

    Returns (alice / bob) of the latest price record
    """
    alice = self._price_record[-1][0]
    bob = self._price_record[-1][1]
    return alice.price / bob.price


  def calculate_mean_price_ratio(self) -> float:
    """Calculate mean of price ratio

    Returns mean of (alice / bob) of all price record.
    """
    return statistics.mean(map(
      lambda prices: prices[0].price / prices[1].price,
      self._price_record,
    ))


  def is_right_time_to_trade(self) -> bool:
    """Check whether to trade or not

    It will return False when there are not enough price records (less than 2).

    All calculation is based on the latest price ratio recorded. You need to
    call fetch_prices and record_prices to reflect latest price data on the
    calculation. 
    """
    try:
      quantiles = self.calculate_quantiles()
    except statistics.StatisticsError:
      return False

    if quantiles[-1] - quantiles[0] < self._threshold:
      return False

    ratio = self.get_latest_price_ratio()
    return not quantiles[0] < ratio < quantiles[-1]

  
  def calculate_quantiles(self) -> list[float]:
    """Calculate quantiles
    
    Returns quantile list

    Raises statistics.StatisticsError when there are not enough price records.
    """
    return statistics.quantiles(
      map(
        lambda prices: prices[0].price / prices[1].price,
        self._price_record,
      ),
      n=self._quantiles,
    )
