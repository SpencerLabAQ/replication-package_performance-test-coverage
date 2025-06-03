from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler

from utils import results


def net(X_train, X_test, y_train, randomState):

    classifier = MLPClassifier(max_iter=100000, random_state=randomState)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier
