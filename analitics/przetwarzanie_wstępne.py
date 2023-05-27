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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
import imblearn
from sklearn.datasets import make_classification
from imblearn.over_sampling import RandomOverSampler

np.random.seed(0)
# %% Ładowanie danych

data = pd.read_csv("C:/Users/mlado/Desktop/wyniki_git1.csv")
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(axis=0, inplace=True)

#data = data[data["competitor_age"]>=13]
data.loc[data["competitor_age"] < 13, "yoyo_vo2max"] *= 1.004


# Kolumny z wynikami
y_vals = data.loc[:, ["yoyo_level", "yoyo_dist", "yoyo_vo2max", "yoyo_training_load"]]

# odrzucenie z X kolumn z wynikami oraz informacjami osobistymi
data.drop(["Unnamed: 0", "competitor_foldername", "competitor_age","yoyo_level", "yoyo_dist", "yoyo_vo2max", "yoyo_training_load"], axis=1, inplace=True)


# stworzenie rang
y_ranked = []
dictionary_of_ranks = {"0": [0, 35],
                        "1": [35, 38.4],
                        "2": [38.4, 45.2],
                        "3": [45.2, 51],
                        "4": [51, 60],
                        "5": [60, 100]}

"""dictionary_of_ranks = {"0": [0, 51],
                        "1": [51, 100]}"""

for value in y_vals["yoyo_vo2max"]:
    for class_key, class_range in dictionary_of_ranks.items():
        if class_range[0] <= value < class_range[1]:
            y_ranked.append(int(class_key))
            break

#plt.hist(y_ranked)
plt.hist(y_ranked, bins=[0, 1, 2, 3, 4, 5, 6], range=[0,6], align='left', edgecolor='black')
plt.xlabel('Grupa')
plt.ylabel('Częstość występowania')
plt.title('Histogram przedstawiający rozkład rang')
# %%
r = np.corrcoef(y_vals["yoyo_dist"], y_vals["yoyo_vo2max"])
"""young = age[age["competitor_age"] < 13]
young_above_5 = len(young[young["yoyo_ranked"] == 5])
young_under_5 = len(young[young["yoyo_ranked"] < 5])

teen = age[age["competitor_age"]>=13]
teen_above_5 = len(teen[teen["yoyo_ranked"] == 5])
teen_under_5 = len(young[young["yoyo_ranked"] <5])"""

# %%
# imputacja wartości brakujących
"""imputer = KNNImputer(n_neighbors=3)
data_transformed = imputer.fit_transform(data)"""
hrv_cols = [col for col in data.columns if 'HRV' in col]
rrv_cols = [col for col in data.columns if 'RRV' in col]
imputed = pd.DataFrame(data, columns=hrv_cols)

ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(imputed, y_ranked)
# %%
# Dobór cech do uczenia
gb = GradientBoostingClassifier(n_estimators=500, learning_rate=0.1,
                max_depth=1, random_state=0).fit(X_res, y_res)
selector = RFECV(gb, step=1, cv=2)
selector = selector.fit(X_res, y_res)
# %%
number_of_features = 10
sel_idxs = np.argpartition(selector.ranking_, number_of_features)[:number_of_features]
data_sel = data.iloc[:, sel_idxs]
data_sel = data

# %%
skf = StratifiedKFold(n_splits=10)
skf.get_n_splits(X_res, y_res)

for i, (train_index, test_index) in enumerate(skf.split(X_res, y_res)):
    X_train = X_res.iloc[train_index, :]
    y_train = np.array(y_res)[train_index]
    X_test = X_res.iloc[test_index, :]
    y_test = np.array(y_res)[test_index]

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_pred_random_forest = rf.predict(X_test)
    CM = confusion_matrix(y_test, y_pred_random_forest)
    print(CM)
    print("Fold: ", i)
    accuracy = accuracy_score(y_test, y_pred_random_forest)
    print("accuracy: ", accuracy)
    prec = precision_score(y_test, y_pred_random_forest)
    print("precision", prec)
    rec = recall_score(y_test, y_pred_random_forest)
    print("recall", rec)

# %% podział na dane treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(data_sel, y_ranked, test_size=0.3, random_state=0, stratify=y_ranked)

# skalowanie danych
scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# %% Uczenie modeli
# las losowy
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred_random_forest = rf.predict(X_test)

# SVM
clf = svm.SVC()
clf.fit(X_train, y_train)
y_pred_svm=clf.predict(X_test)

# KNN
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train, y_train)
y_pred_neigh =neigh.predict(X_test)

# GBoost
gb = GradientBoostingClassifier(n_estimators=300, learning_rate=0.1,
                max_depth=1, random_state=0).fit(X_train, y_train)

y_pred_gb = gb.predict(X_test)

# Wyniki
accuracy = accuracy_score(y_test, y_pred_random_forest)
"""prec = precision_score(y_test, y_pred_random_forest)
rec = recall_score(y_test, y_pred_random_forest)"""
print("Accuracy random forest:\nAcc:", accuracy)#, "prec:", prec, "rec: ", rec)

accuracy = accuracy_score(y_test, y_pred_svm)
"""prec = precision_score(y_test, y_pred_svm)
rec = recall_score(y_test, y_pred_svm)"""
print("Accuracy svm:\nAcc:", accuracy)#, "prec:", prec, "rec: ", rec)

accuracy = accuracy_score(y_test, y_pred_neigh)
"""prec = precision_score(y_test, y_pred_neigh)
rec = recall_score(y_test, y_pred_neigh)"""
print("Accuracy knn:\nAcc:", accuracy)#, "prec:", prec, "rec: ", rec)

accuracy = accuracy_score(y_test, y_pred_gb)
"""prec = precision_score(y_test, y_pred_gb)
rec = recall_score(y_test, y_pred_gb)"""
print("Accuracy gb:\nAcc:", accuracy)#, "prec:", prec, "rec: ", rec)

# %%