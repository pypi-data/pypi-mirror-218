import os
import numpy as np
import joblib
import logging

class Perceptron:
    def __init__(self, eta: float=None, epochs: int=None):

        logging.info(f">>>>>>>Initialsing Perceptron Class <<<<<<<<<<<")

        self.weights = np.random.randn(3) * 1e-4 # small random weights
        training = (eta is not None) and (epochs is not None)
        
        if training:
            logging.info(f"initial weights before training: \n{self.weights}\n")
            logging.info(f"initial weights before training: \n{self.weights}\n")
        
        self.eta = eta
        self.epochs = epochs        

    def _z_outcome(self, inputs, weights):
        return np.dot(inputs, weights)

    def activation(self, z):
        return np.where(z > 0, 1, 0)

    def fit(self, X, y):
        
        self.X = X
        self.y = y
        
        X_with_bias = np.c_[self.X, -np.ones((len(self.X), 1))]
        logging.info(f"X With Bias:  {X_with_bias}")

        for epoch in range(self.epochs):
            logging.info(f"for epoch: {epoch}")
            logging.info("--"*10)

            z = self._z_outcome(X_with_bias, self.weights)
            y_hat = self.activation(z)
            
            logging.info(f"predicted value after forward pass: {y_hat}")

            self.error = self.y - y_hat
            logging.info(f"Error: {self.error}")


            self.weights = self.weights + self.eta * np.dot(X_with_bias.T, self.error)
            logging.info(f"Updated Weights After Epochs {epoch + 1}/{self.epochs}: \n{self.weights}")
            logging.info(">>"*10)

    def predict(self, X):

        # Predict method means forword pass

        X_with_bias = np.c_[X, -np.ones((len(X), 1))]
        z = self._z_outcome(X_with_bias, self.weights)
        
        return self.activation(z)

    def total_loss(self):
        total_loss = np.sum(self.error)

        logging.info(f"\nTotal loss: {total_loss}")

        return total_loss

    def _create_dir_return_path(self, model_dir, filename):
        os.makedirs(model_dir, exist_ok=True)
        return os.path.join(model_dir, filename)
    
    def save(self, filename, model_dir=None):
        if model_dir is not None:
            model_file_path = self._create_dir_return_path(model_dir, filename)
            joblib.dump(self, model_file_path)
        else:
            model_file_path = self._create_dir_return_path("model", filename)
            joblib.dump(self, model_file_path)
        
        logging.info(f"Model [ {filename} ] saved at [ {model_file_path} ]")

    def load(self, filepath):
        return joblib.load(filepath)