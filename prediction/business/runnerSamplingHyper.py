from sklearn.model_selection import KFold

from business import main
from utils import data_preparation, results, featureSelection
from pathlib import Path

# Dataset definition
path = Path(__file__).parent.parent
dataset = str(path)+"/data/metrics_combined_all_28_02_2024-28.csv"
print(dataset)

#results file
result_file = "/results/resultsCV.csv"#"/results/ResultsHyperParam.csv"#FinalResultBox1
result_file = str(path)+result_file

#features
columns = []

############################# PARAMS #############################

#Train/Test size
test_size = 0.2 #20% test 80% train

#Random State
random_state = 42

#Models
#models = ["DT"]
#models = ["DT","RF","kNN"]
models = ["RF", "ADA", "MLP", "DT", "kNN", "LR", "GB", "HGB", "LDA", "CNB", "NB"]

##### Sampling #####
sampling_mode = ["None","Over","Under"] #["None","Over","Under"]Under/Over/None
#sampling_mode = ["None"]

##### HyperParameter #####
#hyperparameters = []
hyperparameters = True

##### AutoSpearman #####
autoSpearman = False

##### RFECV Feature Selection #####
featureSelectionVar = False

#experiment_name = "nofold-newDataset-Ablation_removedNameLen-OverSampling-noAutospearman" #possbily as a result of append of different parameters


############################# RUN #############################

##### Data Preparation #####
#LOADING Data From CSV
X_Data, Y_Data = main.dataLoadingPandas(dataset, columns)

##### Auto SpearMan #####
if(autoSpearman):
    X_Data = featureSelection.autoSpearman(X_Data)
    #print(X_Data.columns)

##### Feature Selection RFECV #####
if(featureSelectionVar):
    columns = featureSelection.rfecv(X_Data, Y_Data)
    #print(columns)
    #### Reloading Data with a different set of features####
    X_Data, Y_Data = main.dataLoadingPandas(dataset, columns)

configuration = [dataset.split("/")[-1], featureSelectionVar, autoSpearman, hyperparameters, str(len(X_Data.columns))]


###### Ignition ######
for sMode in sampling_mode:

    #TRAIN-TEST-SPLIT
    x_Train, x_Test, y_Train, y_Test = data_preparation.prepare(X_Data, Y_Data, test_size, sMode)

    #experiment name
    #experiment_name = "noFold"+"-"+dataset.split("/")[-1]+"-"+"FeatureAnalysis:"+str(featureSelectionVar)+"-"+"FeaturesConsidered:"+str(len(columns))+"-"+sMode+"-"+str(hyperparameters)+"-"+"AutoSpearman:"+str(autoSpearman)

##### Prediction ######

    for model in models:
        y_test, y_predictions, y_predictions_proba, model_name = main.predict(X_Data, Y_Data, model,
                                                                                  hyperparameters, x_Train,
                                                                                  x_Test, y_Train, y_Test, random_state)
        try:
            y_test, y_predictions, y_predictions_proba, model_name = main.predict(X_Data, Y_Data, model, hyperparameters, x_Train,
                                                                                  x_Test, y_Train, y_Test, random_state)
            ##### Display Data #####
            results.display(y_test, y_predictions, y_predictions_proba, model_name, result_file, configuration, sMode)
        except:
            print("exception")


        #results.displayKFold(y_test, y_predictions, y_predictions_proba, model_name, result_file, configuration, sMode)

