import numpy as np
import pandas as pd
import prince
from keras.utils import to_categorical
from .datatransform import Data_Transform


class mca():
    def transform(self, data):
        data_transformer = Data_Transform()

        X, y, output_size = data_transformer.ready_data(data)
        X_train, X_test, X_val, y_train, y_test, y_val = data_transformer.split_data(X, y)
        y_train, y_test, y_val = data_transformer.label_encode(y_train, y_test, y_val)
        num_classes = 3
        y_train_cat= to_categorical(y_train, num_classes)
        y_test_cat = to_categorical(y_test, num_classes)
        y_val_cat = to_categorical(y_val, num_classes)

        one_hot = pd.get_dummies(X)
        n_components = self.get_n_components(one_hot)

        mca = prince.MCA(n_components, n_iter=20, copy=True, check_input=True, engine='sklearn')
        X_train = mca.fit_transform(X_train)
        X_test = mca.fit_transform(X_test)
        X_val = mca.fit_transform(X_val)
        return X_train, X_test, X_val, y_train_cat, y_test_cat, y_val_cat, output_size, n_components

    def get_n_components(self, data, threshold=0.9):
        covariance_matrix = np.cov(data.values.T)
        eigenvalues, _ = np.linalg.eig(covariance_matrix)
        total_variance = np.sum(eigenvalues)
        explained_variance_ratio = eigenvalues / total_variance
        cumulative_explained_variance = np.cumsum(explained_variance_ratio)
        n_components = np.argmax(cumulative_explained_variance >= threshold) + 1
        return n_components

    