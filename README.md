# ⛏️ Mining Consistent Popular Topics in Tweets

**Mining Tweets** is a data mining project designed to identify and analyze popular topics in tweets over time, developed as part of a Data Mining course project. This tool utilizes a **modified FP-Growth algorithm** and **Temporal Apriori** to track consistent, time-relevant trends in tweet datasets.

## 🚀 Features

1. **Time-Aware Topic Mining**: Finds word sets (topics) that appear together within specified timeframes, ensuring insights remain relevant.
2. **Modified FP-Growth Algorithm**: Optimized for speed and scalability, avoiding redundant candidate generation while incorporating temporal support.
3. **Flexible Data Preprocessing**: Filters, cleans, and formats raw tweets into structured data, handling large-scale datasets efficiently.
4. **Interactive Evaluation**: Generates HTML reports comparing Temporal Apriori and FP-Growth in terms of speed and result quality.

## 🔍 Dataset
This project uses a dataset of **179,000 tweets** on COVID-19 from [Kaggle](https://www.kaggle.com/gpreda/covid19-tweets). The dataset was preprocessed to retain only the date and text fields, with further cleaning steps to remove URLs, stopwords, punctuation, and irrelevant symbols.

## 📊 Experimental Evaluation
This project compares Temporal Apriori and FP-Growth algorithms in:
1. **Speed**: FP-Growth shows scalability improvements with large datasets, remaining consistent as data volume increases.
2. **Quality**: FP-Growth consistently generates similar and high-quality frequent itemsets when compared to Apriori.

Performance tests reveal that FP-Growth is significantly faster than Apriori, making it a more suitable choice for large datasets.

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/mining-tweets.git
   cd mining-tweets
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📂 Project Structure

- `main.py`: The main program to run Temporal Apriori or FP-Growth algorithms.
- `preprocessing.py`: Preprocesses raw tweet data for analysis.
- `eval.py`: Runs evaluations to compare algorithm performance, including result quality and speed.

---

## 💡 Usage

### 1. Preprocess Raw Data
Prepare raw tweet data for mining with:
```bash
python preprocessing.py [--input --output]
```
**Parameters**:
- `--input` (default "covid19_tweets.csv"") - Raw CSV data file.
- `--output` (default "data.csv") - Output file for processed data.

**Output**:
- csv preprocessed data

### 2. Run Main Program
Analyze time-relevant frequent topics using Temporal Apriori or FP-Growth:
```bash
python main.py --apriori [--input --ndata --supp --minTsupp --maxTsupp]
```
or 
```bash
python main.py --fp [--input --ndata --supp --minTsupp --maxTsupp]
```
**Parameters**:
- `--input` (default "data.csv") - Preprocessed CSV file of tweets.
- `--ndata` (default 10000) - Number of transactions (tweets).
- `--supp` (default 0.5) - Minimum Support Threshold.
- `--minTsupp` (default 3) - Minimum Temporal Support Threshold (days).
- `--maxTsupp` (default 21) - Maximum Temporal Support Threshold (days).

### 3. Run Evaluation Program
Run comparative tests between Temporal Apriori and FP-Growth:
```bash
python eval.py --test {1, 2, 3}
```
**Parameters**:
1. Number of transactions
2. Support Threshold
3. Temporal Support Threshold
   
**Output**:
- html report

Alternatively, generate a topic table for single test analysis:
```bash
python eval.py --table [--input --ndata --supp --minTsupp --maxTsupp]
```
- `--input` (default "data.csv") - Preprocessed CSV file of tweets.
- `--ndata` (default 10000) - Number of transactions (tweets).
- `--supp` (default 0.5) - Minimum Support Threshold.
- `--minTsupp` (default 3) - Minimum Temporal Support Threshold (days).
- `--maxTsupp` (default 21) - Maximum Temporal Support Threshold (days).

**Output**:
- html report

---

## 📈 Example Commands
```bash
# Run Apriori with specific parameters
python main.py --apriori --input "data.csv" --ndata 5000 --supp 0.4 --minTsupp 2 --maxTsupp 10

# Preprocess raw tweet data
python preprocessing.py --input "raw_tweets.csv" --output "data.csv"

# Run evaluation test and generate report
python eval.py --test 1
```


---

Happy mining! 🎉
