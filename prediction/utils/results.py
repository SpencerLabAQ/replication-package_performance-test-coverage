from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report, confusion_matrix
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, precision_score, recall_score, roc_auc_score, balanced_accuracy_score
from utils import csvWriter

def display(y_test, y_predictions, y_predictions_proba, model_name, fileName, configuration, sMode):

    y_predictions_proba = y_predictions_proba[:, 1]
    TN, FP, FN, TP = confusion_matrix(y_test, y_predictions).ravel()


    bal_acc = balanced_accuracy_score(y_test, y_predictions)
    acc = accuracy_score(y_test, y_predictions)
    auc = roc_auc_score(y_test, y_predictions_proba)
    mcc = matthews_corrcoef(y_test, y_predictions)
    precision = precision_score(y_test, y_predictions, average='binary')
    recall = recall_score(y_test, y_predictions, average='binary')
    f1 = f1_score(y_test, y_predictions, average='binary')

    resultsArray = configuration+[sMode,model_name,precision,recall,f1,acc,bal_acc,auc,mcc,TP,FP,TN,FN]

    csvWriter.write(resultsArray,fileName,kFold=False)

def displayKFold(y_test, y_predictions, y_predictions_proba, model_name, fileName, configuration, sMode):
    y_predictions_proba = y_predictions_proba[:, 1]
    TN, FP, FN, TP = confusion_matrix(y_test, y_predictions).ravel()


    bal_acc = balanced_accuracy_score(y_test, y_predictions)
    acc = accuracy_score(y_test, y_predictions)
    auc = roc_auc_score(y_test, y_predictions_proba)
    mcc = matthews_corrcoef(y_test, y_predictions)
    precision = precision_score(y_test, y_predictions, average='binary')
    recall = recall_score(y_test, y_predictions, average='binary')
    f1 = f1_score(y_test, y_predictions, average='binary')

    resultsArray = configuration+[sMode,model_name,precision,recall,f1,acc,bal_acc,auc,mcc,TP,FP,TN,FN]

    csvWriter.write(resultsArray,fileName,kFold=False)