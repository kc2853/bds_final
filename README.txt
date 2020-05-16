Notes on running and reading the files
• Python 3.7.4

• Python packages that may need to be downloaded: numpy, matplotlib, pandas, statsmodels, pmdarima, beautifulsoup4, tweepy, urllib3, vaderSentiment

• Data collection process
i) Blockchain data
1. Download the following files to the data/blockchain directory from https://etherscan.io/charts which is Etherscan:
export-BlockReward.csv
export-NetworkUtilization.csv
export-TransactionFee.csv
export-NetworkHash.csv
export-GasUsed.csv
export-AvgGasPrice.csv
export-BlockTime.csv
export-BlockSize.csv
export-AddressCount.csv
export-TxGrowth.csv
export-Ethersupply2.csv
export-MarketCap.csv
export-EtherPrice.csv

2. Run `python blockchain_data.py` which will compile all of the above spreadsheets into one master spreadsheet for blockchain data at data/Final.csv.

ii) Twitter data
1. Run `python get_tweets.py all 3500` which will start scraping up to 3500 (which is around Twitter's rate limit) tweets per 100 influencers from CryptoWeekly (scraped from CryptoWeekly's website) and add the tweets as csv files to the data/tweets directory.
2. One can repeat this process multiple times, and the resulting tweets will get merged automatically (such that new data would be prepended to the old data seamlessly).
3. If the above is done, then run `python score_tweets.py` which will apply VADER's sentiment analysis on the tweets at the data/tweets directory, apply couple mathematical calculations to generate new columns, and merge them into one master spreadsheet for Twitter data at data/tweets_influencers.csv.

iii) Merging blockchain data and Twitter data
1. Open final_project_featureset.ipynb.
2. Run all cells (manually or by clicking Run All).
3. Find the cell (after having run all cells) that contains definitions of store_timeseries() and store_timeseries_binary() which allow custom date inputs. By running the methods, one can export the merged spreadsheet (with custom date inputs) that is ready to be processed and analyzed by RapidMiner.

• RapidMiner
1. There are 8 processes (corresponding to 4 machine learning algorithms per problem instance, regression or binary classification):
ETH project_GBT
ETH project_GBT_binary
ETH project_SVM
ETH project_SVM_binary
ETH project_NN
ETH project_NN_binary
ETH project_LSTM
ETH project_LSTM_binary

2. One can import data into RapidMiner from the output of the above iii). Make sure to specify the dates as "Date(UTC)" and set its role as id. In binary classification, make sure to change the data type of PriceChange to binomial when importing.

3. While one should be able to run the processes as they are (given the data have been downloaded or imported correctly), one should also make sure to change export destinations for export operators (e.g. GBT_WindowSize1 Results) so that export locations exist in the local machine.

4. For LSTM, one needs to download the Deep Learning extension package (not the Keras version). Note that LSTM processes have used the Loop Parameters operator (rather than the Optimize Parameters operator) and thus do not need any connections to Results in order to run.

• One should be able to open and run final_project_timeseries.ipynb after the data collection process. It is a tutorial / documentation on its own regarding applying traditional time series modeling techniques on our Ethereum price data.

• results/binary folder contains results for all 4 machine learning algorithms (GBT, SVM, NN, and LSTM) with regards to binary classification. In the .res files (this would be true with .res files elsewhere as well), one should note that three results (i.e. Parameter set, AttributeWeights, and PerformanceVector) are logged per window size per machine learning algorithm. Since 5 window sizes have been experimented with per machine learning algorithm, this means that results/binary/GBT_binary.res (for example) contains 15 results: (Parameter set, AttributeWeights, PerformanceVector) for window sizes 1, 2, 3, 7, and 10.
1. Parameter set: This is yielded by RapidMiner's Optimize Parameters operator. It outputs the sliding window validation errors (used in the final report) as well as the optimal set of parameters yet to be tested on out-of-sample data.
2. AttributeWeights: This is yielded by RapidMiner's Explain Predictions operator and outputs the global weights of features corresponding to the trained machine learning model. It is a way to see which features are the ones that make contributions to forecasting.
3. PerformanceVector: This manifests the performance of our trained machine learning model on out-of-sample (test) data.

• results/regression folder contains results for all 4 machine learning algorithms (GBT, SVM, NN, and LSTM) with regards to regression. The above regarding .res files applies here as well (except the fact that results per window size have been separated out as separate files).

• Note that results with LSTM are in a csv format (in results/binary and results/regression). This is because Loop Parameters (as opposed to Optimize Parameters) has been used only for LSTM.