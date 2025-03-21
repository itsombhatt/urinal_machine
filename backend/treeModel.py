import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier
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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.16, random_state = 42)

decisionTree = DecisionTreeClassifier(random_state=42)
randomForest = RandomForestClassifier(n_estimators=100, # Number of trees to train
                       criterion='gini', # How to train the trees. Also supports entropy.
                       max_depth=None, # Max depth of the trees. Not necessary to change.
                       min_samples_split=2, # Minimum samples to create a split.
                       min_samples_leaf=0.001, # Minimum samples in a leaf. Accepts fractions for %. This is 0.1% of sample.
                       min_weight_fraction_leaf=0.0, # Same as above, but uses the class weights.
                       max_features='sqrt', # Maximum number of features per split (not tree!) by default is sqrt(vars)
                       max_leaf_nodes=None, # Maximum number of nodes.
                       min_impurity_decrease=0.0001, # Minimum impurity decrease. This is 10^-3.
                       bootstrap=True, # If sample with repetition. For large samples (>100.000) set to false.
                       oob_score=True,  # If report accuracy with non-selected cases.
                    #    n_jobs=-1, # Parallel processing. Set to -1 for all cores. Watch your RAM!!
                       random_state=42, # Seed
                       verbose=1, # If to give info during training. Set to 0 for silent training.
                       warm_start=False, # If train over previously trained tree.
                       class_weight='balanced'
                                    )
gradient = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=42)


decisionTree.fit(X_train, y_train)
print("decisionTree: ", decisionTree.score(X_test, y_test))
randomForest.fit(X_train, y_train)
print("randomForest: ", randomForest.score(X_test, y_test))
gradient.fit(X_train, y_train)
print("gradient: ", gradient.score(X_test, y_test))


bagged = BaggingClassifier(estimator=decisionTree, n_estimators=25, max_samples=1200, random_state=42)
bagged.fit(X_train, y_train)
print("bagging: ", bagged.score(X_test, y_test))