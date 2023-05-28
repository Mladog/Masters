# %% Importowanie bibliotek

import numpy as np
import pandas as pd
from imblearn.over_sampling import ADASYN 
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
import csv
from db_utils import get_data_from_db
np.random.seed(0)

# %% Załadowanie danych

data = get_data_from_db()
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(axis=0, inplace=True)

# korekta wyniku VO2max dla grupy osób poniżej 13 roku życia
data.loc[data["competitor_age"] < 13, "yoyo_vo2max"] /= 1.10048

# wyodrębnienie wektora z wynikami
y_vals = data[["yoyo_vo2max"]].values

# odrzucenie z matrycy danych kolumn z wynikami oraz informacjami osobistymi
data.drop(["competitor_foldername", "competitor_age","yoyo_level", "yoyo_dist", "yoyo_vo2max", "yoyo_training_load"], axis=1, inplace=True)

# stworzenie rang
y_ranked = []
# slownik uzywany podczas klasyfikacji do wielu klas
"""dictionary_of_ranks = {"0": [0, 35],
                        "1": [35, 38.4],
                        "2": [38.4, 45.2],
                        "3": [45.2, 51],
                        "4": [51, 60],
                        "5": [60, 100]}"""

# slownik uzywany podczas klasyfikacji binarnej
dictionary_of_ranks = {"0": [0, 51],
                        "1": [51, 100]}

for value in y_vals:
    for class_key, class_range in dictionary_of_ranks.items():
        if class_range[0] <= value < class_range[1]:
            y_ranked.append(int(class_key))
            break

smote = ADASYN(random_state=42, n_neighbors=2)
X_balanced, y_balanced = smote.fit_resample(data, y_ranked)

# %% wybór danych przekazanych do uczenia modelu
hrv_cols = [col for col in data.columns if 'HRV' in col]
rrv_cols = [col for col in data.columns if 'RRV' in col]
selected_data = pd.DataFrame(X_balanced, columns=rrv_cols)

# %% Nadanie priorytetow cechom
gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1,
                max_depth=1, random_state=0).fit(selected_data, y_balanced)
selector = RFECV(gb, step=1, cv=2)
selector = selector.fit(selected_data, y_balanced)
# %% Wybór cech przekazanych do uczenia według priorytetu
number_of_features = 10
sel_idxs = np.argpartition(selector.ranking_, number_of_features)[:number_of_features]
data_sel = selected_data.iloc[:, sel_idxs]
data_sel = selected_data

# %% Sprawdzenie wyników klasyfikacji
skf = StratifiedKFold(n_splits=10)
skf.get_n_splits(data_sel, y_balanced)

results = []
results.append(["Model", "Mean Accuracy", "Mean Recall", "Mean Precision"])
#results.append(["Model", "Mean Accuracy", "Mean F1"])

f1 = []
acc = []
prec = []
rec = []
for i, (train_index, test_index) in enumerate(skf.split(data_sel, y_balanced)):
    X_train = data_sel.iloc[train_index, :]
    y_train = np.array(y_balanced)[train_index]
    X_test = data_sel.iloc[test_index, :]
    y_test = np.array(y_balanced)[test_index]

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_pred_random_forest = rf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred_random_forest)
    acc.append(accuracy)
    p= precision_score(y_test, y_pred_random_forest)
    prec.append(p)
    r = recall_score(y_test, y_pred_random_forest)
    rec.append(r)

    """ #print("Fold: ", i)
    accuracy = accuracy_score(y_test, y_pred_random_forest)
    acc.append(accuracy)
    #print("accuracy: ", accuracy)
    f1_res = f1_score(y_test, y_pred_random_forest, average='macro')
    f1.append(f1_res)
    #print("f1_score", f1_res)"""

#results.append(["Random Forest", np.mean(acc), np.mean(f1)])
results.append(["Random Forest", np.mean(acc), np.mean(rec), np.mean(prec)])

#print("mean acc rf: ", np.mean(acc))
#print("mean recall rf:", np.mean(rec))
#print("mean prec rf:", np.mean(prec))
#print("mean f1 rf: ", np.mean(f1))

f1 = []
acc = []
prec = []
rec = []
for i, (train_index, test_index) in enumerate(skf.split(data_sel, y_balanced)):
    X_train = data_sel.iloc[train_index, :]
    y_train = np.array(y_balanced)[train_index]
    X_test = data_sel.iloc[test_index, :]
    y_test = np.array(y_balanced)[test_index]

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf = svm.SVC()
    clf.fit(X_train, y_train)
    y_pred_svm=clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred_svm)
    acc.append(accuracy)
    p= precision_score(y_test, y_pred_svm)
    prec.append(p)
    r = recall_score(y_test, y_pred_svm)
    rec.append(r)


    """#print("Fold: ", i)
    accuracy = accuracy_score(y_test, y_pred_svm)
    acc.append(accuracy)
    #print("accuracy: ", accuracy)
    f1_res = f1_score(y_test, y_pred_svm, average='macro')
    f1.append(f1_res)
    #print("f1_score", f1_res)"""

"""print("mean acc svm: ", np.mean(acc))
print("mean recall svm:", np.mean(rec))
print("mean prec svm:", np.mean(prec))"""
#print("mean f1 svm: ", np.mean(f1))
#results.append(["SVM", np.mean(acc), np.mean(f1)])
results.append(["SVM", np.mean(acc), np.mean(rec), np.mean(prec)])

f1 = []
acc = []
prec = []
rec = []
for i, (train_index, test_index) in enumerate(skf.split(data_sel, y_balanced)):
    X_train = data_sel.iloc[train_index, :]
    y_train = np.array(y_balanced)[train_index]
    X_test = data_sel.iloc[test_index, :]
    y_test = np.array(y_balanced)[test_index]

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X_train, y_train)
    y_pred_neigh =neigh.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred_neigh)
    acc.append(accuracy)
    p= precision_score(y_test, y_pred_neigh)
    prec.append(p)
    r = recall_score(y_test, y_pred_neigh)
    rec.append(r)
    

    """#print("Fold: ", i)
    accuracy = accuracy_score(y_test, y_pred_neigh)
    acc.append(accuracy)
    #print("accuracy: ", accuracy)
    f1_res = f1_score(y_test, y_pred_neigh, average='macro')
    f1.append(f1_res)
    #print("f1_score", f1_res)"""
"""print("mean acc KNN: ", np.mean(acc))
print("mean recall KNN:", np.mean(rec))
print("mean prec KNN:", np.mean(prec))"""
#print("mean f1 KNN: ", np.mean(f1))
#results.append(["KNN", np.mean(acc), np.mean(f1)])
results.append(["KNN", np.mean(acc), np.mean(rec), np.mean(prec)])


f1 = []
acc = []
prec = []
rec = []
for i, (train_index, test_index) in enumerate(skf.split(data_sel, y_balanced)):
    X_train = data_sel.iloc[train_index, :]
    y_train = np.array(y_balanced)[train_index]
    X_test = data_sel.iloc[test_index, :]
    y_test = np.array(y_balanced)[test_index]

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,
                max_depth=1, random_state=0).fit(X_train, y_train)

    y_pred_gb = gb.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred_gb)
    acc.append(accuracy)
    p= precision_score(y_test, y_pred_gb)
    prec.append(p)
    r = recall_score(y_test, y_pred_gb)
    rec.append(r)

    """#print("Fold: ", i)
    accuracy = accuracy_score(y_test, y_pred_gb)
    acc.append(accuracy)
    #print("accuracy: ", accuracy)
    f1_res = f1_score(y_test, y_pred_gb, average='macro')
    f1.append(f1_res)
    #print("f1_score", f1_res)"""

#print("mean acc gb: ", np.mean(acc))
#print("mean recall gb:", np.mean(rec))
#print("mean prec gb:", np.mean(prec))
#print("mean f1 gb: ", np.mean(f1))
#results.append(["Gradient Boosting", np.mean(acc), np.mean(f1)])
results.append(["Gradient Boosting", np.mean(acc), np.mean(rec), np.mean(prec)])

output_file = "results.csv"

# Write the results to the CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(results)

# Print a message to confirm the saving of results
print("Results saved to:", output_file)

# %%