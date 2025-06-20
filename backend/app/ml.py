# app/ml.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os
import random

DATA_PATH = os.path.join(os.path.dirname(__file__), "uploads", "intents.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "chatbot_model.joblib")


pipeline = None
responses = {}

def train_model():
    global pipeline, responses
    
    df = pd.read_csv(DATA_PATH)
    X = df["text"]
    y = df["intent"]
    responses = df.groupby("intent")["response"].apply(list).to_dict()
    
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2))),
        ("clf", LogisticRegression(max_iter=800))
    ])
    pipeline.fit(X, y)
    
    joblib.dump((pipeline, responses), MODEL_PATH)
    print("Модель обучена и сохранена!")

def load_model():
    global pipeline, responses
    if pipeline is None or not responses:
        pipeline, responses = joblib.load(MODEL_PATH)

def get_ml_response(user_message):
    load_model()
    if not user_message or not isinstance(user_message, str):
        return "Пусте повідомлення. Спробуйте ще раз."
    intent = pipeline.predict([user_message])[0]
    resp_list = responses.get(intent, [])
    if resp_list:
        return random.choice(resp_list)
    else:
        return "Вибачте, я не зрозумів запитання. Спробуйте інакше!"

if __name__ == "__main__":
    train_model()
