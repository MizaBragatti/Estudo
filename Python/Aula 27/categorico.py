import pandas as pd
from sklearn.linear_model import LinearRegression

cars = pd.read_csv(r'c:\\Users\\Miza\\Documents\\Estudo\\Python\\Aula 27\\data.csv')

ohe_cars = pd.get_dummies(cars[['Car']])

X = pd.concat([cars[['Volume', 'Weight']], ohe_cars], axis=1)
y = cars['CO2']

regr = LinearRegression()
regr.fit(X, y)

novo_dado = pd.DataFrame([[2300, 1300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]], columns=X.columns)
predictCO2 = regr.predict(novo_dado)
print(predictCO2)