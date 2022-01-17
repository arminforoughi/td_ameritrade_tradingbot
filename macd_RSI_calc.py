import td_trade as td
import pandas as pd





class calculate_macd:
    def __init__(self, df):
        self.new_df = df[34:]
        #macd
        self.df = df
        self.low_ema = 12
        self.high_ema = 26
        self.macd = 0
        self.signal = 0
        self.bar = 0
        self.bar_slope = 0
        self.ema_12 = self.df['close'][:self.low_ema].mean()
        self.ema_26 = self.df['close'][:self.high_ema].mean()
        #rsi
        self.previus_price = 0
        self.price_change = 0
        self.gain = 0
        self.loss = 0
        self.ave_gain = 0
        self.ave_loss = 0
        self.rsi = 0
        self.df["price_change"] = pd.NaT
        self.df["gain"] = pd.NaT
        self.df["loss"] = pd.NaT
        self.df["ave_gain"] = pd.NaT
        self.df["ave_loss"] = pd.NaT
        self.df["rsi"] = pd.NaT
        self.df_2 = self.df[self.low_ema:self.high_ema]


    def rsi_calculations(self, x):
        self.price_change = x - self.previus_price
        self.previus_price = x
        if self.price_change > 0:
            self.gain = self.price_change
            self.loss = 0
        else:
            self.gain = 0
            self.loss = abs(self.price_change)
        return self.price_change, self.gain, self.loss

    def ema_12_c(self, x):

        self.ema_12 = x * (2/(self.low_ema+1)) + self.ema_12 * (1 - (2/(self.low_ema+1)))
        return self.rsi_calculations(x)

    def first_14(self):

        self.df_2['price_change'], self.df_2['gain'], self.df_2['loss'] = zip(*self.df['close'][self.low_ema:self.high_ema].apply(self.ema_12_c))
        self.df['price_change'][self.low_ema:self.high_ema] = self.df_2['price_change']
        self.df['gain'][self.low_ema:self.high_ema] = self.df_2['gain']
        self.df['loss'][self.low_ema:self.high_ema] = self.df_2['loss']

    def macd_c(self, x):

        self.ema_12 = x * (2/(self.low_ema+1)) + self.ema_12 * (1 - (2/(self.low_ema+1)))
        self.ema_26 = x * (2/(self.high_ema+1)) + self.ema_26 * (1 - (2/(self.high_ema+1)))
        self.macd = self.ema_12 - self.ema_26
        return self.macd

    def get_rsi(self, index):
        if index < 48:
            mean_gain = self.df['gain'].loc[index - 14:index].mean()
            mean_loss = self.df['loss'].loc[index - 14:index].mean()
        else:
            mean_gain = self.new_df['gain'].loc[index - 14:index].mean()
            mean_loss = self.new_df['loss'].loc[index - 14:index].mean()


        rs = round(mean_gain / mean_loss, 2)
        rsi = round(100 - (100 / (1 + rs)), 2)

        return mean_gain, mean_loss, rsi

    def get_rsi_new(self, new_gain, new_loss):

        mean_gain = (self.new_df['gain'][-13:].sum() + new_gain) / 14
        mean_loss = (self.new_df['loss'][-13:].sum() + new_loss) / 14


        rs = round(mean_gain / mean_loss, 2)
        rsi = round(100 - (100 / (1 + rs)), 2)

        return mean_gain, mean_loss, rsi


    def f25_34(self):
        self.df_2 = self.df[self.high_ema:34]

        self.df_2['price_change'], self.df_2['gain'], self.df_2['loss'] = zip(*self.df['close'][self.high_ema:34].apply(self.rsi_calculations))
        self.df_2['ave_gain'], self.df_2['ave_loss'], self.df_2['rsi'] = zip(*self.df[self.high_ema:34].index.to_series().apply(self.get_rsi))

        self.df['price_change'][self.high_ema:34]= self.df_2['price_change']
        self.df['gain'][self.high_ema:34] = self.df_2['gain']
        self.df['loss'][self.high_ema:34] = self.df_2['loss']
        self.df['ave_gain'][self.high_ema:34] = self.df_2['ave_gain']
        self.df['ave_loss'][self.high_ema:34] = self.df_2['ave_loss']
        self.df['rsi'][self.high_ema:34] = self.df_2['rsi']
        return self.df['close'][self.high_ema:34].apply(self.macd_c)


    def macd_signal_c(self, x):

        self.ema_12 = x * (2/(self.low_ema+1)) + self.ema_12 * (1 - (2/(self.low_ema+1)))
        self.ema_26 = x * (2/(self.high_ema+1)) + self.ema_26 * (1 - (2/(self.high_ema+1)))
        self.macd = self.ema_12 - self.ema_26
        self.signal = self.macd *(2/(9+1)) + self.signal * (1-(2/(9+1)))
        self.bar_slope =  (self.macd - self.signal) - self.bar
        self.bar = self.macd - self.signal

        return self.ema_12, self.ema_26,  self.macd, self.signal, self.bar, self.bar_slope


    def rest(self):
        self.new_df['price_change'], self.new_df['gain'], self.new_df['loss'] = zip(*self.df['close'][34:].apply(self.rsi_calculations))
        self.new_df['ave_gain'], self.new_df['ave_loss'], self.new_df['rsi'] = zip(*self.df[34:].index.to_series().apply(self.get_rsi))


        return self.df['close'][34:].apply(self.macd_signal_c)

    def all(self):
        self.first_14()
        self.signal = self.f25_34().mean()
        self.new_df['ema_12'], self.new_df['ema_26'], self.new_df['macd'], self.new_df['signal'], self.new_df['bar'], self.new_df['bar_slope']  = zip(*self.rest())


min_15 = td.price_history('SPY', 15)
min_60 = td.price_history('SPY', 60)


df_15 = pd.json_normalize(min_15['candles'])[['close', 'volume']]
df_60 = pd.json_normalize(min_60['candles'])[['close', 'volume']]


macd_15 = calculate_macd(df_15)
macd_60 = calculate_macd(df_60)

macd_15.all()
macd_60.all()
print(macd_15.new_df)
#print(macd_60.new_df)


dicc = {'close': 465.31, 'volume': 14234.0, 'price_change': -0.040000000000020464, 'gain': 0.0, 'loss': 0.040000000000020464, 'ave_gain': 0.04666666666666212, 'ave_loss': 0.037333333333329694, 'rsi': 55.56, 'ema_12': 465.19474183808734, 'ema_26': 464.5803994235635, 'macd': 0.6143424145238328, 'signal': 0.6867653023035744, 'bar': -0.0724228877797416, 'bar_slope': -0.01930629473129286}



def add_new_price(new_price, volume):
    dicc['close'], dicc['volume'] = new_price, volume
    dicc['ema_12'], dicc['ema_26'], dicc['macd'], dicc['signal'], dicc['bar'], dicc['bar_slope']  = macd_15.macd_signal_c(new_price)
    dicc['price_change'], dicc['gain'], dicc['loss'] = macd_15.rsi_calculations(new_price)
    dicc['ave_gain'], dicc['ave_loss'], dicc['rsi'] = macd_15.get_rsi_new(dicc['gain'], dicc['loss'])

    macd_15.new_df = macd_15.new_df.append(dicc, ignore_index = True)


add_new_price(460.31, 2)
add_new_price(464.31, 2)

print(macd_15.new_df)
