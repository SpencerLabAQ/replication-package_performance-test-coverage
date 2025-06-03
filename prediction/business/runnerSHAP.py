from sklearn.model_selection import StratifiedKFold

from business import main as business
from utils import data_preparation, results, featureSelection, kfold_print
from pathlib import Path

# Dataset definition
path = Path(__file__).parent.parent
dataset = str(path)+"/data/metrics_combined_all_28_02_2024-28.csv"
print(dataset)

#results file
result_file = "/results/results5Fold.csv"#"/results/ResultsHyperParam.csv"#FinalResultBox1
result_file = str(path)+result_file


#features
columns = []

############################# PARAMS #############################

#Train/Test size
test_size = 0.2 #20% test 80% train

#Random State
random_state = 42

#Models
models = ["DT"]
#models = ["DT","RF","kNN"]
#models = ["RF", "ADA", "MLP", "DT", "kNN", "LR", "GB", "HGB", "LDA", "CNB", "NB"]

##### Sampling #####
#sampling_mode = ["Simple","Over","Under"] #["None","Over","Under"]Under/Over/None
sampling_mode = ["Simple"]

##### kFold #####
kfold = False

##### HyperParameter #####
#hyperparameters = []
hyperparameters = False

##### AutoSpearman #####
autoSpearman = False

##### RFECV Feature Selection #####
featureSelectionVar = False

##### SHAP Feature Analysis #####
SHAP = True


############################# RUN #############################

##### Data Preparation #####
#LOADING Data From CSV
X_Data, Y_Data, datasetKfold = business.dataLoadingPandas(dataset, columns)

##### Auto SpearMan #####
if(autoSpearman):
    X_Data = featureSelection.autoSpearman(X_Data)
    print(X_Data.columns)
    X_Data, Y_Data, datasetKfold = business.dataLoadingPandas(dataset, X_Data.columns)

##### Feature Selection RFECV #####
if(featureSelectionVar):
    columns = featureSelection.rfecv(X_Data, Y_Data)
    print(columns)
    #### Reloading Data with a different set of features####
    X_Data, Y_Data, datasetKfold = business.dataLoadingPandas(dataset, columns)

##### k fold #################################################################
splits_xy = []
if kfold:
    target_column = 'isBenchmarked'

    skf = StratifiedKFold(n_splits=5,shuffle=True,random_state=42)
    for i, (train_indices, test_indices) in enumerate(skf.split(X_Data, Y_Data)):
        x_train = datasetKfold.drop(columns=target_column, axis=1).iloc[train_indices]
        y_train = datasetKfold[target_column].iloc[train_indices]
        x_test = datasetKfold.drop(columns=target_column, axis=1).iloc[test_indices]
        y_test = datasetKfold[target_column].iloc[test_indices]

        splits_xy.append((x_train, y_train, x_test, y_test))
else:
    splits_xy.append(('','','',''))

#############################################################################

configuration = [dataset.split("/")[-1], featureSelectionVar, autoSpearman, hyperparameters, str(len(X_Data.columns))]


for x_Train, y_Train, x_Test, y_Test in splits_xy: #splits_xy = 1 if not kfold
    ###### Ignition ######
    for sMode in sampling_mode:

        #TRAIN-TEST-SPLIT
        if(kfold):
            x_Train, y_Train = data_preparation.prepareKfold(x_Train, y_Train, sMode)
        else:
            x_Train, x_Test, y_Train, y_Test = data_preparation.prepare(X_Data, Y_Data, test_size, sMode)
            print(y_Test.info())

        #experiment name
        #experiment_name = "noFold"+"-"+dataset.split("/")[-1]+"-"+"FeatureAnalysis:"+str(featureSelectionVar)+"-"+"FeaturesConsidered:"+str(len(columns))+"-"+sMode+"-"+str(hyperparameters)+"-"+"AutoSpearman:"+str(autoSpearman)

    ##### Prediction ######

        for model in models:
            #y_test, y_predictions, y_predictions_proba, model_name = business.predict(model,hyperparameters, x_Train,x_Test, y_Train, y_Test, random_state)
            try:
                y_test, y_predictions, y_predictions_proba, model_name = business.predict(model, hyperparameters, x_Train,
                                                                                      x_Test, y_Train, y_Test, random_state, SHAP)
                ##### Display Data #####
                results.display(y_test, y_predictions, y_predictions_proba, model_name, result_file, configuration, sMode)
            except Exception as e:
                print(e)


            #results.displayKFold(y_test, y_predictions, y_predictions_proba, model_name, result_file, configuration, sMode)