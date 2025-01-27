from sklearn.linear_model import LogisticRegression

from utils import results


def LR(X_train, X_test, y_train, randomState):

    classifier = LogisticRegression(max_iter=100000, random_state=randomState)

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier