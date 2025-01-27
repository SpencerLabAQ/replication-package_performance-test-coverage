from sklearn.neighbors import KNeighborsClassifier

from utils import results


def kNN(X_train, X_test, y_train, algorithm, leaf_size, metric, n_neighbors, weights):

    if(n_neighbors!=None):
        classifier = KNeighborsClassifier(algorithm=algorithm, leaf_size=leaf_size, metric=metric, n_neighbors=n_neighbors, weights=weights)
    else:
        classifier = KNeighborsClassifier()

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier