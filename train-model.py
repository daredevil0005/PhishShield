import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils import resample
import joblib
import json

from src.url_features import extract_url_features

# Load dataset
df = pd.read_csv("dataset/phishing_data.csv")
df.columns = df.columns.str.strip().str.lower()

# Extract features from URLs
X = df['url'].apply(extract_url_features).apply(pd.Series)
y = df['label']

# Split BEFORE balancing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Balance ONLY training data
train_data = X_train.copy()
train_data['label'] = y_train

safe = train_data[train_data.label == 0]
phish = train_data[train_data.label == 1]

phish_upsampled = resample(
    phish,
    replace=True,
    n_samples=len(safe),
    random_state=42
)

balanced = pd.concat([safe, phish_upsampled])

X_train = balanced.drop(columns=['label'])
y_train = balanced['label']

# Train model
model = GradientBoostingClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4
)

model.fit(X_train, y_train)

# Evaluate on unseen data
y_pred = model.predict(X_test)

print("\n📊 Model Performance:\n")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "model/phishing_model.pkl")

# Save feature column order
with open("model/columns.json", "w") as f:
    json.dump(list(X_train.columns), f)

print("\n✅ Model trained and saved successfully!")