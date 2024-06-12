from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

class DecisionTree:
    def __init__(self):
        self.decision_tree = None

    def initalize_tree(self, file_path):
        df = pd.read_csv(file_path)

        categorical_features = ['continent']
        df = pd.get_dummies(df, columns=categorical_features)

        # Encoding target variable using map
        meal_mapping = {meal: code for code, meal in enumerate(df['suggested_meal'].unique())}
        df['suggested_meal'] = df['suggested_meal'].map(meal_mapping)

        X = df.drop('suggested_meal', axis=1)
        y = df['suggested_meal']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf = DecisionTreeClassifier(random_state=42)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Decision Tree accuracy: {accuracy}')
        # plt.figure(figsize=(20,10))
        # plot_tree(clf, feature_names=X.columns, class_names=list(meal_mapping.keys()), filled=True, impurity=False)
        # plt.savefig("decision_tree_misc/decision_tree.pdf", format='pdf')

        idx_to_meal_mapping = {v: k for k, v in meal_mapping.items()}

        self.decision_tree = clf
        return idx_to_meal_mapping
        
    def predict(self, data: pd.DataFrame):
        return self.decision_tree.predict(data)
