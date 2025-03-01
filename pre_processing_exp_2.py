# -*- coding: utf-8 -*-
"""pre-processing-exp-2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SrzLzdCu38tccIje10D8eXYA0npuakiK

# New Section
"""

import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np

def preprocess_data(data, target_column, k_best=5):
    # Indent all lines within the function body
    X = data.drop(target_column, axis=1)
    y = data[target_column]
    if not np.issubdtype(y.dtype, np.number):
        y = pd.Categorical(y).codes
    selector = SelectKBest(f_classif, k=k_best)
    X_new = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()]
    X = pd.DataFrame(X_new, columns=selected_features)
    imputer = SimpleImputer(strategy='mean')
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    discretizer = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')
    try:
        X = pd.DataFrame(discretizer.fit_transform(X), columns=X.columns)
    except ValueError as e:
        print(f"Discretization Error: {e}")
        return None
    for col in X.columns:
        Q1 = X[col].quantile(0.25)
        Q3 = X[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        X = X[(X[col] >= lower_bound) & (X[col] <= upper_bound)]
        y = y[X.index]
    processed_data = pd.concat([X.reset_index(drop=True), y.reset_index(drop=True)], axis=1)
    return processed_data

data = pd.read_csv("/content/breast_cancer.csv")
preprocessed_data = preprocess_data(data, "Class")
if preprocessed_data is not None:
    print(preprocessed_data.info())
    print(preprocessed_data.head())
else:
    print("Preprocessing failed due to errors.")