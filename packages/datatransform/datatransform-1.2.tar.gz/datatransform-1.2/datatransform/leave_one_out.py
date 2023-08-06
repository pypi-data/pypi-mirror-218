from category_encoders import LeaveOneOutEncoder
from .datatransform import Data_Transform

class LeaveOneOut:
    def transform(self, data):
        data_transformer = Data_Transform()

        X, y = data_transformer.ready_data(data)
        X_train, X_test, X_val, y_train, y_test, y_val = data_transformer.split_data(X, y)
        y_train, y_test, y_val, y_train_cat, y_test_cat, y_val_cat = data_transformer.label_encode(y_train, y_test, y_val)

        encoder = LeaveOneOutEncoder(cols=X_train.columns)
        X_train = encoder.fit_transform(X_train, y_train)
        X_val = encoder.transform(X_val)
        X_test = encoder.transform(X_test)

        return X_train, X_test, X_val, y_train_cat, y_test_cat, y_val_cat
    

