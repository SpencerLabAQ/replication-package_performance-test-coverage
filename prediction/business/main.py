from models import neuralNet, decisionTree, linearRegression, linearDiscriminantAnalysis, gradientBoosting, randomForest, complementNaiveBayesian, naiveBayesian, supportVectorMachines, kneighbor, adaBoost
import pandas as pd
import numpy as np

from utils import shapCalculator


def dataLoadingPandas(dataset, columns):

    if(dataset == 'data/metrics_combined_all-05-12-2023.csv'):
        columns = ["methodScope", "isOverloaded", "methodLoc", "#for", "#while", "#do", "#nestedLoops", "#if", "#switch", "#case", "#return", "#throw", "#catch", "cyclo", "#vars", "#methodCalls",
             "#internalCalls", "#externalCalls", "#cPkgClasses", "cIsAbstract", "cNestingLevel", "#cImports", "#cNativeImports", "classLOC", "#cMethods", "#cInherits", "#cImplements", "usesConcurrency", "usesCollection", "isBenchmarked"]

    else:
        columns_default = ["methodScope","nameLen", "isOverloaded", "methodLoc", "#for", "#while", "#do", "#nestedLoops", "#if", "#switch", "#case", "#return", "#throw", "#catch", "cyclo", "#vars", "#methodCalls",
                   "#internalCalls", "#externalCalls", "usesJavaUtil", "usesJavaLangThread", "usesJavaUtilConcurrent", "usesJavaIo", "usesJavaNio", "usesJavaNioChannels", "usesJavaNioFile", "usesJavaNioCharset" ,"usesJavaNet",
        "usesJavaxNetSsl", "usesJavaLang", "usesJavaLangManagement", "usesJavaUtilRegex", "usesJavaText", "usesJavaMath", "#cPkgClasses","classScope", "cIsAbstract", "cNestingLevel", "#cImports", "#cNativeImports", "classLOC", "#cMethods", "#cInherits", "#cImplements", "isBenchmarked"]

    if(len(columns)>0):
        columns = np.append(columns, "isBenchmarked")#columns.append(["isBenchmarked"])
        print(columns)
        Scopes = {'public': '1', 'protected': '2', 'private': '3', 'default': '4'}
        df = pd.read_csv(dataset, usecols=columns)
        if('methodScope' in columns):
            df['methodScope'] = df['methodScope'].map(Scopes)
        if('classScope' in columns):
            df['classScope'] = df['classScope'].map(Scopes)

    else:
        Scopes = {'public': '1', 'protected': '2', 'private': '3', 'default': '4'}
        df = pd.read_csv(dataset, usecols=columns_default)
        df['methodScope'] = df['methodScope'].map(Scopes)
        df['classScope'] = df['classScope'].map(Scopes)

    #df.fillna(method='ffill', inplace=True)
    #df.fillna(value=1.0, inplace=True)

    Y_Data = df['isBenchmarked']
    X_Data = df.drop(columns='isBenchmarked')
    print(X_Data.count())
    #X_Data.fillna(method='ffill', inplace=True)
    #Y_Data.fillna(method='ffill', inplace=True)


    print("Composition: ")
    print(Y_Data.count())
    print(Y_Data.value_counts())
    print(Y_Data.unique())

    return X_Data, Y_Data, df

def predict(model, hyperparameters, X_train, X_test, y_train, y_test, random_state, SHAP):

    print("#############")
    print("#############")
    print("TESTING " + model)
    print("#############")
    print("#############")


    if(model=="MLP"):
    # Multi Layer Perceptron
        y_predictions, y_predictions_proba, classifier = neuralNet.net(X_train, X_test, y_train, random_state)

    if(model=="DT"):

        if (hyperparameters):
            criterion = "entroy"
            max_depth = None
            max_features = None
            min_samples_leaf = 1
        else:
            criterion = None
            max_depth = None
            max_features = None
            min_samples_leaf = None
        y_predictions, y_predictions_proba, classifier = decisionTree.DT(hyperparameters, X_train, X_test, y_train, criterion, max_depth, max_features, min_samples_leaf, random_state)

    if(model=="LR"):
        y_predictions, y_predictions_proba, classifier = linearRegression.LR(X_train, X_test, y_train, random_state)

    if(model=="LDA"):
        y_predictions, y_predictions_proba, classifier = linearDiscriminantAnalysis.LDA(X_train, X_test, y_train)

    if(model=="GB"):
        y_predictions, y_predictions_proba, classifier = gradientBoosting.GB(X_train, X_test, y_train, random_state)

    if(model=="HGB"):
        y_predictions, y_predictions_proba, classifier = gradientBoosting.HGB(X_train, X_test, y_train, random_state)

    if(model=="RF"):
    # Random Forest
    #
        if(hyperparameters):
            max_depth = None
            max_features = 'sqrt'
            min_sample_leaf = 1
            n_estimators = 2000
        else:
            max_depth = None
            max_features = None
            min_sample_leaf = None
            n_estimators = None

        y_predictions, y_predictions_proba, classifier = randomForest.rf(hyperparameters, X_train, X_test, y_train, max_depth, n_estimators, max_features, min_sample_leaf, random_state)

    if(model=="CNB"):
    #Complement Naive Bayesian Network
    #
        if(hyperparameters):
            alpha = 0.5
        else:
            alpha = None

        y_predictions, y_predictions_proba, classifier = complementNaiveBayesian.CNB(X_train, X_test, y_train, alpha)

    if(model=="NB"):
    #Gaussian Naive Bayesian Network
    #
        y_predictions, y_predictions_proba, classifier = naiveBayesian.NB(X_train, X_test, y_train)

    if(model=="SVM"):
    # Support Vector Machines
    #
        kernel = "linear" #rbf
        y_predictions, y_predictions_proba, classifier = supportVectorMachines.SVM(X_train, X_test, y_train, kernel)

    if(model=="kNN"):
    # k-nearest neighbor
    #
        if(hyperparameters):
            algorithm = "kd_tree"
            leaf_size = 35
            metric = "minkowski"
            n_neighbors = 1
            weights = "distance"
        else:
            algorithm = None
            leaf_size = None
            metric = None
            n_neighbors = None
            weights = None

        y_predictions, y_predictions_proba, classifier = kneighbor.kNN(hyperparameters, X_train, X_test, y_train, algorithm, leaf_size, metric, n_neighbors, weights)

    if(model=="ADA"):
    # ADABoost
    #
        y_predictions, y_predictions_proba, classifier = adaBoost.ada(X_train, X_test, y_train, random_state)

    if(SHAP):
        shapCalculator.calculateShap(classifier,X_test)

    return y_test, y_predictions, y_predictions_proba, model