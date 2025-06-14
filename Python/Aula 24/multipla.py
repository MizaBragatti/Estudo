import pandas
from sklearn import linear_model

df = pandas.read_csv(r'c:\Users\Miza\Documents\Estudo\Python\Aula 24\data.csv')

X = df[['Weight', 'Volume']]
y = df['CO2']

regr = linear_model.LinearRegression()
regr.fit(X, y)

predictCO2 = regr.predict([[3300, 1300]])

print(predictCO2)
print(regr.coef_)