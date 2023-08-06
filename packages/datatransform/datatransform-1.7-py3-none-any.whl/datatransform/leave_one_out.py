from category_encoders import LeaveOneOutEncoder
from keras.utils import to_categorical
from .datatransform import Data_Transform

class LeaveOneOut:
    def transform(self, data):
        data_transformer = Data_Transform()

        X, y, output_size = data_transformer.ready_data(data)
        X_train, X_test, X_val, y_train, y_test, y_val = data_transformer.split_data(X, y)
        y_train, y_test, y_val = data_transformer.label_encode(y_train, y_test, y_val)

        encoder = LeaveOneOutEncoder(cols=X_train.columns)
        X_train = encoder.fit_transform(X_train, y_train)
        X_val = encoder.transform(X_val)
        X_test = encoder.transform(X_test)

        num_classes = 3
        y_train_cat= to_categorical(y_train, num_classes)
        y_test_cat = to_categorical(y_test, num_classes)
        y_val_cat = to_categorical(y_val, num_classes)
        
        n_components = len(X_train.columns)

        return X_train, X_test, X_val, y_train_cat, y_test_cat, y_val_cat, output_size, n_components
    

