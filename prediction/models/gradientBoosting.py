from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier

from utils import results


def GB(X_train, X_test, y_train, randomState):

    classifier = GradientBoostingClassifier(random_state=randomState)

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier

def HGB(X_train, X_test, y_train, randomState):

    classifier = HistGradientBoostingClassifier(random_state=randomState)

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier