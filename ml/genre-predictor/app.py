from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pickle
import os
import json

# Get the directory where this app.py is located
app_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(app_dir, 'templetes')

app = Flask(__name__, template_folder=template_dir)

# Configure CORS for production and local development
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173", "https://*.netlify.app"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# MongoDB Connection
# For local MongoDB: mongodb://localhost:27017
# For MongoDB Atlas: mongodb+srv://username:password@cluster.mongodb.net/database
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = "genre_predictor"
MONGO_COLLECTION = "predictions"

try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    mongo_client.admin.command('ping')
    db = mongo_client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    print("[OK] MongoDB connected successfully")
except Exception as e:
    print(f"[WARNING] MongoDB not available: {e}")
    print("Tip: Working in offline mode without database storage")
    db = None
    collection = None

# Load model from the same directory
model_path = os.path.join(app_dir, "genre_model.pkl")
vectorizer_path = os.path.join(app_dir, "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["text"]
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    
    # Store in MongoDB if available
    if collection is not None:
        collection.insert_one({
            "text": text,
            "prediction": prediction,
            "timestamp": datetime.utcnow()
        })
    
    return render_template("index.html", result=prediction)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        # Get text from form data
        text = request.form.get("text", "").strip()
        
        print(f"DEBUG: Received text: '{text}'")
        
        if not text:
            return jsonify({"error": "No text provided", "success": False}), 400
        
        # Vectorize and predict
        vec = vectorizer.transform([text])
        prediction = model.predict(vec)[0]
        
        print(f"DEBUG: Prediction result: {prediction}")
        
        # Store in MongoDB if available
        prediction_record = {
            "text": text,
            "prediction": prediction,
            "timestamp": datetime.utcnow()
        }
        
        if collection is not None:
            result = collection.insert_one(prediction_record)
            prediction_record["_id"] = str(result.inserted_id)
        
        return jsonify({"result": prediction, "success": True})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "success": False}), 500

@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        if collection is None:
            return jsonify({"error": "Database not available", "history": []}), 503
        
        limit = request.args.get("limit", 20, type=int)
        history = list(collection.find().sort("timestamp", -1).limit(limit))
        
        # Convert ObjectId to string and format timestamps
        for record in history:
            record["_id"] = str(record["_id"])
            record["timestamp"] = record["timestamp"].isoformat()
        
        return jsonify({"history": history, "success": True})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        if collection is None:
            return jsonify({"error": "Database not available", "stats": {}}), 503
        
        total_predictions = collection.count_documents({})
        
        # Count by genre
        pipeline = [
            {"$group": {"_id": "$prediction", "count": {"$sum": 1}}}
        ]
        genre_counts = list(collection.aggregate(pipeline))
        
        stats = {
            "total_predictions": total_predictions,
            "genre_distribution": {item["_id"]: item["count"] for item in genre_counts}
        }
        
        return jsonify({"stats": stats, "success": True})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == "__main__":
    app.run(debug=True)