import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.model_selection import train_test_split
import warnings 
warnings.filterwarnings('ignore')

data = pd.read_csv("data.csv")
X = data.drop("position", axis=1).values
y = data.position.values

poly = PolynomialFeatures(degree=2, include_bias=True)
transformed_data = poly.fit_transform(X)
print(transformed_data.shape)

X_train, X_test, y_train, y_test = train_test_split(transformed_data, y, test_size=0.16, random_state = 42)

model = LogisticRegression(penalty='l2', max_iter=10000)
model.fit(X_train, y_train)
print("no bagging: ", model.score(X_test, y_test))

bagged = BaggingClassifier(estimator=model, n_estimators=50, random_state=42)
bagged.fit(X_train, y_train)
print("bagging: ", bagged.score(X_test, y_test))