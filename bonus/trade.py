#!/usr/bin/python3
# -*- coding: iso-8859-1 -*
""" Python starter bot for the Crypto Trader games, from ex-Riddles.io """
__version__ = "1.0"

import sys
from .numpy import numpy as np
from .pandas import pandas as pd
from .tensorflow.keras.models import load_model

class Bot:
    def __init__(self):
        self.botState = BotState()
        self.threshold_upper = 1.02
        self.threshold_lower = 0.98

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
            # This won't work every time, but it works sometimes!
            dollars = self.botState.stacks["USDT"]
            current_closing_price = self.botState.charts["USDT_BTC"].closes[-1]
            affordable = dollars / current_closing_price
            # print(f'My stacks are {dollars}. The current closing price is {current_closing_price}. So I can afford {affordable}', file=sys.stderr)
            if dollars < 100:
                print("no_moves", flush=True)
            else:
                position_data = self.botState.get_position_data("USDT_BTC")
                df = pd.DataFrame(position_data, columns=["volume", "high", "low", "open"])
                model = load_model('model_MC.h5')
                window_len = 5
                zero_base = True
                num_mc_samples = 100
                prediction = self.predict_from_MC(df, model, window_len, zero_base, num_mc_samples)
                
                current_price = self.botState.charts["USDT_BTC"].closes[-1]
                if prediction > current_price * self.threshold_upper:
                    self.decision = 'buy'
                elif prediction < current_price * self.threshold_lower:
                    self.decision = 'sell'
                else:
                    self.decision = 'no_moves'

                if self.decision != 'no_moves':
                    risk_levels = self.calculate_risk_levels(prediction)
                    trade_percentage = self.calculate_trade_percentage(risk_levels)
                    amount = self.decide_amount(trade_percentage)
            
                    if self.decision == 'buy':
                        print(f'buy USDT_BTC {amount}', flush=True)
                    elif self.decision == 'sell':
                        print(f'sell USDT_BTC {amount}', flush=True)
    
    def normalise_min_max(self, df):
        return (df - df.min()) / (data.max() - df.min())
    
    def normalise_zero_base(self, df):
        if df.iloc[0].any() != 0:
            return df / df.iloc[0] - 1
        else:
            return df


    def extract_window_data(self, df, window_len=5, zero_base=True):
        window_data = []
        for idx in range(len(df) - window_len):
            tmp = df[idx: (idx + window_len)].copy()
            if zero_base:
                tmp = self.normalise_zero_base(tmp)
            window_data.append(tmp.values)
        return np.array(window_data)

    def predict_from_MC(self, df, model, window_len, zero_base, num_mc_samples, alpha=0.05):
        data = df.dropna()
        data = data[['high', 'low', 'open', 'volume']]

        live_data = self.extract_window_data(data, window_len, zero_base)
        predictions = []
        for _ in range(num_mc_samples):
            preds = model.predict(live_data)
            predictions.append(preds)

        return predictions
    
    def calculate_risk_levels(self, predictions, alpha=0.05):
        
        predictions = np.array(predictions)
        mean_preds = np.mean(predictions, axis=0)
        std_preds = np.std(predictions, axis=0)

        var_preds = np.percentile(predictions, 100 * alpha, axis=0)

        sorted_preds = np.sort(predictions, axis=0)
        num_cvar = int((1 - alpha) * num_mc_samples)
        cvar_preds = np.mean(sorted_preds[:num_cvar], axis=0)

        risk_levels = np.zeros_like(mean_preds)
        risk_levels[mean_preds <= var_preds] = 1
        risk_levels[(mean_preds > var_preds) & (mean_preds <= cvar_preds)] = 2
        risk_levels[(mean_preds > cvar_preds) & (mean_preds <= mean_preds + std_preds)] = 3
        risk_levels[(mean_preds > mean_preds + std_preds) & (mean_preds <= mean_preds + 2 * std_preds)] = 4
        risk_levels[mean_preds > mean_preds + 2 * std_preds] = 5

        return risk_levels
    
    def calculate_trade_percentage(self, risk_level):
    
        if risk_level == 1:
            return 0.4
        elif risk_level == 2:
            return 0.35
        elif risk_level == 3:
            return 0.3
        elif risk_level == 4:
            return 0.25
        elif risk_level == 5:
            return 0.1
        else:
            return 0

    def decide_amount(self, trade_percentage):
        portfolio_value = self.botState.stacks["USDT"]
        btc_price = self.botState.charts["USDT_BTC"].closes[-1]
        amount = portfolio_value * trade_percentage / btc_price
        return amount      
        
class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for (i, key) in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)


class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)


class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.1
        self.date = 0
        self.stacks = dict()
        self.charts = dict()

    def update_chart(self, pair: str, new_candle_str: str):
        if not (pair in self.charts):
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        if key == "time_per_move":
            self.timePerMove = int(value)
        if key == "candle_interval":
            self.candleInterval = int(value)
        if key == "candle_format":
            self.candleFormat = value.split(",")
        if key == "candles_total":
            self.candlesTotal = int(value)
        if key == "candles_given":
            self.candlesGiven = int(value)
        if key == "initial_stack":
            self.initialStack = int(value)
        if key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))
    
    def get_position_data(self, pair):
        if pair in self.charts:
            chart = self.charts[pair]
            position_data = []
            for i in range(len(chart.dates)):
                candle_data = {
                    "volume": chart.volumes[i],
                    "high": chart.highs[i],
                    "low": chart.lows[i],
                    "open": chart.opens[i]
                }
                position_data.append(candle_data)
            return position_data
        return []

if __name__ == "__main__":
    mybot = Bot()
    mybot.run()
