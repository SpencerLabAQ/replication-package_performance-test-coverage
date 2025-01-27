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

    '''
        X_Data=sc.fit_transform(X_Data)
    X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state = 1)

    classifier = MLPClassifier(max_iter=300, activation='relu', solver='adam', random_state=1)
    #hidden_layer_sizes = (150, 100, 50)
    classifier.fit(X_train, y_train)

    print(classifier.score(X_test, y_test))
    '''

def SMOTEnet(X_Data, Y_Data, test_size):
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = MLPClassifier(max_iter=20, activation='relu', solver='adam', random_state=1)

    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)
    print(accuracy_score(y_test, y_predictions))

def RoseNet(X_Data, Y_Data, test_size):
    ros = RandomOverSampler(random_state=42)
    X_res, y_res = ros.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = MLPClassifier(max_iter=20, activation='relu', solver='adam', random_state=1)
    classifier.fit(X_train, y_train)

    print(classifier.score(X_test, y_test))

    y_predictions = classifier.predict(X_test)
    print(y_predictions[50])
    print(accuracy_score(y_test, y_predictions))

def NetUnderSampled(X_Data, Y_Data, test_size):
    rus = RandomUnderSampler(random_state=42)
    X_res, y_res = rus.fit_resample(X_Data, Y_Data)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = MLPClassifier(max_iter=1000, activation='relu', solver='adam', random_state=1)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    results.display(y_test, y_predictions)

def NetHybrid(X_Data, Y_Data, test_size):
    rus = RandomUnderSampler(random_state=42)
    X_res, y_res = rus.fit_resample(X_Data, Y_Data)

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_res, y_res)

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, stratify=y_res, random_state=1, test_size=test_size)

    classifier = MLPClassifier(max_iter=1000, activation='relu', solver='adam', random_state=1)
    classifier.fit(X_train, y_train)
    y_predictions = classifier.predict(X_test)
    #    for i in range(0, len(y_test)):
    #        print(y_test[i]+" -> "+y_predictions[i])
    results.display(y_test, y_predictions)