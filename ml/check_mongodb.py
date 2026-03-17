from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017')
db = client['genre_predictor']
collection = db['predictions']

# Count documents
count = collection.count_documents({})
print(f'Total predictions stored: {count}')

# Show last 5 predictions
if count > 0:
    print('\nLast 5 predictions:')
    for doc in collection.find().sort('timestamp', -1).limit(5):
        text_preview = doc['text'][:50] if len(doc['text']) > 50 else doc['text']
        print(f"  - Text: {text_preview}... -> {doc['prediction']}")
else:
    print('No predictions stored yet. Test by making predictions in the React app at http://localhost:5173')
