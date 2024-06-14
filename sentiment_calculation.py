import json
import logging
import threading
import time
from Sentiment_Functions import Sentiment_Functions

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('Sentiment_Analysis.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def process_files(line, source_file, destination_file):
    with open(destination_file, 'a+') as dest_file:
        dest_file.write(line + '\n')
    # Remove the processed line from the source file
    lines = []
    with open(source_file, 'r') as src_file:
        lines = src_file.readlines()
    with open(source_file, 'w') as src_file:
        for l in lines[1:]:
            src_file.write(l)

def sentiment_analysis(collection_name, keywords, database_name_raw, database_name_summary, database_name_sentiment, thread_index):
    try:
        start_time = time.time()
        sentiment_instance = Sentiment_Functions(collection_name=collection_name)
        
        # Collect news data
        collected_data = sentiment_instance.collecting_news('2017-07-01', '2017-12-01', keywords, collection_name)

        # Store raw data
        for entry_dict in collected_data:
            sentiment_instance.store_data_in_mongo(database_name_raw, entry_dict, collection_name)

        # Process data and store summary and sentiment
        raw_db = sentiment_instance.client[database_name_raw]
        summary_db = sentiment_instance.client[database_name_summary]
        sentiment_db = sentiment_instance.client[database_name_sentiment]
        for cause_name in raw_db.list_collection_names():
            if cause_name == collection_name:  
                raw_collection_name = raw_db[cause_name]
                summary_collection_name = summary_db[cause_name]
                sentiment_collection_name = sentiment_db[cause_name]
                for entry in raw_collection_name.find():
                    raw_data = entry
                    raw_data["_id"] = str(raw_data["_id"])
                    
                    # Check if summary already exists in summarized data collection
                    if summary_collection_name.find_one({"_id": raw_data["_id"]}):
                        logger.info(f"Summary already exists for {raw_data['title']} in summarized data. Skipping.")
                        continue

                    # Generate summary
                    raw_data["summary"] = sentiment_instance.summarize_article(raw_data["link"])
                    raw_data["pre_processed_summary"] = sentiment_instance.Preprocessing(raw_data["summary"])
                    if raw_data["summary"]:
                        # Store summary data
                        sentiment_instance.store_data_in_mongo(database_name_summary, raw_data, cause_name)
                        logger.info(f"Summary stored successfully for {raw_data['title']}")

                        # Generate and store sentiment
                        sentiment = sentiment_instance.analyze_sentiment(raw_data["pre_processed_summary"])
                        sentiment_data = {
                            "_id": raw_data["_id"],
                            "title": raw_data["title"],
                            "summary": raw_data["summary"],
                            "sentiment": sentiment
                        }
                        sentiment_instance.store_data_in_mongo(database_name_sentiment, sentiment_data, cause_name)
                        logger.info(f"Sentiment stored successfully for {raw_data['title']}")
                    else:
                        logger.warning(f"Skipping summary and sentiment storage for {raw_data['title']} due to an error.")

        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Thread {thread_index} finished in {elapsed_time:.2f} seconds")

    except Exception as e:
        logger.error(f"Error in sentiment_analysis: {e}")

# Read one line from to_be_processed.txt
with open('to_be_processed.txt', 'r') as file:
    line = file.readline().strip()
    if line:
        process_files(line, 'to_be_processed.txt', 'socio_economic.txt')

# Read socio_economic_collections after processing to_be_processed.txt
with open('Socio_economic.txt', 'r') as file:
    socio_economic_collections = [json.loads(line) for line in file]

threads = []
for thread_index, collection_data in enumerate(socio_economic_collections, start=1):
    collection_name = collection_data["collection"]
    keywords = collection_data["keywords"]
    thread = threading.Thread(
        target=sentiment_analysis,
        args=(collection_name, keywords, 'raw_data', 'summarized_data', 'sentiment_data', thread_index))
    threads.append(thread)

logger.info(f"Number of threads: {len(threads)}")
start_time_total = time.time()

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end_time_total = time.time()
elapsed_time_total = end_time_total - start_time_total
logger.info(f"All threads finished in {elapsed_time_total:.2f} seconds")

# Move the processed line from socio_economic.txt to processed.txt
with open('Socio_economic.txt', 'r') as socio_economic_file:
    processed_line = socio_economic_file.readline().strip()

if processed_line:
    process_files(processed_line, 'socio_economic.txt', 'processed.txt')

