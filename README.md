# Mining Tweets
 Mining Time-Consistent Popular Topics in Tweets

## Main program
To run the main program using Temporal Apriori or FP-Growth:

`python main.py --apriori [--input --ndata --supp --minTsupp --maxTsupp]`

`python main.py --fp [--input --ndata --supp --minTsupp --maxTsupp]`

### Parameters
- apriori Execute apriori process
- fp Execute FP-Growth process
- input String name of csv file, output of preprocessing (default "data.csv")
- ndata Integer Number of transactions (default 10000)
- supp Float Minimum Support Threshold (default 0.5)
- minTsupp Integer Minimum Temporal Support Threshold (default 3)
- maxTsupp Integer Maximum Temporal Support Threshold (default 21)

---

## Preprocessing
To preprocess raw data:

`python preprocessing.py [--input --output]`

### Parameters
- input String name of csv input file, raw data (default "covid19_tweets.csv")
- output String name of csv output file, preprocessed data(default "data.csv")
### Output
- csv preprocessed data

--- 

## Evaluation Program
To run test comparison on Temporal Apriori and FP-Growth:

`python eval.py --test {1, 2, 3}`

### Parameters
1. Number of transactions
2. Support Threshold
3. Temporal Support Threshold

### Output

- html report


To run a single test and see topic table:

`python eval.py --table [--input --ndata --supp --minTsupp --maxTsupp]`

### Parameters
- input String name of csv file, output of preprocessing (default "data.csv")
- ndata Integer Number of transactions (default 10000)
- supp Float Minimum Support Threshold (default 0.5)
- minTsupp Integer Minimum Temporal Support Threshold (default 3)
- maxTsupp Integer Maximum Temporal Support Threshold (default 21)

### Output

- html report