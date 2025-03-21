import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score
import warnings 
warnings.filterwarnings('ignore')

data = pd.read_csv("backend/data.csv")
X = data.drop("position", axis=1).values
y = data.position.values

poly = PolynomialFeatures(degree=2, include_bias=True)
transformed_data = poly.fit_transform(X)
print(transformed_data.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.16, random_state = 42)

model = MLPClassifier(hidden_layer_sizes=(8,), activation='relu', solver='sgd', learning_rate='adaptive', max_iter=300)
model.fit(X_train, y_train)
scores = cross_val_score(model, X, y, cv=5)

# print(model.predict([[1,0,2,1,1]]))
print("no bagging: ", model.score(X_test, y_test))
print("cross validation score: ", scores.mean())

bagged = BaggingClassifier(estimator=model, n_estimators=50, random_state=42)
bagged.fit(X_train, y_train)
print("bagging: ", bagged.score(X_test, y_test))
