from gnews import GNews
import datetime as dt
from datetime import timedelta, date,datetime
import json
import hashlib
import time
import random
from newspaper import Article, ArticleException
from pymongo import MongoClient
import re
import contractions
from textblob import TextBlob
import nltk
import string 
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class Sentiment_Functions:
    def __init__(self, location="mongodb://localhost:27017", collection_name=None):
        try:
            self.client = MongoClient(location) if location else None
            self.collection_name = collection_name
        except Exception as e:
            print(f"Error creating MongoClient: {e}")
            self.client = None
    
            
    def collecting_news(self, start_date, end_date, keywords,collection_name):
        try:
            news_client = GNews(language='en', country='IN', max_results = 25)
            start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
            collected_data = []
            for keyword in keywords:
                articles_collected = 0
                sDate = start_date

                while sDate <= end_date:
                    news_client.start_date = sDate
                    news_client.end_date = min(sDate + dt.timedelta(days=30), end_date)

                    result = news_client.get_news(keyword)
                    
                    for entry in result:
                        entry_dict = self.generate_entry_dict(collection_name, entry)
                        if entry_dict:
                            collected_data.append(entry_dict)
                            articles_collected += 1

                    sDate += dt.timedelta(days=30)

                    print(f"New Articles collected for keyword '{keyword}': {articles_collected},{news_client.start_date, news_client.end_date}")
                    sleep_time = random.uniform(1, 5)  # Random sleep time between 1 and 5 seconds
                    time.sleep(sleep_time)
            return collected_data
        except Exception as e:
            print(f"Error collecting news: {e}")
            return []

    def generate_unique_identifier(self, title):
        try:
            hash_object = hashlib.sha256(title.encode())
            unique_identifier = hash_object.hexdigest()
            return unique_identifier
        except Exception as e:
            print(f"Error generating unique identifier: {e}")
            return None
        


    def generate_entry_dict(self, collection_name, entry):
        try:
            published_date = entry['published date']
            date_object = datetime.strptime(published_date, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = date_object.strftime("%d/%m/%Y")
            
            return {
                "collection_name": collection_name,
                "title": entry['title'],
                "published_date": formatted_date,  # Include formatted date here
                "link": entry['url'],
                "publisher": {
                    "href": entry['publisher']['href'],
                    "title": entry['publisher']['title'],
                },
                "unique_identifier": self.generate_unique_identifier(entry['title'])
            }
        except Exception as e:
            print(f"Error generating entry dictionary: {e}")
            return None


    def store_data_in_mongo(self, database_name, data, collection_name):
        try:
            if self.client:
                database_names = self.client.list_database_names()
                if database_name not in database_names:
                    print("New database created")
                    db = self.client[database_name]
                else:
                    print("Storing in already existing database")
                    db = self.client[database_name]

                collection = db[collection_name]

                # Check if the data already exists in the collection
                if not collection.find_one({"unique_identifier": data["unique_identifier"]}):
                    collection.insert_one(data)
                    print("Data stored successfully.")
                    return True  # Data successfully stored
                else:
                    print("Duplicate data. Skipping.")
                    return False
            else:
                print("MongoClient not initialized. Unable to store data.")
                return False
        except Exception as e:
            print(f"Error storing data in MongoDB: {e}")
            return False

    def summarize_article(self, url):
        try:
            # print(f"Processing URL: {url}")
            article = Article(url, language='en')
            time.sleep(2)
            article.download()
            article.parse()
            article.nlp()
            return article.summary
        except ArticleException as e:
            print(f"Failed to process article: {e}")
            return None
        except Exception as e:
            print(f"Error summarizing article: {e}")
            return None
        
    
        return text
    def _lowercase(self, text):
        return text.lower()

    def _expand_contractions(self, text):
        return contractions.fix(text)

    def _tokenize(self, text):
        return word_tokenize(text)

    def _remove_stopwords(self, tokens):
        stop_words = set(stopwords.words("english"))
        punctuation_set = set(string.punctuation)
        stop_words.update(punctuation_set)

        return [word for word in tokens if word.lower() not in stop_words]

    def _remove_special_characters(self, tokens):
        return [re.sub(r'[^a-zA-Z]', '', word) for word in tokens if word.isalpha()]

    def _lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in tokens]

    def _join_tokens(self, tokens):
        return ' '.join(tokens)

    def Preprocessing(self, text):
        if text is None:
            return None
        # Apply each step of preprocessing
        text = self._lowercase(text)
        text = self._expand_contractions(text)
        tokens = self._tokenize(text)
        tokens = self._remove_stopwords(tokens)
        tokens = self._remove_special_characters(tokens)
        tokens = self._lemmatize(tokens)
        preprocessed_text = self._join_tokens(tokens)

        return preprocessed_text
    
    def analyze_sentiment(self, text):
        try:
            if text:
                analysis = TextBlob(text)
                sentiment = {
                    "polarity": analysis.sentiment.polarity,
                    "subjectivity": analysis.sentiment.subjectivity
                }
                return sentiment
            else:
                print("No text provided for sentiment analysis.")
                return None
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return None