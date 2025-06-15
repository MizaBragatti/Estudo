import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

df = pandas.read_csv(r'c:\Users\Miza\Documents\Estudo\Python\Aula 25\data.csv')

#print(df)

d = {'UK': 0, 'USA': 1, 'N':2}
df['Nationality'] = df['Nationality'].map(d)

d = {'YES':1, 'NO':0}
df['Go'] = df['Go'].map(d)

features = ['Age', 'Experience', 'Rank', 'Nationality']

X = df[features]
y = df['Go']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

plot = tree.plot_tree(dtree, feature_names=features)

print(dtree.predict([[40, 5, 7, 1]]))
print(dtree.predict([[41, 5, 7, 1]]))
print(dtree.predict([[42, 5, 7, 1]]))
print(dtree.predict([[43, 5, 7, 1]]))
print(dtree.predict([[45, 5, 7, 1]]))
print("[1] means 'GO'")
print("[0] means 'NO'")

plt.show()


