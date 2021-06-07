import pandas as pd
import re
import string

import nltk 

import datetime as dt

import argparse
import os.path
import sys

def preprocess_text(row):
    text = row['text']
    #remove URL links
    text = re.sub(r"http\S+", "", text)
    
    #extract only characters, numbers, hashtags and tags
    #remove punctuation and emoji 
    text = re.sub('[^A-Za-z0-9#@]+', ' ', text)

    # remove stand-alone numbers
    text = re.sub(r'\b[0-9]+\b\s*', ' ',  text)

    # remove stand-alone characters
    text = re.sub(r'\b[A-Za-z]\b', ' ',  text)


    #lowerize
    text = text.lower()
    #tokenize
    text = text.split()
    #remove duplicate words in the same tweet
    text = list(set(text))

    #remove stopwords
    stopword = nltk.corpus.stopwords.words('english')
    text = [word for word in text if word not in stopword]
    
    return text

def toDatetime(row):
    #convert string to datetime type
    date = row['date']
    format = '%Y-%m-%d %H:%M:%S'
    return dt.datetime.strptime(date, format).date()


def dateToDict(times):
    #takes as input a list of sorted dates
    #returns a dict of dates with index the datetime and value an integer
    dates = dict()
    for time in times:
        if not dates:
            dates[time] = 1
        else:
            if time not in dates:
                last = list(dates)[-1]
                diff = time - last
                dates[time] = dates[last]+diff.days  
    return dates

def dataToList(data, dates_dict):
    data_list = []
    for _, row in data.iterrows():
        date = row['date']
        text = row['text']
        str1 = " "
        temp =  [dates_dict[date],str1.join(text)]
        # temp =  [dates_dict[date],text]
        data_list.append(temp)
    return data_list


def importFromCSV(input):
    print("Processing data csv file ...")
    data = pd.read_csv(input,delimiter=';')
    data = data[["date","text"]]
    
    data = data.dropna(how='any')
    data = data.drop_duplicates()

    data['text'] = data.apply(preprocess_text, axis=1)
    data['date'] = data.apply(toDatetime, axis=1)
    data = data.sort_values(by='date')

    dates_dict = dateToDict(list(data['date']))

    data_list = dataToList(data,dates_dict)

    print("Done!")
    return data_list      

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Preprocess Raw csv file')

    parser.add_argument("--input",
                        help="csv raw data input", default="covid19_tweets.csv")

    parser.add_argument("--output",
                        help="csv preprocessed data output", default="data1.csv")

    args = parser.parse_args()

    data = importFromCSV(args.input)
    df = pd.DataFrame(data,columns=['Time','Words'])

    df.to_csv(args.output,index=False)
