from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree 

data = datasets.load_wine(as_frame=True)

X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=22)


clf = BaggingClassifier(n_estimators=12, oob_score=True, random_state=22)
clf.fit(X_train, y_train)

plt.figure(figsize=(30, 20))

plot_tree(clf.estimators_[0])
plt.show()
# oob_model = BaggingClassifier(n_estimators=12, oob_score=True, random_state=22)
# oob_model.fit(X_train, y_train)

# print(f"OOB Score: {oob_model.oob_score_:.2f}")

# dtree = DecisionTreeClassifier(random_state=22)
# dtree.fit(X_train, y_train)

# y_pred = dtree.predict(X_test)

# print(f"Train data Accuracy: {accuracy_score(y_true=y_train, y_pred=dtree.predict(X_train)):.2f}")
# print(f"Test data Accuracy: {accuracy_score(y_true=y_test, y_pred=y_pred):.2f}")

# estimator_range = [2,4,6,8,10,12,14,16]

# models = []
# scores = []

# for n_estimators in estimator_range:
#     clf = BaggingClassifier(n_estimators=n_estimators, random_state=22)
#     clf.fit(X_train, y_train)
    
#     models.append(clf)
#     scores.append(accuracy_score(y_true=y_test, y_pred=clf.predict(X_test)))

# plt.figure(figsize=(9, 6))
# plt.plot(estimator_range, scores)
# plt.xlabel("Number of Estimators", fontsize=18)
# plt.ylabel("Accuracy", fontsize=18)
# plt.tick_params(labelsize=16)

# plt.show()
