import numpy as np
from audio_features.extract_features import generate_feature_file
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import NearMiss

import tensorflow as tf
import keras
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Reshape, Conv2D, ConvLSTM1D, AveragePooling2D, BatchNormalization, \
    Activation, Flatten, LSTM, Bidirectional
from keras.utils import to_categorical


def train_dl_model(dl_model, folder_path=None, x_train=None, y_train=None, x_val=None, y_val=None, scaler=None,
                   label_folder_map=None, testing=True, val_size=0.3, oversampling=None, undersampling=False,
                   batch_size=48, epochs=100):
    oversampler = None
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

            if x_val is not None and y_val is not None:
                x_val, y_val = oversampler.fit_resample(x_val, y_val)

        if undersampling:
            if oversampling is not None:
                raise ValueError("Both oversampling and undersampling cannot be enabled at the same time")
            undersampler = NearMiss(version=1, n_neighbors=3)
            x_train, y_train = undersampler.fit_resample(x_train, y_train)

            if x_val is not None and y_val is not None:
                x_val, y_val = undersampler.fit_resample(x_val, y_val)

        if x_val is None and y_val is None:
            x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=val_size,
                                                              random_state=42)

        results = train_model(dl_model, x_train, y_train, x_val, y_val, testing, batch_size, epochs)
        return results

    except Exception as e:
        return None, str(e)


def train_model(dl_model, x_train, y_train, x_val, y_val, testing, batch_size, epochs):
    model = None
    model_details = None
    results = None
    if dl_model == "DNN":
        results = train_test_fit_dnn_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs)
    elif dl_model == "DNN-CNN":
        results = train_test_dnn_cnn_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs)
    elif dl_model == "DNN-BiLSTM":
        results = train_test_dnn_bilstm_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs)
    elif dl_model == "DNN-convLSTM":
        results = train_test_dnn_convlstm_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs)

    return results


def train_test_fit_dnn_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs):
    x_test = None
    y_test = None

    if testing:
        x_train, x_test, y_train, y_test = train_test_split(x_val, y_val, test_size=0.3,
                                                            random_state=42)

    def build_model():
        '''Function to build ensemble model'''
        # First Model
        inp1 = Input(shape=193)
        lay1 = Dense(units=512, activation='relu', kernel_initializer='GlorotUniform')(inp1)
        lay2 = Dropout(0.4)(lay1)
        lay3 = Dense(units=256, activation='relu', kernel_initializer='GlorotUniform')(lay2)
        lay4 = Dropout(0.2)(lay3)
        hidden1 = Dense(128, activation='relu')(lay4)
        hidden2 = Dense(64, activation='relu')(hidden1)
        output = Dense(2, activation='softmax')(hidden2)
        model = Model(inputs=inp1, outputs=output)

        return model

    num_classes = len(np.unique(y_train))

    x_train = x_train.values
    y_train = y_train.values
    y_train = to_categorical(y_train, num_classes=num_classes)

    x_val = x_val.values
    y_val = y_val.values
    y_val = to_categorical(y_val, num_classes=num_classes)

    test_data = None

    if testing:
        x_test = x_test.values
        y_test = y_test.values
        y_test = to_categorical(y_test, num_classes=num_classes)
        test_data = InputGenerator(x_test, y_test, batch_size=batch_size)

    train_data = InputGenerator(x_train, y_train, batch_size=batch_size)
    val_data = InputGenerator(x_val, y_val, batch_size=batch_size)

    model = build_model()
    print(model.summary())

    model.compile(
        optimizer='Adam',
        loss='BinaryCrossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall(), keras.metrics.AUC()])

    history = model.fit(train_data, epochs=epochs, validation_data=val_data,
                        verbose=2)

    if testing:
        results = testing_evaluation(model, test_data, y_test)
        return history, results

    return history


def train_test_dnn_cnn_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs):
    x_test = None
    y_test = None

    if testing:
        x_train, x_test, y_train, y_test = train_test_split(x_val, y_val, test_size=0.3,
                                                            random_state=42)

    def build_model():
        '''Function to build ensemble model'''
        # First Model
        inp1 = Input(shape=193)
        lay1 = Dense(units=512, activation='relu', kernel_initializer='GlorotUniform')(inp1)
        lay2 = Dropout(0.4)(lay1)
        lay61 = Reshape((64, 8, 1))(lay2)
        lay62 = Conv2D(32, (3, 3), strides=(2, 2))(lay61)
        lay63 = AveragePooling2D((2, 2), strides=(2, 2))(lay62)
        lay64 = BatchNormalization()(lay63)
        lay65 = Activation('relu')(lay64)

        lay66 = Conv2D(64, (3, 3), padding="same")(lay65)
        # lay67  = AveragePooling2D((2, 2), strides=(2,2)) (lay66)
        lay68 = BatchNormalization()(lay66)
        lay69 = Activation('relu')(lay68)

        lay611 = Conv2D(64, (3, 3), padding="same")(lay69)
        # lay612 = AveragePooling2D((2, 2), strides=(2,2)) (lay611)
        lay613 = BatchNormalization()(lay611)
        lay614 = Activation('relu')(lay613)

        lay615 = Flatten()(lay614)
        lay616 = Dense(units=256, activation='relu', kernel_initializer='GlorotUniform')(lay615)
        lay617 = Dropout(rate=0.5)(lay616)
        lay3 = Dense(units=256, activation='relu', kernel_initializer='GlorotUniform')(lay2)
        lay4 = Dropout(0.2)(lay3)
        hidden1 = Dense(128, activation='relu')(lay4)
        hidden2 = Dense(64, activation='relu')(hidden1)
        output = Dense(2, activation='softmax')(hidden2)
        model = Model(inputs=inp1, outputs=output)

        return model

    num_classes = len(np.unique(y_train))

    x_train = x_train.values
    y_train = y_train.values
    y_train = to_categorical(y_train, num_classes=num_classes)

    x_val = x_val.values
    y_val = y_val.values
    y_val = to_categorical(y_val, num_classes=num_classes)

    test_data = None

    if testing:
        x_test = x_test.values
        y_test = y_test.values
        y_test = to_categorical(y_test, num_classes=num_classes)
        test_data = InputGenerator(x_test, y_test, batch_size=batch_size)

    train_data = InputGenerator(x_train, y_train, batch_size=batch_size)
    val_data = InputGenerator(x_val, y_val, batch_size=batch_size)

    model = build_model()
    print(model.summary())

    model.compile(
        optimizer='Adam',
        loss='BinaryCrossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall(), keras.metrics.AUC()])

    history = model.fit(train_data, epochs=epochs, validation_data=val_data,
                        verbose=2)

    if testing:
        results = testing_evaluation(model, test_data, y_test)
        return history, results

    return history


def train_test_dnn_bilstm_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs):
    x_test = None
    y_test = None

    if testing:
        x_train, x_test, y_train, y_test = train_test_split(x_val, y_val, test_size=0.3,
                                                            random_state=42)

    def build_model():
        '''Function to build ensemble model'''
        # First Model
        inp1 = Input(shape=193)
        lay1 = Dense(units=512, activation='relu', kernel_initializer='GlorotUniform')(inp1)
        lay2 = Dropout(0.4)(lay1)
        lay2 = Reshape((64, 8))(lay2)
        lay2 = BatchNormalization()(lay2)
        lay2 = Bidirectional(LSTM(64, return_sequences=True))(lay2)
        lay2 = Bidirectional(LSTM(64))(lay2)
        lay3 = Dense(units=256, activation='relu', kernel_initializer='GlorotUniform')(lay2)
        lay4 = Dropout(0.2)(lay3)
        hidden1 = Dense(128, activation='relu')(lay4)
        hidden2 = Dense(64, activation='relu')(hidden1)
        output = Dense(2, activation='softmax')(hidden2)
        model = Model(inputs=inp1, outputs=output)

        return model

    num_classes = len(np.unique(y_train))

    x_train = x_train.values
    y_train = y_train.values
    y_train = to_categorical(y_train, num_classes=num_classes)

    x_val = x_val.values
    y_val = y_val.values
    y_val = to_categorical(y_val, num_classes=num_classes)

    test_data = None

    if testing:
        x_test = x_test.values
        y_test = y_test.values
        y_test = to_categorical(y_test, num_classes=num_classes)
        test_data = InputGenerator(x_test, y_test, batch_size=batch_size)

    train_data = InputGenerator(x_train, y_train, batch_size=batch_size)
    val_data = InputGenerator(x_val, y_val, batch_size=batch_size)

    model = build_model()
    print(model.summary())

    model.compile(
        optimizer='Adam',
        loss='BinaryCrossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall(), keras.metrics.AUC()])

    history = model.fit(train_data, epochs=epochs, validation_data=val_data,
                        verbose=2)

    if testing:
        results = testing_evaluation(model, test_data, y_test)
        return history, results

    return history


def train_test_dnn_convlstm_model(x_train, y_train, x_val, y_val, testing, batch_size, epochs):
    x_test = None
    y_test = None

    if testing:
        x_train, x_test, y_train, y_test = train_test_split(x_val, y_val, test_size=0.3,
                                                            random_state=42)

    def build_model():
        '''Function to build ensemble model'''
        # First Model
        inp1 = Input(shape=193)
        lay1 = Dense(units=512, activation='relu', kernel_initializer='GlorotUniform')(inp1)
        lay2 = Dropout(0.4)(lay1)
        lay61 = Reshape((64, 8, 1))(lay2)
        lay62 = ConvLSTM1D(filters=40, kernel_size=(3),
                           padding='same', input_shape=(None, 64, 8, 1), return_sequences=True)(lay61)
        lay63 = BatchNormalization()(lay62)
        lay64 = ConvLSTM1D(filters=40, kernel_size=(3),
                           padding='same', return_sequences=True)(lay63)
        lay614 = BatchNormalization()(lay64)
        lay615 = Flatten()(lay614)
        lay616 = Dense(units=256, activation='relu', kernel_initializer='GlorotUniform')(lay615)
        lay617 = Dropout(rate=0.5)(lay616)
        lay3 = Dense(units=256, activation='relu', kernel_initializer='GlorotUniform')(lay2)
        lay4 = Dropout(0.2)(lay3)
        hidden1 = Dense(128, activation='relu')(lay4)
        hidden2 = Dense(64, activation='relu')(hidden1)
        output = Dense(2, activation='softmax')(hidden2)
        model = Model(inputs=inp1, outputs=output)

        return model

    num_classes = len(np.unique(y_train))

    x_train = x_train.values
    y_train = y_train.values
    y_train = to_categorical(y_train, num_classes=num_classes)

    x_val = x_val.values
    y_val = y_val.values
    y_val = to_categorical(y_val, num_classes=num_classes)

    test_data = None

    if testing:
        x_test = x_test.values
        y_test = y_test.values
        y_test = to_categorical(y_test, num_classes=num_classes)
        test_data = InputGenerator(x_test, y_test, batch_size=batch_size)

    train_data = InputGenerator(x_train, y_train, batch_size=batch_size)
    val_data = InputGenerator(x_val, y_val, batch_size=batch_size)

    model = build_model()
    print(model.summary())

    model.compile(
        optimizer='Adam',
        loss='BinaryCrossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall(), keras.metrics.AUC()])

    history = model.fit(train_data, epochs=epochs, validation_data=val_data,
                        verbose=2)

    if testing:
        results = testing_evaluation(model, test_data, y_test)
        return history, results

    return history


class CustomPipeline(tf.keras.utils.Sequence):
    def __init__(self, data_x, data_y, batch_size=48, shuffle=False, n_classes=2):
        self.indexes = None
        self.features = data_x
        self.labels = data_y
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.n_features = self.features.shape[1]
        self.n_classes = 2
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.features) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        X, y = self.__data_generation(indexes)
        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.features))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, indexes):
        X = np.empty((self.batch_size, self.n_features))
        y = np.empty((self.batch_size, self.n_classes), dtype=int)

        # print(self.features)
        for i, ID in enumerate(indexes):
            X[i,] = self.features[ID]
            y[i,] = self.labels[ID]
        return X, y


class InputGenerator(tf.keras.utils.Sequence):
    """Wrapper of two generatos for the combined input model"""

    def __init__(self, X, Y, batch_size):
        self.genX = CustomPipeline(X, Y, batch_size=batch_size, shuffle=False)

    def __len__(self):
        return self.genX.__len__()

    def __getitem__(self, index):
        X_batch, Y_batch = self.genX.__getitem__(index)
        return X_batch, Y_batch


def testing_evaluation(model, test_data, y_test):
    test_res = model.evaluate(test_data)
    y_pred = model.predict(test_data)
    y_pred = np.array(list(map(lambda x: np.argmax(x), y_pred)))
    y_true = np.array(list(map(lambda x: np.argmax(x), y_test)))

    results = {
        "Test Loss": test_res[0],
        "Test Precision": precision_score(y_true[:len(y_pred)], y_pred),
        "Test Recall": recall_score(y_true[:len(y_pred)], y_pred),
        "Test Accuracy": test_res[1],
        "Test AUC": test_res[2]
    }

    return results
