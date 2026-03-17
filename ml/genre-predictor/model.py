import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

# Get the directory where this model.py is located
model_dir = os.path.dirname(os.path.abspath(__file__))

# load dataset
dataset_path = os.path.join(model_dir, "dataset.csv")
data = pd.read_csv(dataset_path)

X = data["text"]
y = data["genre"]

# convert text to numbers
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# train model
model = MultinomialNB()
model.fit(X_vec, y)

# save model with absolute paths
model_path = os.path.join(model_dir, "genre_model.pkl")
vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")

pickle.dump(model, open(model_path, "wb"))
pickle.dump(vectorizer, open(vectorizer_path, "wb"))

print("Model trained successfully!")