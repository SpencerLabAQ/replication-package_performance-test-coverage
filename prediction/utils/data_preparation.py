from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def prepare(X_Data, Y_Data, test_size, sampling_mode):

    if (sampling_mode == "Simple"):
        X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=Y_Data, random_state=42,
                                                            test_size=test_size)
        #X_train, X_test, y_train, y_test = train_test_split(X_Data, Y_Data, stratify=None, random_state=42,
        #                                                    test_size=test_size, shuffle=False)
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

def prepareKfold(X_train, y_train, sampling_mode):

    if (sampling_mode == "Over"):

        os = SMOTE(random_state=42)

        X_train, y_train = os.fit_resample(X_train, y_train)

    if (sampling_mode == "Under"):

        us = RandomUnderSampler(random_state=42)

        X_train, y_train = us.fit_resample(X_train, y_train)

    return X_train, y_train