from sklearn.naive_bayes import ComplementNB

from utils import results


def CNB(X_train, X_test, y_train, alpha):

    if (alpha != None):
        classifier = ComplementNB(alpha=alpha)
    else:
        classifier = ComplementNB()
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    y_predictions_proba = classifier.predict_proba(X_test)
    return y_predictions, y_predictions_proba, classifier

'''
def cnbSMOTE(X_Data, Y_Data, test_size, alpha):
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = ComplementNB(alpha=alpha)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)

def cnbUnderSampling(X_Data, Y_Data, test_size, alpha):
    rus = RandomUnderSampler(random_state=42)
    X_res, y_res = rus.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = ComplementNB(alpha=alpha)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)

def cnbHybrid(X_Data, Y_Data, test_size, alpha):

    rus = RandomUnderSampler(random_state=42)
    X_res, y_res = rus.fit_resample(X_Data, Y_Data)

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_res, y_res)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = ComplementNB(alpha=alpha)
    # hidden_layer_sizes = (150, 100, 50)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)'''