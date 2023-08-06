import numpy as np
from signal_processing_packages.src.kalman.audio_features.extract_features import generate_feature_file
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import NearMiss


def train_ml_model(ml_model, folder_path=None, x_train=None, y_train=None, x_test=None, y_test=None, scaler=None,
                   label_folder_map=None, testing=True, test_size=0.3, oversampling=None, undersampling=False):
    try:
        if folder_path is not None:
            assert x_train is None and y_train is None, "x_train and y_train must be None when folder_path is given"
            audio_df, label_name_dict = generate_feature_file(folder_path, scaler, label_folder_map)
            x_train = audio_df.drop(columns=['label'])
            y_train = audio_df['label']

        if oversampling is not None:
            assert oversampling in ["smote", "adasyn"], "oversampling must be 'smote' or 'adasyn'"
            if undersampling:
                raise ValueError("Both oversampling and undersampling cannot be enabled at the same time")
            if oversampling == "smote":
                oversampler = SMOTE()
            elif oversampling == "adasyn":
                oversampler = ADASYN()
            x_train, y_train = oversampler.fit_resample(x_train, y_train)

            if x_test is not None and y_test is not None:
                x_test, y_test = oversampler.fit_resample(x_test, y_test)

        if undersampling:
            if oversampling is not None:
                raise ValueError("Both oversampling and undersampling cannot be enabled at the same time")
            undersampler = NearMiss(version=1, n_neighbors=3)
            x_train, y_train = undersampler.fit_resample(x_train, y_train)

            if x_test is not None and y_test is not None:
                x_test, y_test = undersampler.fit_resample(x_test, y_test)

        if testing:
            if folder_path is None:
                assert x_train is not None and y_train is not None, "x_train and y_train must be provided when " \
                                                                    "testing is True and folder_path is None"
                if x_test is None and y_test is None:
                    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=test_size,
                                                                        random_state=42)
            else:
                x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=test_size,
                                                                    random_state=42)

        else:
            assert folder_path is None and x_train is not None and y_train is not None, "x_train and y_train must be " \
                                                                                        "provided when testing is " \
                                                                                        "False and folder_path is None"

        classification_report_result, model_details = train_model(ml_model, x_train, y_train, x_test, y_test)
        return model_details, classification_report_result

    except Exception as e:
        return None, str(e)


def train_model(ml_model, x_train, y_train, x_test=None, y_test=None):
    try:
        model = None
        model_details = None
        if ml_model == "random_forest":
            model = RandomForestClassifier(n_estimators=201, criterion="entropy")
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "Random Forest",
                "model_instance": model
            }

        elif ml_model == "svm":
            model = SVC(C=0.1, gamma=0.001, kernel='poly')
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "Support Vector Machine",
                "model_instance": model
            }

        elif ml_model == "decision_tree":
            cv = np.arange(1, 50)
            cv_scores = []
            for depth in cv:
                model = DecisionTreeClassifier(max_depth=depth)
                scores = cross_val_score(model, x_train, y_train, cv=10, scoring='accuracy')
                cv_scores.append(scores.mean())

            mse = [1 - x for x in cv_scores]

            optimal_depth = cv[mse.index(min(mse))]

            model = DecisionTreeClassifier(max_depth=optimal_depth)
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "Decision Tree",
                "model_instance": model
            }

        elif ml_model == "gradient_boosting":
            model = GradientBoostingClassifier()
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "Gradient Boosting",
                "model_instance": model
            }

        elif ml_model == "xgboost":
            params = {
                'objective': 'binary:logistic',
                'max_depth': 4,
                'alpha': 10,
                'learning_rate': 1.0,
                'n_estimators': 100
            }

            model = XGBClassifier(**params)
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "XGBoost",
                "model_instance": model
            }

        elif ml_model == "knn":
            model = KNeighborsClassifier(n_neighbors=3)
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "K-Nearest Neighbors",
                "model_instance": model
            }

        elif ml_model == "mlp":
            model = MLPClassifier(random_state=1, max_iter=300).fit(x_train, y_train)
            model_details = {
                "model_type": "Multi-Layer Perceptron",
                "model_instance": model
            }

        elif ml_model == "adaboost":
            model = AdaBoostClassifier()
            model.fit(x_train, y_train)
            model_details = {
                "model_type": "AdaBoost",
                "model_instance": model
            }

        if x_test is not None and y_test is not None:
            y_pred = model.predict(x_test)
            classification_report_result = classification_report(y_test, y_pred)
        else:
            y_pred = model.predict(x_train)
            classification_report_result = classification_report(y_train, y_pred)

        return classification_report_result, model_details

    except Exception as e:
        return None, str(e)

# Sample testing
# folder_path = None
# x_train = None  # Provide your x_train data here
# y_train = None  # Provide your y_train data here
# x_test = None  # Provide your x_test data here
# y_test = None  # Provide your y_test data here
# ml_model = "random_forest"
# testing = False
#
# model_details, classification_report_result = train_ml_model(ml_model, folder_path, x_train=x_train,
# y_train=y_train, x_test=x_test, y_test=y_test, testing=testing) if model_details is not None: print("Model
# Details:") print(model_details)
#
#     print("Classification Report:")
#     print(classification_report_result)
# else:
#     print("An error occurred:", classification_report_result)
