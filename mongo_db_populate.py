import os
import sys
import pandas as pd
from pymongo import MongoClient
import argparse
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=os.getenv('LOGGING_LEVEL', default=logging.INFO))
logger = logging.getLogger(__name__)

def main(folder_path, mongo_host, mongo_port=27017, mongo_password=None):
    # Extract database name from folder name
    database_name = os.path.basename(os.path.normpath(folder_path))

    # Build the MongoDB URI
    mongo_uri = f'mongodb://{mongo_host}:{mongo_port}'

    # Log the connection details (without the password)
    logger.info(f'Connecting to MongoDB at {mongo_host}:{mongo_port}')

    try:
        # Establish MongoDB connection
        client = MongoClient(mongo_uri, password=mongo_password) if mongo_password else MongoClient(mongo_uri)
        db = client[database_name]

        # Iterate through each CSV file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                collection_name = os.path.splitext(filename)[0]
                logger.info(f'Creating collection {collection_name}')

                # Read CSV file into DataFrame
                csv_path = os.path.join(folder_path, filename)
                df = pd.read_csv(csv_path)

                # Convert DataFrame to dictionary and insert into MongoDB
                collection = db[collection_name]
                collection.insert_many(df.to_dict('records'))

                logger.info(f'Inserted {len(df)} records into collection {collection_name}')

    except Exception as e:
        logger .error(f'Error occurred: {e}')
    finally:
        # Close MongoDB connection
        client.close()
        logger.info('MongoDB connection closed')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import CSV files to MongoDB collections.')
    parser.add_argument('folder_path', help='Path to the folder containing CSV files')
    parser.add_argument('mongo_host', help='MongoDB host')
    parser.add_argument('-P', '--port', type=int, help='MongoDB port', default=27017)
    parser.add_argument('-p', '--password', help='MongoDB password', default=None)

    args = parser.parse_args()

    main(args.folder_path, args.mongo_host, args.port, args.password)