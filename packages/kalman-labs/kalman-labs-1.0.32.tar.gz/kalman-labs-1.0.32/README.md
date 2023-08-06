# kalman-labs

The `kalman-labs` package provides a set of tools and functionalities for audio signal processing and machine learning tasks. It includes features for feature extraction, machine learning model training, and deep learning model training.

## Features

### 1. Audio Feature Extraction

The package provides a module for extracting audio features from audio files. The `audio_features` module offers various feature extraction techniques, such as MFCC, Mel spectrogram, Chromagram, and more. These features can be used as inputs to machine learning and deep learning models.

Example usage:

```python
from kalman.audio_features import extract_features

audio_file = 'path/to/audio/file.wav'
features = extract_features(audio_file)

# The 'features' variable contains a dictionary of extracted audio features
```

- `generate_feature_file(folder_path, scaler=None, label_folder_map=None)`: This function generates a feature file by extracting audio features from the audio files in a specified folder. It returns a DataFrame containing the extracted features and a dictionary mapping labels to folder names. 

  **Parameters:**
  
  - `folder_path` (str): The path to the folder containing the audio files. This folder should have subfolders representing different classes, and each subfolder should contain audio files corresponding to that class.
  
  - `scaler` (str or None, optional): The scaler to use for feature normalization. Supported options are "standard" and "minmax". If set to None, no scaling will be applied. Default is None.
  
  - `label_folder_map` (dict or None, optional): A dictionary mapping labels to folder names. This allows you to override the default folder names as class labels. If set to None, the folder names will be used as labels. Default is None.
  
  **Example:**
  
  ```python
  folder_path = "audio_data"
  scaler = "standard"
  label_folder_map = {"class1": "folder1", "class2": "folder2"}
  
  audio_df, label_name_dict = generate_feature_file(folder_path, scaler, label_folder_map)
  ```
  
  In this example, audio features will be extracted from the audio files in the "audio_data" folder using the "standard" scaler. The labels will be mapped according to the provided `label_folder_map`.
  
Note: The `audio_feature_extraction` parameter and `generate_feature_file` function are applicable to both the `train_ml_model` and `train_dl_model` functions.

### 2. Machine Learning Model Training

The package includes functionalities for training machine learning models on audio data. It supports several popular machine learning algorithms, such as Random Forest, Support Vector Machine (SVM), K-Nearest Neighbors (KNN), and Logistic Regression.

Example usage:

```python
from kalman.machine_learning_training import train_ml_model

ml_model = 'random_forest'
folder_path = 'path/to/audio/files'  # Path to the folder containing audio files
x_train = ...   # Provide the training data
y_train = ...   # Provide the training labels
x_test = ...   # Provide the testing data (optional)
y_test = ...   # Provide the testing labels (optional)

# Example usage with additional parameters:
undersampling = True
oversampling = 'smote'
scaler = 'standard'
label_folder_map = {'class_1': 'folder_1', 'class_2': 'folder_2'}

model_details, classification_report = train_ml_model(ml_model, folder_path=folder_path, x_train=x_train, y_train=y_train,
                                                     x_test=x_test, y_test=y_test, undersampling=undersampling,
                                                     oversampling=oversampling, scaler=scaler,
                                                     label_folder_map=label_folder_map)

# The resulting model_details dictionary contains information about the trained model
# The classification_report contains precision, recall, f1-score, and support for each class
```

**Parameter Descriptions:**

- `ml_model` (str): The machine learning model to train. Supported options are: "random_forest", "svm", "knn", "logistic_regression".
- `folder_path` (str): Path to the folder containing audio files. This parameter should be used when the audio data is stored in separate files.
- `audio_feature_extraction` (str): The audio feature extraction technique to use. Supported options are: "mfcc", "chroma", "mel".
- `x_train` (array-like): Training data features. This should be a 2D array-like object.
- `y_train` (array-like): Training data labels. This should be a 1D array-like object.
- `x_test` (array-like, optional): Testing data features. This should be a 2D array-like object. (default: None)
- `y_test` (array-like, optional): Testing data labels. This should be a 1D array-like object. (default: None)
- `test_size` (float, optional): The proportion of the testing data when `x_test` and `y_test` are not provided. This parameter is used for splitting the training data into training and testing sets. (default: 0.2)
- `undersampling` (bool, optional): Whether to perform undersampling to balance the class distribution. (default: False)
- `oversampling` (str, optional): The oversampling technique to use. Supported options are: "smote", "adasyn". (default: None)
- `scaler` (str, optional): The scaler to apply to the data. Supported options are: "standard", "minmax", "robust". (default: None)
- `label_folder_map` (dict, optional): A mapping of class labels to folder names in the case of separate audio files. This is required when `folder_path` is used. (default: None)
- `testing` (bool, optional): Whether to perform testing and return evaluation results. (default: False)



### 3. Deep Learning Model Training

The package provides functionalities for training deep learning models on audio data. It supports various architectures, including Deep Neural Networks (DNN), Convolutional Neural Networks (CNN), Bidirectional LSTM, and Convolutional LSTM.

Example usage:

```python
from kalman.deep_learning_training import train_dl_model

dl_model = 'DNN'
folder_path = 'path/to/audio/files'  # Path to the folder containing audio files
x_train = ...   # Provide the training data
y_train = ...   # Provide the training labels
x_val = ...     # Provide the validation data
y_val = ...     # Provide the validation labels

# Example usage with additional parameters:
val_size = 0.3
oversampling = 'smote'
undersampling = True
batch_size = 48
epochs = 100

results = train_dl_model(dl_model, folder_path=folder_path, x_train=x_train, y_train=y_train,
                         x_val=x_val, y_val=y_val, val_size=val_size, oversampling=oversampling,
                         undersampling=undersampling, batch_size=batch_size, epochs=epochs)

# The resulting results dictionary contains evaluation metrics such as accuracy, precision, recall, and AUC
```

**Parameter Descriptions:**

- `dl_model` (str): The deep learning model to train. Supported options are: "DNN", "DNN-CNN", "DNN-BiLSTM", "DNN-convLSTM".
- `folder_path` (str): Path to the folder containing audio files. This parameter should be used when the audio data is stored in separate files.
- `audio_feature_extraction` (str): The audio feature extraction technique to use. Supported options are: "mfcc", "chroma", "mel".
- `x_train` (array-like): Training data features. This should be a 2D array-like object.
- `y_train` (array-like): Training data labels. This should be a 1D array-like object.
- `x_val` (array-like): Validation data features. This should be a 2D array-like object.
- `y_val` (array-like): Validation data labels. This should be a 1D array-like object.
- `val_size` (float, optional): The proportion of the validation data when `x_val` and `y_val` are not provided. (default: 0.3)
- `oversampling` (str, optional): The oversampling technique to use. Supported options are: "smote", "adasyn". (default: None)
- `undersampling` (bool, optional): Whether to perform undersampling to balance the class distribution. (default: False)
- `batch_size` (int, optional): The batch size for training the deep learning models. (default: 48)
- `epochs` (int, optional): The number of epochs for training the deep learning models. (default: 100)
- `testing` (bool, optional): Whether to perform testing and return evaluation results. (default: False)

**Parameter combinations:**
- `folder_path`, `audio_feature_extraction`, `x_train`, and `y_train` must not be used together. Use either `folder_path` or `audio_feature_extraction` with `x_train` and `y_train` to provide the training data.
- `x_val` and `y_val` should be provided together. If not provided, the validation data will be split from the training data based on `val_size`.
- `oversampling` and `undersampling` cannot be enabled at the same time. Choose either oversampling or undersampling.

In case `testing` parameter is set to `True` in `train_dl_model`, the function will perform testing by splitting `x_val` and `y_val` into 70% validation and 30% testing data.


The evaluation results will be included in the `results` dictionary, which will contain metrics such as accuracy, precision, recall, and AUC.

Please note that the choice of parameters depends on your specific requirements and the nature of your audio data. Use the appropriate combinations of parameters based on your needs.
