import pandas
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

df = pandas.read_csv(r'c:\Users\Miza\Documents\Estudo\Python\Aula 25\data.csv')

test_data = [
    [40, 5, 7, 1],
    [41, 5, 7, 1],
    [42, 5, 7, 1],
    [43, 5, 7, 1],
    [45, 5, 7, 1]
]

d = {'UK': 0, 'USA': 1, 'N':2}
df['Nationality'] = df['Nationality'].map(d)

d = {'YES':1, 'NO':0}
df['Go'] = df['Go'].map(d)

features = ['Age', 'Experience', 'Rank', 'Nationality']

X = df[features]
y = df['Go']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

test_df = pandas.DataFrame(test_data, columns=features)
print(dtree.predict(test_df))

print("[1] means 'GO'")
print("[0] means 'NO'")

plt.show()