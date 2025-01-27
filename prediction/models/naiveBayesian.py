from sklearn.naive_bayes import GaussianNB

from utils import results


def NB(X_train, X_test, y_train):

    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier
