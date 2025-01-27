from sklearn.ensemble import AdaBoostClassifier

from utils import results


def ada(X_train, X_test, y_train, randomState):

    classifier = AdaBoostClassifier(random_state=randomState)

    classifier.fit(X_train, y_train)
    y_predictions_proba = classifier.predict_proba(X_test)
    y_predictions = classifier.predict(X_test)
    return y_predictions, y_predictions_proba, classifier
