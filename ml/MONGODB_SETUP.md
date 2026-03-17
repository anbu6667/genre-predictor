# MongoDB Setup Guide for Genre Predictor

## Option 1: Local MongoDB (Easy for Development)

### Windows Installation:
1. Download MongoDB Community from: https://www.mongodb.com/try/download/community
2. Run the installer and follow the setup wizard
3. MongoDB will be installed as a Windows Service and runs automatically
4. Check if running: Open Command Prompt and type `mongosh`

### Verify MongoDB is Running:
```powershell
mongosh
```

The app will automatically connect to `mongodb://localhost:27017`

---

## Option 2: MongoDB Atlas (Cloud - Recommended for Production)

### Setup Steps:
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new project and cluster
4. Add a database user with username and password
5. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/database`

### Use with Flask:
Set the environment variable before running:

**Windows PowerShell:**
```powershell
$env:MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/genre_predictor"
c:/ml/.venv/Scripts/python.exe app.py
```

**Windows Command Prompt:**
```cmd
set MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/genre_predictor
c:/ml/.venv/Scripts/python.exe app.py
```

---

## New API Endpoints

### 1. Make a Prediction
```
POST /api/predict
Content-Type: form-data
Body: text=<movie_description>

Response: {"result": "Genre", "success": true}
```

### 2. Get Prediction History
```
GET /api/history?limit=20

Response: {"history": [...predictions...], "success": true}
```

### 3. Get Statistics
```
GET /api/stats

Response: {
  "stats": {
    "total_predictions": 42,
    "genre_distribution": {
      "Action": 12,
      "Romance": 10,
      "Sci-Fi": 8,
      ...
    }
  },
  "success": true
}
```

---

## Database Schema

**Collection: predictions**
```json
{
  "_id": "ObjectId",
  "text": "Movie description",
  "prediction": "Genre",
  "timestamp": "2026-03-17T20:15:30.123Z"
}
```

---

## Troubleshooting

**Error: "MongoDB not available"**
- Ensure MongoDB service is running
- Check MONGO_URI environment variable is correct
- The app will work offline without predictions being stored

**Connection refused**
- Make sure MongoDB service is started
- For local: `mongosh` should connect
- For Atlas: Check IP whitelist and username/password

**SSL Certificate Error (Atlas)**
- Add `&retryWrites=true` to connection string if needed

---

## Storage Behavior

- ✅ **MongoDB Available**: All predictions stored in database
- ⚠️ **MongoDB Unavailable**: Predictions work but not stored (development mode)
- All predictions include timestamp for tracking
