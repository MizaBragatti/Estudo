from sklearn import datasets
iris = datasets.load_iris()
from sklearn.linear_model import LogisticRegression

X = iris['data']
y = iris['target']

logit = LogisticRegression(max_iter=10000)

C = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
scores = []
for c in C:
    logit.set_params(C=c)
    logit.fit(X, y)
    scores.append(logit.score(X, y))

# print(logit.fit(X, y))
# print(logit.score(X, y))
print(scores)