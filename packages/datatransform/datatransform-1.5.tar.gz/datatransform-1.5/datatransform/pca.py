import pandas as pd
from sklearn.decomposition import PCA
from keras.utils import to_categorical
from .datatransform import Data_Transform

class PCA():
    def transform(self, data):
        data_transformer = Data_Transform()

        X, y, output_size = data_transformer.ready_data(data)
        X = pd.get_dummies(X)
        X_train, X_test, X_val, y_train, y_test, y_val = data_transformer.split_data(X, y)
        y_train, y_test, y_val = data_transformer.label_encode(y_train, y_test, y_val)
        num_classes = 3
        y_train_cat= to_categorical(y_train, num_classes)
        y_test_cat = to_categorical(y_test, num_classes)
        y_val_cat = to_categorical(y_val, num_classes)

        pca = PCA(n_components = 0.98)
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        X_val = pca.transform(X_val)
        n_components = pca.n_components_

        return X_train, X_test, X_val, y_train_cat, y_test_cat, y_val_cat, output_size, n_components