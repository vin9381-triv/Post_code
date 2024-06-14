# Sentiment Analysis Project

Welcome to the Sentiment Analysis Project! This repository contains a comprehensive solution for collecting news articles, summarizing them, and analyzing their sentiment. The project utilizes a variety of tools and libraries to accomplish these tasks efficiently.

## Introduction

In the digital age, understanding the sentiment behind news articles can provide valuable insights into public opinion and trends. This project aims to simplify the process of sentiment analysis by automating the collection, summarization, and sentiment evaluation of news articles. By leveraging powerful Python libraries and APIs, we can turn raw news data into meaningful sentiment information.

## Project Structure

The project is divided into several key components:

1. **Sentiment Functions**
2. **Sentiment Analysis Script**

### Sentiment Functions

The `Sentiment_Functions.py` file contains essential functions required for the sentiment analysis process. Below is an overview of each function:

1. **`__init__`**
   - Initializes a MongoDB client connection and sets the collection name for storing and retrieving data.

2. **`collecting_news`**
   - Collects news articles from GNews based on specified keywords and date ranges, processing each article and storing the data.

3. **`generate_unique_identifier`**
   - Generates a unique identifier for a news article based on its title using SHA-256 hashing.

4. **`generate_entry_dict`**
   - Transforms a news article entry into a structured dictionary suitable for database storage, including fields like title, published date, link, and a unique identifier.

5. **`store_data_in_mongo`**
   - Stores a news article entry in the specified MongoDB collection, checking for duplicates to prevent redundant entries.

6. **`summarize_article`**
   - Downloads, parses, and summarizes a news article from a given URL using the `newspaper` library.

7. **Text Preprocessing Helper Functions**
   - Includes functions to lowercase text, expand contractions, tokenize text, remove stopwords and special characters, and lemmatize tokens.

8. **`Preprocessing`**
   - Applies all preprocessing steps to the input text in sequence, ensuring clean and consistent input for sentiment analysis.

9. **`analyze_sentiment`**
   - Uses the TextBlob library to analyze the sentiment of a given text, calculating polarity and subjectivity scores.

### Sentiment Analysis Script

The main script leverages the functions defined in `Sentiment_Functions.py` to perform the following steps:

1. **Setting Up the Logger**
   - Initializes a logger to track the script's progress and log any errors.

2. **Processing Files**
   - Includes a function to move lines from one file to another, useful for managing data processing.

3. **Sentiment Analysis Function**
   - The core function that coordinates the entire sentiment analysis process.

4. **Collecting News Data**
   - Collects news articles based on specified keywords and stores the raw data in a MongoDB database.

5. **Processing and Summarizing Data**
   - Summarizes the collected articles, preprocesses the summaries, analyzes their sentiment, and stores the results in a summary database.

6. **Running Multiple Threads**
   - Utilizes threading to process multiple collections simultaneously, enhancing the script's efficiency.

7. **Moving Processed Lines**
   - Moves processed lines from one file to another to keep track of progress.

## Usage

To get started with the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sentiment-analysis.git
   cd sentiment-analysis
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MongoDB connection and adjust configurations in the script as needed.

4. Run the sentiment analysis script:
   ```bash
   python sentiment_analysis.py
   ```

## Conclusion

This project provides a robust framework for conducting sentiment analysis on news articles. By following the structured approach outlined above, you can easily collect, summarize, and analyze the sentiment of news data. We hope this project serves as a valuable tool for your sentiment analysis needs.

Happy coding! 🎉

For any questions or contributions, feel free to open an issue or submit a pull request.
