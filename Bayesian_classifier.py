import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import norm

# === 1. Load column names from spambase.names ===

def load_feature_names(names_file_path):
    feature_names = []
    with open(names_file_path, 'r') as f:
        for line in f:
            if ':' in line and not line.startswith('|'):
                name = line.split(':')[0].strip()
                feature_names.append(name)
    feature_names.append('class')  # Last column is the class label
    return feature_names

# === 2. Load the data ===

feature_names = load_feature_names('C:/Users/krzys/Downloads/spambase/spambase.names')
df = pd.read_csv('C:/Users/krzys/Downloads/spambase/spambase.data', header=None, names=feature_names)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# === 3. Split into test set and train+validation set ===

X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === 4. Naive Bayes classifier with Gaussian distribution ===

class NaiveBayesGaussian:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.parameters = {}
        for cls in self.classes:
            X_cls = X[y == cls]
            self.parameters[cls] = {
                'mean': X_cls.mean(axis=0),
                'var': X_cls.var(axis=0) + 1e-6,
                'prior': X_cls.shape[0] / X.shape[0]
            }

    def predict(self, X):
        predictions = []
        for x in X:
            probs = {}
            for cls in self.classes:
                mean = self.parameters[cls]['mean']
                var = self.parameters[cls]['var']
                prior = self.parameters[cls]['prior']
                likelihood = norm.logpdf(x, loc=mean, scale=np.sqrt(var)).sum()
                probs[cls] = np.log(prior) + likelihood
            predictions.append(max(probs, key=probs.get))
        return np.array(predictions)

# === 5. Validation — random splits ===

def evaluate_random_splits(X, y, repeats=5, test_size=0.2):
    scores = []
    for i in range(repeats):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, stratify=y, random_state=i)
        model = NaiveBayesGaussian()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        scores.append([
            accuracy_score(y_val, y_pred),
            precision_score(y_val, y_pred),
            recall_score(y_val, y_pred),
            f1_score(y_val, y_pred)
        ])
    return np.array(scores)

# === 6. K-fold cross-validation ===

def evaluate_k_fold(X, y, k=5):
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
    scores = []
    for train_idx, val_idx in skf.split(X, y):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        model = NaiveBayesGaussian()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        scores.append([
            accuracy_score(y_val, y_pred),
            precision_score(y_val, y_pred),
            recall_score(y_val, y_pred),
            f1_score(y_val, y_pred)
        ])
    return np.array(scores)

# === 7. Compare validations ===

random_scores = evaluate_random_splits(X_train_val, y_train_val)
kfold_scores = evaluate_k_fold(X_train_val, y_train_val)

print("Average metrics (random split):", random_scores.mean(axis=0))
print("Standard deviations:", random_scores.std(axis=0))
print("Average metrics (k-fold validation):", kfold_scores.mean(axis=0))
print("Standard deviations:", kfold_scores.std(axis=0))

# === 8. Final model on training + validation data ===

final_model = NaiveBayesGaussian()
final_model.fit(X_train_val, y_train_val)
final_predictions = final_model.predict(X_test)

print("\nMetrics on test set:")
print("Accuracy:", accuracy_score(y_test, final_predictions))
print("Precision:", precision_score(y_test, final_predictions))
print("Recall:", recall_score(y_test, final_predictions))
print("F1 score:", f1_score(y_test, final_predictions))
