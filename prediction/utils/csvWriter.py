import csv

def write(results,fileName,kFold):

    with open(fileName, 'a+', newline='') as csvfile:
        results_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csvfile.seek(0)
        line = csvfile.readline()

        if kFold:
            if "model" not in line:
                results_writer.writerow(
                    ["experiment_name","model_name", "precision", "recall", "f1_score", "accuracy", "balanced_accuracy","auc", "mcc"])
                results_writer.writerow(results)
            else:
                results_writer.writerow(results)
        else:
            if "model" not in line:
                results_writer.writerow(["dataset_name","rfecv","autospearman","hyperparameters","features","sampling","model_name","precision","recall","f1_score","accuracy","balanced_accuracy","auc","mcc","TP","FP","TN","FN"])
                results_writer.writerow(results)
            else:
                results_writer.writerow(results)


