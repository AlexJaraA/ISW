import pandas as pd
import numpy as np
import math as m


def icsv(path):
    df = pd.read_csv(path)
    print(df.shape)
    df = df[['Date', 'Close']]
    return df


def volatility(df):
    lista = list()
    for i in range(0, df.shape[0]):
        if(i == 0):
            lista.append(0)
        else:
            lista.append(df.at[i, 'Close']/df.at[i-1, 'Close'])
    df['Dt'] = lista
    df['Rt'] = np.log(lista)
    df.at[0,'Rt'] = 0
    mean = np.mean(df['Rt'])
    df['Dev'] = pow(df['Rt'] - mean, 2)
    return m.sqrt(np.mean(df['Dev'])*252)


def iterations(x, y, price, riskfree, volatility, time):
    np.random.seed(1)
    St = 0
    Sf = 0
    time = (time/12)/y
    for i in range(0, x):
        for j in range(0, y):
            if j == 0:
                S = [price]
            else:
                auxiliar = riskfree*S[j-1]*time + volatility*S[j-1]*np.random.normal(0, 1, 1)*m.sqrt(time)
                S.append(S[j-1] + auxiliar)       
        if i == 0:
            Z = S
        else:
            list_of = [Z, S]
            Z = [sum(x) for x in zip(*list_of)]
        St = St + max((S[y-1] - price), 0)
        Sf = Sf + S[y-1]

    return [a / x for a in Z], St/x, Sf/x
