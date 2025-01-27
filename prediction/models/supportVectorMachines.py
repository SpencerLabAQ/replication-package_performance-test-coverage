from sklearn import svm
from sklearn.ensemble import BaggingClassifier

from utils import results


def SVM(X_train, X_test, y_train, kernel):

    model =svm.SVC(decision_function_shape='ovr', kernel=kernel, cache_size=20000)
    classifier = BaggingClassifier(estimator=model)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier

"""
def svmSMOTE(X_Data, Y_Data, test_size):

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier =svm.SVC(decision_function_shape='ovo')
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)

def svmUnderSampling(X_Data, Y_Data, test_size):
    rus = RandomUnderSampler(random_state=42)
    X_res, y_res = rus.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier =svm.SVC(decision_function_shape='ovo')
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)
"""