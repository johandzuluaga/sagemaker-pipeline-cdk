from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class ReshapeWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, model):
        self.model = model

    def predict(self, X):
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        return self.model.predict(X)