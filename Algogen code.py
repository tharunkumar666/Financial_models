from AlgorithmImports import *
import talib
import random
import numpy as np

class LiquidAssetTradingStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  # Start date
        self.SetCash(100000000)  # Starting cash
        
        # Define the top assets in each category (adjust counts as needed)
        self.equities = self.GetTopEquities(500)
        self.crypto = self.GetTopCrypto(10)
        self.forex = self.GetTopForex(20)
        self.futures = self.GetTopFutures(30)
        
        # Combined list of all asset classes
        self.symbols = self.equities + self.crypto + self.forex + self.futures
        self.trailing_stops = {}
        
        # Add each security to the portfolio
        for symbol in self.symbols:
            self.AddSecurity(symbol.SecurityType, symbol, Resolution.Daily)
        
        # Schedule to run the trade function every day at 10:00 AM
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.At(10, 0), self.Trade)
        
        # Track the last asset class traded
        self.last_traded_class = None
    
    def GetTopEquities(self, count):
        return [Symbol.Create(ticker, SecurityType.Equity, Market.USA) for ticker in self.FetchTopTickers("equities", count)]
    
    def GetTopCrypto(self, count):
        return [Symbol.Create(ticker, SecurityType.Crypto, Market.Binance) for ticker in self.FetchTopTickers("crypto", count)]
    
    def GetTopForex(self, count):
        return [Symbol.Create(ticker, SecurityType.Forex, Market.FXCM) for ticker in self.FetchTopTickers("forex", count)]
    
    def GetTopFutures(self, count):
        return [Symbol.Create(ticker, SecurityType.Future, Market.CME) for ticker in self.FetchTopTickers("futures", count)]
    
    def FetchTopTickers(self, asset_class, count):
        # Placeholder: Replace with actual data-fetching logic
        if asset_class == "equities":
            return ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'APO', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BAX', 'BDX', 'BRK.B', 'BBY', 'TECH', 'BIIB', 'BLK', 'BX', 'BK', 'BA', 'BKNG', 'BWA', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BLDR', 'BG', 'BXP', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CPAY', 'CTVA', 'CSGP', 'COST', 'CTRA', 'CRWD', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI', 'DVA', 'DAY', 'DECK', 'DE', 'DELL', 'DAL', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DHI', 'DTE', 'DUK', 'DD', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ERIE', 'ESS', 'EL', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FICO', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FI', 'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GE', 'GEHC', 'GEV', 'GEN', 'GNRC', 'GD', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GL', 'GDDY', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'DOC', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', 'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'INCY', 'IR', 'PODD', 'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM', 'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KVUE', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KKR', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LII', 'LLY', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OTIS', 'PCAR', 'PKG', 'PLTR', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RVTY', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SW', 'SNA', 'SOLV', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SMCI', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TPL', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UBER', 'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VLTO', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VTRS', 'VICI', 'V', 'VST', 'VMC', 'WRB', 'GWW', 'WAB', 'WBA', 'WMT', 'DIS', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WY', 'WMB', 'WTW', 'WDAY', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZTS'][:count]
        elif asset_class == "crypto":
            return ["BTCUSD", "ETHUSD", "BNBUSD", "XRPUSD", "ADAUSD", "DOGEUSD", "SOLUSD", "DOTUSD", "MATICUSD", "LTCUSD"][:count]
        elif asset_class == "forex":
            return ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURJPY", "EURGBP", "GBPJPY", "AUDJPY", "CADJPY", "CHFJPY", "EURAUD", "EURCAD", "EURCHF", "EURNZD", "GBPAUD", "GBPCAD", "GBPNZD"][:count]
        elif asset_class == "futures":
            return ["ES", "NQ", "YM", "RTY", "CL", "GC", "SI", "HG", "ZB", "ZN", "ZF", "ZT", "DX", "BTC", "ETH", "NG", "HO", "RB", "ZC", "ZW", "ZS", "ZM", "ZL", "KC", "SB", "CT", "OJ", "LE", "HE", "GF"][:count]
        return []
    
    def Trade(self):
        # Decide which asset class to trade
        if self.last_traded_class is None or self.Time.day % 10 == 0:
            # Randomly select an asset class to trade (equities, crypto, forex, futures)
            self.last_traded_class = random.choice([self.equities, self.crypto, self.forex, self.futures])
        
        # Get symbols for the currently selected asset class
        current_symbols = self.last_traded_class
        
        for symbol in current_symbols:
            if self.Securities.ContainsKey(symbol):
                history = self.History(symbol, 30, Resolution.Daily)  # Increased to 30 bars for dynamic RSI
                if history.empty:
                    continue
                
                close_prices = history["close"]

                # Calculate RSI (14-period)
                rsi = talib.RSI(close_prices, timeperiod=14)

                #  Dynamic RSI Thresholds
                if len(rsi) >= 20:  # Ensure enough data for calculation
                    mean_rsi = np.mean(rsi[-20:])  # Rolling mean of RSI over last 20 bars
                    std_rsi = np.std(rsi[-20:])    # Rolling standard deviation of RSI
                    
                    oversold_threshold = mean_rsi - std_rsi  # Dynamic Oversold Level
                    overbought_threshold = mean_rsi + std_rsi  # Dynamic Overbought Level
                else:
                    oversold_threshold, overbought_threshold = 30, 70  # Default values if not enough data
                
                #  Calculate Bollinger Bands
                upper_band, middle_band, lower_band = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

                current_price = close_prices.iloc[-1]
                position_size = self.Portfolio.TotalPortfolioValue * 0.065 / current_price
                stop_loss_price = current_price * 0.985  # 1.5% trailing stop loss
                
                #  Dynamic RSI Trading Signals
                if rsi.iloc[-1] < oversold_threshold and current_price <= lower_band[-1]:
                    self.SetHoldings(symbol, 0.065)
                    self.trailing_stops[symbol] = stop_loss_price
                    self.Debug(f"BUY {symbol} - RSI: {rsi.iloc[-1]}, Threshold: {oversold_threshold}")

                elif rsi.iloc[-1] > overbought_threshold and current_price >= upper_band[-1]:
                    self.Liquidate(symbol)
                    self.Debug(f"SELL {symbol} - RSI: {rsi.iloc[-1]}, Threshold: {overbought_threshold}")
                
                #  Implement Trailing Stop Logic
                if symbol in self.trailing_stops:
                    if current_price < self.trailing_stops[symbol]:
                        self.Liquidate(symbol)
                        self.Debug(f"EXIT {symbol} - Hit Trailing Stop")
                    else:
                        new_stop_price = current_price * 0.985
                        self.trailing_stops[symbol] = max(self.trailing_stops[symbol], new_stop_price)
                        self.Debug(f"UPDATE Trailing Stop {symbol} - New Stop: {self.trailing_stops[symbol]}")
