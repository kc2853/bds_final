import os
import pandas as pd


def process_and_export(path_from, path_to):
    df1 = pd.read_csv(os.path.join(path_from, 'export-EtherPrice.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df2 = pd.read_csv(os.path.join(path_from, 'export-MarketCap.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df3 = pd.read_csv(os.path.join(path_from, 'export-Ethersupply2.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df4 = pd.read_csv(os.path.join(path_from, 'export-TxGrowth.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df5 = pd.read_csv(os.path.join(path_from, 'export-AddressCount.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df6 = pd.read_csv(os.path.join(path_from, 'export-BlockSize.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df7 = pd.read_csv(os.path.join(path_from, 'export-BlockTime.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df8 = pd.read_csv(os.path.join(path_from, 'export-AvgGasPrice.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df9 = pd.read_csv(os.path.join(path_from, 'export-GasUsed.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df10 = pd.read_csv(os.path.join(path_from, 'export-NetworkHash.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df11 = pd.read_csv(os.path.join(path_from, 'export-TransactionFee.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df12 = pd.read_csv(os.path.join(path_from, 'export-NetworkUtilization.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]
    df13 = pd.read_csv(os.path.join(path_from, 'export-BlockReward.csv'), parse_dates=['Date(UTC)'], index_col='Date(UTC)')['2015-08-07':]

    res = df1
    del res['UnixTimeStamp']
    res['2'] = df2['MarketCap']
    res['3'] = df3['Value']
    res['4'] = df4['Value']
    res['5'] = df5['Value']
    res['6'] = df6['Value']
    res['7'] = df7['Value']
    res['8'] = df8['Value (Wei)']
    res['9'] = df9['Value']
    res['10'] = df10['Value']
    res['11'] = df11['Value']
    res['12'] = df12['Value']
    res['13'] = df13['Value']
    res.columns = ['Price', 'MarketCap', 'Supply', 'TxGrowth', 'AddressCount', 'BlockSize', 'BlockTime', 'AvgGasPrice', 'GasUsed', 'NetworkHash', 'TransactionFee', 'NetworkUtilization', 'BlockReward']
    res.to_csv(path_to)
    print('Successfully exported to:', path_to)


if __name__ == '__main__':
    process_and_export('data/blockchain', 'data/Final.csv')