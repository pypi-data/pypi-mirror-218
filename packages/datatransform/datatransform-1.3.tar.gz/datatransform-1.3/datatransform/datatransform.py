import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

class Data_Transform:
    '''
    def yaml_setup(self):
        with open('dt_params.yaml', 'r') as file:
            dt_params = yaml.safe_load(file)
        return dt_params
    '''
    
    def ready_data(self, data):
        dataframe = pd.read_csv(data)
        X = dataframe.drop(['Decision', 'user_name'], axis=1)
        y = dataframe['Decision']
        for column in X.columns:
            X[column].fillna('Unknown', inplace=True)
            X[column] = X[column].astype(str)
        output_size = len(y.unique())
        return X, y, output_size
        
    def split_data(self, X, y, test_size = 0.2, random_state = 40):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size, random_state)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size, random_state)
        return X_train, X_test, X_val, y_train, y_test, y_val

    def label_encode(self, y_train, y_test, y_val, num_classes=3):
        label_encoder = LabelEncoder()
        label_encoder.fit(y_train)
        y_train = label_encoder.transform(y_train)
        y_test = label_encoder.transform(y_test)
        y_val = label_encoder.transform(y_val)
        y_train_categorical = to_categorical(y_train, num_classes)
        y_test_categorical = to_categorical(y_test, num_classes)
        y_val_categorical = to_categorical(y_val, num_classes)
        return y_train_categorical, y_test_categorical, y_val_categorical
