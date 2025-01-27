from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SequentialFeatureSelector, RFE, RFECV, VarianceThreshold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from utils.conf_selectors import AutoSpearmanSelector
from utils.utils import PandasTransformer, PandasSelector

os = SMOTE(random_state=42)

def sequentialSelection(X_Data, Y_Data):
    print(X_Data.columns)
    classifier = DecisionTreeClassifier(random_state=42, class_weight='balanced')
    sfs = SequentialFeatureSelector(classifier, direction="backward", n_features_to_select=1, scoring="f1")
    sfs.fit(X_Data, Y_Data)
    print(sfs.get_feature_names_out(X_Data.columns))
    #print(sfs.get_support())

def rfe(X_Data, Y_Data):
    #classifier = GradientBoostingClassifier()
    classifier = RandomForestClassifier(random_state=42, class_weight='balanced')
    #classifier = DecisionTreeClassifier(random_state=42, class_weight='balanced')
    selector = RFE(classifier, n_features_to_select=5, step=1)
    selector = selector.fit(X_Data, Y_Data)
    print(selector.support_)
    print(selector.ranking_)

def rfecv(X_Data, Y_Data):
    classifier = DecisionTreeClassifier(random_state=42)
    #classifier = RandomForestClassifier(random_state=42, class_weight='balanced')
    selector = RFECV(classifier, step=1, cv=5, scoring="f1")#matthews_corrcoef , scoring="matthews_corrcoef"
    selector = selector.fit(X_Data, Y_Data)
    print(selector.support_)
    print(selector.get_feature_names_out(X_Data.columns))
    #print(selector.ranking_)
    return selector.get_feature_names_out(X_Data.columns)

def autoSpearman(X_Data):
    preprocess_pipeline = Pipeline([
        ('scaler', PandasTransformer(StandardScaler())),
        ('selector1', PandasSelector(VarianceThreshold())),
        ('selector2', PandasSelector(AutoSpearmanSelector(clustering_threshold=0.7, vif_threshold=10))),
    ])
    # Fit on the train.
    # print(len(X_train))
    X_Data_Reduced = preprocess_pipeline.fit_transform(X_Data)
    # print(X_train[0])
    #X_test_reduced = preprocess_pipeline.fit_transform(X_Test)

    return X_Data_Reduced