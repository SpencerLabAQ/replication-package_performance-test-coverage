from sklearn.ensemble import RandomForestClassifier

import numpy as np

def rf(hyperparameters, X_train, X_test, y_train, max_depth, n_estimators, max_features, min_sample_leaf, random_state):

    if(hyperparameters==False):
        classifier = RandomForestClassifier(random_state=random_state)
    else:
        classifier = RandomForestClassifier(max_depth=max_depth, random_state=random_state, n_estimators=n_estimators, max_features=max_features, min_samples_leaf=min_sample_leaf)

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)

    return y_predictions, y_predictions_proba, classifier

