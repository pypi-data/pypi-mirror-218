import pandas as pd
from regbot import signal

df = pd.read_csv('../reinforce/regbot_v49_training.csv')

y_pred = []
def getSignal(a,b,c):
    return signal(a,b,c)

print(df.head())
df = df.sample(frac=1).reset_index(drop=True)
print(df.head())
df = df[df['targets'] == 1].tail(20)
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['b'],row['close-gradient'],row['close-gradient-neg']), axis=1)

print(df.head())

print(len(df[df['result'] == df['targets']]), len(df))
