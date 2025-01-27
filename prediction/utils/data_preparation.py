from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def prepare(X_Data, Y_Data, test_size,sampling_mode):



    if (sampling_mode == "None"):
        #X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=42,
         #                                                   test_size=test_size)
        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=None, random_state=42,
                                                            test_size=test_size, shuffle=False)
    if (sampling_mode == "Over" ):

        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=42,
                                                            test_size=test_size)
        os = SMOTE(random_state=42)

        X_train, y_train = os.fit_resample(X_train, y_train)

    if (sampling_mode == "Under"):

        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=42,
                                                            test_size=test_size)

        us = RandomUnderSampler(random_state=42)

        X_train, y_train = us.fit_resample(X_train, y_train)


    print("Train size: ")
    print(len(X_train))
    print("test Size :")
    print(len(X_test))
    return X_train, X_test, y_train, y_test

def prepareOld(X_Data, Y_Data, test_size, oversampler, undersampler, sampling_mode, sample_size, threshold_sample_size):

    if (sampling_mode == "None"):
        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=1,
                                                            test_size=test_size)

    if (sampling_mode == "Over" ):

        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=1,
                                                            test_size=test_size)

        if (sample_size!=None and sample_size >= threshold_sample_size):
            os = oversampler(sample_size, random_state=42)
        else:
            os = oversampler(random_state=42)

        X_train, y_train = os.fit_resample(X_train, y_train)
        #X_test, y_test = os.fit_resample(X_test, y_test)

    if (sampling_mode == "Under"):

        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=1,
                                                            test_size=test_size)

        if (sample_size!=None and sample_size >= threshold_sample_size):
            us = undersampler(sample_size, random_state=42)
        else:
            us = undersampler(random_state=42)

        X_train, y_train = us.fit_resample(X_train, y_train)
        #X_test, y_test = us.fit_resample(X_test, y_test)


    if (sampling_mode == "Hybrid"):

        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=1,
                                                            test_size=test_size)

        if (sample_size >= threshold_sample_size):
            os = oversampler(random_state=42)
            us = undersampler(sample_size, random_state=42)
        else:
            os = oversampler(random_state=42)
            us = undersampler(random_state=42)

        X_res, y_res = us.fit_resample(X_train, y_train)

        X_train, y_train = os.fit_resample(X_res, y_res)


    print("Train size: ")
    print(len(X_train))
    print("test Size :")
    print(len(X_test))
    return X_train, X_test, y_train, y_test