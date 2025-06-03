from sklearn.model_selection import cross_val_predict
from sklearn.tree import DecisionTreeClassifier

from utils import results


def DT(hyperparameters, X_train, X_test, y_train, criterion,  max_depth, max_features, min_samples_leaf, random_state):

    if(hyperparameters==False):
        classifier = DecisionTreeClassifier(random_state=random_state)#, class_weight='balanced'

    else:
        classifier = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth, max_features=max_features, min_samples_leaf=min_samples_leaf,random_state=random_state)

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    #y_predictions = cross_val_predict(classifier, X, y, cv=5, method='predict')
    #y_predictions_proba = cross_val_predict(classifier, X, y, cv=5, method='predict_proba')
    return y_predictions, y_predictions_proba, classifier
