# CSV to MongoDB Importer

This Python script imports CSV files from a specified folder into a MongoDB database. Each CSV file is imported into a separate MongoDB collection. The name of the database is derived from the folder name, and the name of each collection is derived from the CSV file name.

## Requirements

- Python 3.x
- `pymongo` library
- `pandas` library

## Installation

First, you need to install the required Python libraries. You can do this using pip:

```bash
pip install pymongo pandas
```

## Usage
The script accepts the following arguments:

- folder_path: Path to the folder containing CSV files (required).
- mongo_host: MongoDB host (required).
- -P or --port: MongoDB port (optional, default is 27017).
- -p or --password: MongoDB password (optional).

### Example Commands

Without password and port (using default port 27017):
```bash
python mongo_collection_from_csv.py /path/to/csv/folder localhost
```

With password and port:
```bash
python mongo_collection_from_csv.py /path/to/csv/folder localhost -P 27017 -p mypassword
```

## Script Description
The script performs the following steps:

1. Extract Database Name: The database name is derived from the folder name containing the CSV files.
2. Build MongoDB URI: Constructs the MongoDB URI using the host and port.
3. Establish MongoDB Connection: Connects to the MongoDB instance using the provided credentials.
4. Iterate Through CSV Files: For each CSV file in the folder:
   - The collection name is derived from the CSV file name.
   - The CSV file is read into a DataFrame.
   - The DataFrame is converted to a dictionary and inserted into the corresponding MongoDB collection.
5. Close MongoDB Connection: Closes the connection to MongoDB.

