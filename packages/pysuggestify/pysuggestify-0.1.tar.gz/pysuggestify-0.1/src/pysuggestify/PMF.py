import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

class PMF():
    """
    Probabilistic Matrix Factorization class for building recommendation models.

    """
    def __init__(self, n_dims = 50, lambda_U = 0.3, lambda_V = 0.3):
        self.n_dims = n_dims
        self.lambda_U = lambda_U
        self.lambda_V = lambda_V
    
    def prepare_data(self, df: pd.DataFrame, row_id_name: str, col_id_name: str, rating_name: str) -> None:
        """
        Prepares the data for building a PMF recommendation model.

        Args:
            df (pandas.DataFrame): The input data containing user-item interactions.
                It should have the following columns: user ID, item ID and rating.

        Returns:
            None

        Examples:
            # Example: Loading data from a CSV file
            PMF_model.prepare_data(ratings, 'userId', 'movieId', 'rating')
        """
        self.df = df
        self.row_id_name = row_id_name
        self.col_id_name = col_id_name
        self.rating_name = rating_name
        self.rating_range = (df[rating_name].min(), df[rating_name].max())
        self.R, self.n_users, self.n_items, self.user_to_row, self.item_to_column = self.get_rating_matrix()
        print('Rating matrix prepared!')
        print('Number of users: ', self.n_users)
        print('Number of items: ', self.n_items)
    
    def get_rating_matrix(self):
        """
        Method to eturns the rating matrix R representing user-item interactions
        with necessary informations.

        Args:
            None

        Returns:
            R: rating matrix representing user-item interactions
            n_users: number of unique users
            n_items: number of unique items
            _user_to_row: dictionary which translate userID to row number
            _item_to_column: dictionary which translate movieID to column number
        """
        _user_to_row = {}
        _item_to_column = {}

        uniq_users = np.unique(self.df[self.row_id_name].values)
        uniq_movies = np.unique(self.df[self.col_id_name].values)

        for i, user_id in enumerate(uniq_users):
            _user_to_row[user_id] = i

        for j, item_id in enumerate(uniq_movies):
            _item_to_column[item_id] = j

        n_users = len(uniq_users)
        n_items = len(uniq_movies)

        R = np.zeros((n_users, n_items))
        for index, row in self.df.iterrows():
            i = _user_to_row[row[self.row_id_name]]
            j = _item_to_column[row[self.col_id_name]]
            R[i, j] = row[self.rating_name]
        
        return R, n_users, n_items, _user_to_row, _item_to_column
    
    def transpose_dict(self, dictionary='user'):
        """
        Transposes the given dictionary, swapping keys and values.

        Args:
            dictionary (str): Specifies the dictionary to transpose. Should be either 'user' or 'item'.
                If 'user' is provided, the user-to-row dictionary will be transposed, swapping user IDs
                with their corresponding row indices. If 'item' is provided, the item-to-column dictionary
                will be transposed, swapping item IDs with their corresponding column indices.
                Defaults to 'user'.

        Returns:
            dict: The transposed dictionary, where keys and values are swapped.


        Examples:
            # Example 1: Transposing the user-to-row dictionary
            PMF_model = PMF(n_dims = 30, lambda_U = 0.3, lambda_V = 0.3)
            PMF_model.prepare_data(ratings, 'userId', 'movieId', 'rating')
            transposed_user_dict = PMF_model.transpose_dict(dictionary='user')

            # Example 2: Transposing the item-to-column dictionary
            PMF_model = PMF(n_dims = 30, lambda_U = 0.3, lambda_V = 0.3)
            PMF_model.prepare_data(ratings, 'userId', 'movieId', 'rating')
            transposed_item_dict = PMF_model.transpose_dict(dictionary='item')
        """
        if dictionary == 'user':
            trans_dict = {key: value for (value, key) in self.user_to_row.items()}
        if dictionary == 'item':
            trans_dict = {key: value for (value, key) in self.item_to_column.items()}
        return trans_dict

    def initialize_parameters(self):
        """
        Initializes the parameters for the recommendation model.
        """
        parameters = {}
        U = np.random.normal(0.0, 1.0/self.lambda_U, (self.n_dims, self.n_users))
        V = np.random.normal(0.0, 1.0/self.lambda_V, (self.n_dims, self.n_items))

        parameters['U'] = U
        parameters['V'] = V
        return parameters

    def update_parameters(self):
        """
        Method for update parameters - latent space matrixes.
        """
        U = self.parameters['U']
        V = self.parameters['V']
        lambda_U = self.lambda_U
        lambda_V = self.lambda_V

        for i in range(self.n_users):
            V_j = V[:, self.R[i, :] > 0]
            U[:, i] = np.dot(np.linalg.inv(np.dot(V_j, V_j.T) + lambda_U * np.identity(self.n_dims)), np.dot(self.R[i, self.R[i, :] > 0], V_j.T))

        for j in range(self.n_items):
            U_i = U[:, self.R[:, j] > 0]
            V[:, j] = np.dot(np.linalg.inv(np.dot(U_i, U_i.T) + lambda_V * np.identity(self.n_dims)), np.dot(self.R[self.R[:, j] > 0, j], U_i.T))

        self.parameters['U'] = U
        self.parameters['V'] = V

    def log_a_posteriori(self):
        """
        Returns log a posteriori probability
        """
        lambda_U = self.lambda_U
        lambda_V = self.lambda_V
        U = self.parameters['U']
        V = self.parameters['V']

        UV = np.dot(U.T, V)
        R_UV = (self.R[self.R > 0] - UV[self.R > 0])

        return -0.5 * (np.sum(np.dot(R_UV, R_UV.T)) + lambda_U * np.sum(np.dot(U, U.T)) + lambda_V * np.sum(np.dot(V, V.T)))

    def update_max_min_ratings(self):
        """
        Update min and max ratings in predicted matrix.
        """
        U = self.parameters['U']
        V = self.parameters['V']
        R = U.T @ V
        self.parameters['min_rating'] = np.min(R)
        self.parameters['max_rating'] = np.max(R)
    
    def predict(self):
        """
        Generates the predicted rating matrix using the trained model parameters.
        
        Returns:
            R_pred: The predicted rating matrix, where rows correspond to users and
            columns correspond to items. Each element of the matrix represents the predicted
            rating for a user-item pair.


        Examples:
            # Example:
            PMF_model = PMF(n_dims = 30, lambda_U = 0.3, lambda_V = 0.3)
            PMF_model.prepare_data(ratings, 'userId', 'movieId', 'rating')
            PMF_model.fit(n_epochs=50)
            PMF_model.predict()

        """
        U = self.parameters['U']
        V = self.parameters['V']
        R_pred = U.T @ V
        R_pred[R_pred > self.rating_range[1]] = self.rating_range[1]
        R_pred[(R_pred < self.rating_range[0]) & (R_pred != 0)] = self.rating_range[0]
        return R_pred

    def predict_one(self, user_id, item_id):
        """
        Predicts the rating for a specific user-item pair using the trained model parameters.

        Args:
            user_id: The ID of the user for whom the rating is predicted.
            item_id: The ID of the item for which the rating is predicted.

        Returns:
            float: The predicted rating for the specified user-item pair.

        Raises: TODO
            KeyError: If the user ID or item ID is not found in the respective dictionaries.

        Examples:
            # Example:
            predicted_rating = PMF_model.predict_one(user_id=42, item_id=101)
        """
        U = self.parameters['U']
        V = self.parameters['V']

        r_ij = U[:, self.user_to_row[user_id]].T.reshape(1, -1) @ V[:, self.item_to_column[item_id]].reshape(-1, 1)
        if r_ij[0][0] > self.rating_range[1]:
            r_ij[0][0] = self.rating_range[1]
        elif r_ij[0][0] < self.rating_range[0]:
            r_ij[0][0] = self.rating_range[0]

        return r_ij[0][0]

    def evaluate(self):
        """
        Evaluates the performance of the recommendation model using root mean squared error (RMSE).

        Returns:
            float: The root mean squared error (RMSE) value indicating the model's performance.

        Examples:
            # Example:
            rmse_score = PMF_model.evaluate()
        """
        ratings_mask = self.R > 0
        R_pred = self.predict()
        rmse = (np.square(self.R[ratings_mask] - R_pred[ratings_mask]).mean(axis=None))**(0.5)
        return rmse

    def fit(self, n_epochs = 10):
        """
        Trains the recommendation model using the specified number of epochs.

        Args:
            n_epochs (int): The number of epochs (iterations) for training the model.
                Defaults to 10.

        Returns:
            None

        Examples:
            # Example:
            PMF_model.fit(n_epochs=20)
        """
        self.parameters = self.initialize_parameters()
        
        self.history = {}
        self.history['log_p'] = []
        self.history['rmse'] = []

        self.update_max_min_ratings()

        for k in range(n_epochs):
            start_time = time.time()
            self.update_parameters()
            log_ap = self.log_a_posteriori()
            self.history['log_p'].append(log_ap)

            self.update_max_min_ratings()
            new_rmse = self.evaluate()
            self.history['rmse'].append(new_rmse)
            end_time = time.time()
            
            print(f'Epoch {k+1}/{n_epochs} \n  Time: {round(end_time - start_time, 1)}s, Log p posteriori: {round(log_ap, 4)}, RMSE: {round(new_rmse, 4)}')

        self.update_max_min_ratings()
    
    def plot_history(self):
        """
        Plots the history of the training process, including the log a-posteriori probability
        and root mean square error (RMSE) values over the epochs.

        Returns:
            None

        Examples:
            # Example:
            PMF_model.plot_history()
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        ax1.set_title('Log a-posteriori probability')
        ax1.plot(np.arange(1, len(self.history['log_p'])+1), self.history['log_p'], label='log_p')
        ax1.set_xlabel('epoch')
        ax1.set_ylabel('log_p')
        ax1.legend()

        ax2.set_title('Root Mean Square Error')
        ax2.plot(np.arange(1, len(self.history['rmse'])+1), self.history['rmse'], label='RMSE')
        ax2.set_xlabel('epoch')
        ax2.set_ylabel('RMSE')
        ax2.legend()
        plt.show()
    
    def get_masked_preds(self):
        """
        Returns the masked predictions where the original rating matrix has zero values.

        Returns:
            numpy.ndarray: The masked predictions, where predictions are shown only for positions
                where the original rating matrix has zero values. Positions with non-zero values
                in the original matrix are masked (set to zero) in the predictions.

        Examples:
            # Example: Getting the masked predictions
            PMF_model.get_masked_preds()
        """
        return self.predict()*(self.R == 0)
