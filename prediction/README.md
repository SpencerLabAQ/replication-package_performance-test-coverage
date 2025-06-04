# In this folder you will find the scripts we used for the prediction

## Requirements
- Python 3.10.5
- [Additional dependencies are listed in the `requirements.txt` file](requirements.txt)

## Folders Structure
-   business: contains the python scripts to start the prediction
-   data: contains the data we used to train and test. Since we used the built-in train-test-split function of scikit-learn, we just stored one single data file
-   models: contains the implementations of the models
-   results: will store the results of the evaluation
-   utils: utilities for the execution

## How to run
For the reader's convenience we created several running scripts. Therefore, the only required command will be:
```
python business/runner*.py
```

Inside the folder you will find several scripts:
-  runnerModelsOnly.py - this script will run the set of models without sampling, feature analysis and hyperparameters
-  runnerSampling.py - this script will run the set of models with sampling and without feature analysis and hyperparameters
-  runnerSamplingAuto.py - this script will run the set of models with sampling and with only the RFECV feature analysis and without hyperparameters
-  runnerSamplingHyper.py - this script will run the set of models with sampling and  with hyperparameters and without feature analysis
-  runnerSamplingRFECV.py - this script will run the set of models with sampling and with only the AutoSpearman feature analysis and without hyperparameters
-  runner5Fold.py - 5 Fold version of the runnerSamplingAuto, in this configuration we are considering the evaluation of the whole set of models without any modification
-  runnerSHAP.py - this script will run the SHAP analysis for this configuration: Decision Tree, No Sampling, No Feature, No Hyperparameters. You can select a different model to study the features, but consider that elapsed time will change as well as the results.

If needed, the combination of the analysis can be arranged as the reader wishes.
Inside the generic runner*.py file you can edit the lines from 24 to 50.
Changing the parameters to True or False, ore removing the sampling techniques or the list of models.
Pay attention that some models may require more time / resources depending on the testing machines


in case of module not found try the following command
```
PYTHONPATH=. python business/runner*.py
```
