# %%
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import datasets, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.feature_selection import RFECV
from sklearn.svm import SVR
import random

random.seed(0)



data = pd.read_csv("C:/Users/mlado/Desktop/yoyo_data.csv")

data = data.dropna(axis=0)

age = data.loc[:, ["yoyo_level", "competitor_age"]]

#data = data[data["competitor_age"]>=13]
data.loc[data["competitor_age"] < 13, "yoyo_level"] *= 1.0048


y_vals = data.loc[:, ["yoyo_level", "yoyo_dist", "yoyo_vo2max", "yoyo_training_load"]]

data.drop(["Unnamed: 0", "competitor_foldername", "competitor_age","yoyo_level", "yoyo_dist", "yoyo_vo2max", "yoyo_training_load"], axis=1, inplace=True)

data.replace([np.inf, -np.inf], np.nan, inplace=True)


y_ranked = []
dictionary_of_ranks = {"0": [0, 35],
                        "1": [35, 38.4],
                        "2": [38.4, 45.2],
                        "3": [45.2, 51],
                        "4": [51, 60],
                        "5": [60, 100]}

for value in y_vals["yoyo_vo2max"]:
    for class_key, class_range in dictionary_of_ranks.items():
        if class_range[0] <= value < class_range[1]:
            y_ranked.append(int(class_key))
            break

"""young = age[age["competitor_age"] < 13]
young_above_5 = len(young[young["yoyo_ranked"] == 5])
young_under_5 = len(young[young["yoyo_ranked"] < 5])

teen = age[age["competitor_age"]>=13]
teen_above_5 = len(teen[teen["yoyo_ranked"] == 5])
teen_under_5 = len(young[young["yoyo_ranked"] <5])"""


imputer = KNNImputer(n_neighbors=2)
data_transformed = imputer.fit_transform(data)

imputed = pd.DataFrame(data_transformed, columns=data.columns)


rf = RandomForestClassifier()
selector = RFECV(rf, step=1, cv=2)
selector = selector.fit(imputed, y_ranked)


sel = imputed.columns[np.where(selector.ranking_ < 10
)[0]]
data_sel = data.loc[:, sel]

X_train, X_test, y_train, y_test = train_test_split(data_sel, y_ranked, test_size=0.3, random_state=0, stratify=y_ranked)


scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred_random_forest = rf.predict(X_test)
clf = svm.SVC()

clf.fit(X_train, y_train)
y_pred_svm=clf.predict(X_test)
"""plt.scatter(range(len(y_pred)), y_pred, color='r')
plt.scatter(range(len(y_pred)), y_test, color='g')"""

accuracy = accuracy_score(y_test, y_pred_random_forest)
print("Accuracy random forest:", accuracy)
accuracy = accuracy_score(y_test, y_pred_svm)
print("Accuracy svm:", accuracy)

# %%
# %%
