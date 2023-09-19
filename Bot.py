##
## EPITECH PROJECT, 2023
## trade-repo
## File description:
## Bot
##

from BotState import BotState
from Chart import Chart
from Candle import Candle
from math import sqrt

class Bot:
    def __init__(self):
        self.botState = BotState()

    def run(self):
        while True:
            reading = input()
            if len(reading) == 0:
                continue
            self.parse(reading)

    def parse(self, info: str):
        tmp = info.split(" ")
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            action = self.make_decision()
            print(action, flush=True)

    def make_decision(self):
        dollars = self.botState.stacks["USDT"]
        current_closing_price = self.botState.charts["USDT_BTC"].closes[-1]
        affordable = dollars / current_closing_price

        if dollars < 100:
            return "no_moves"
        elif affordable > 0.5:
            return f"sell USDT_BTC {0.5 * affordable}"
        else:
            # Calculate Bollinger Bands
            prices = self.botState.charts["USDT_BTC"].closes
            n = len(prices)
            window = min(n, self.botState.bollingerWindow)
            if window < 2:
                return "no_moves"

            sma = sum(prices[-window:]) / window
            squared_diffs = [(price - sma) ** 2 for price in prices[-window:]]
            std_dev = (sum(squared_diffs) / window) ** 0.5

            upper_band = sma + self.botState.bollingerFactor * std_dev
            lower_band = sma - self.botState.bollingerFactor * std_dev

            # Calculate EMA
            ema_period = min(n, self.botState.emaPeriod)
            ema = sum(prices[-ema_period:]) / ema_period

            # Calculate RSI
            rsi_period = min(n, self.botState.rsiPeriod)
            price_diffs = [prices[i] - prices[i-1] for i in range(1, rsi_period)]
            gain_sum = sum([diff for diff in price_diffs if diff > 0])
            loss_sum = -sum([diff for diff in price_diffs if diff < 0])
            rs = gain_sum / loss_sum if loss_sum != 0 else float('inf')
            rsi = 100 - (100 / (1 + rs))

            if current_closing_price > upper_band and rsi > self.botState.overboughtThreshold:
                return self.sell_order("USDT_BTC", 0.5 * affordable)
            elif current_closing_price < lower_band and rsi < self.botState.oversoldThreshold:
                return self.buy_order("USDT_BTC", 0.5 * affordable)
            else:
                return "no_moves"

    def sell_order(self, pair: str, amount: float):
        if "USDT" in self.botState.stacks and self.botState.stacks["USDT"] >= amount:
            return f"sell {pair} {amount}"
        else:
            return "no_moves"

    def buy_order(self, pair: str, amount: float):
        dollars = self.botState.stacks["USDT"]
        price = self.botState.charts[pair].closes[-1]
        if dollars >= amount * price:
            return f"buy {pair} {amount}"
        else:
            return "no_moves"
