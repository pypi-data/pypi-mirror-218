<p align="center">
  <img src="https://raw.githubusercontent.com/msoczi/pysuggestify/main/img/logo.png" width="371" height="168" />
</p>

<!-- PROJECT -->
<br />
<p align="center">
  <h3 align="center">Easy Recommendation System with <code style="background: papayawhip;">PySuggestify</code></h3>
</p>

`PySuggestify` is a module for building personalized recommendation system with PMF algorithm.
<br/><br/>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents:</summary>
  <ol>
    <li><a href="#Overview">Overview</a></li>
    <li><a href="#Installation">Installation</a></li>
    <li><a href="#Example">Example</a></li>
  </ol>
</details>



## Overview

Welcome to `PySuggestify` – an recommendation system implemented with Probabilistic Matrix Factorization (PMF) algorithm. This project aims to provide a low-code solution for building personalized recommender models.

For instance you can build a solution for suggesting movies on a streaming platform based on user ratings.

<p align="center">
  <img src="https://raw.githubusercontent.com/msoczi/pysuggestify/main/img/rating_matrix.png" width="352" height="173" />
</p>

<br>
My implementation incorporates Probabilistic Matrix Factorization (PMF), an advanced and powerful technique for collaborative filtering.<br>
By leveraging PMF, the recommender system captures latent factors within the item-user interaction matrix, enabling it to generate precise and personalized item recommendations. This algorithm takes into account complex patterns and dependencies, ensuring high-quality suggestions that align with the unique preferences and tastes of each customer.

PySuggestify has been equipped with a user-friendly interface, similar to the most popular ones like sklearn/keras. The low-code approach eliminates the need for complex implementation details, allowing users to focus on optimizing the recommendation system to suit their specific needs.

### How it works?
The pysuggestify recommender system operates through a multi-step process to provide accurate predictions for user-item ratings. Here's an overview of how it works:

<p align="center">
  <img src="https://raw.githubusercontent.com/msoczi/pysuggestify/main/img/process.png" />
</p>

1. **Data Preparation:** Initially, pysuggestify takes in user-item interactions data, typically in the form of a user-item matrix with rating values. The majority of cells in this matrix are empty, representing unrated items by users.
2. **Probabilistic Matrix Factorization:** pysuggestify leverages the power of the Probabilistic Matrix Factorization (PMF) algorithm to learn the underlying dependencies between users and items. By decomposing the user-item matrix into latent factors, PMF identifies hidden patterns and captures the essence of user preferences.
3. **Model Training:** Using the PMF algorithm, the recommender system trains the model based on the available user-item ratings. It iteratively optimizes the model parameters to minimize the error between predicted and actual ratings.
4. **Prediction Generation:** Once the model is trained, it can accurately predict the ratings for items that have not yet been rated by a given user. By utilizing the learned dependencies and latent factors, pysuggestify provides personalized rating predictions tailored to individual user preferences.

By following this approach, pysuggestify unlocks the power of PMF algorithm, enabling accurate predictions for missing ratings in the user-item matrix. This allows businesses to offer personalized recommendations and enhance user experiences in various domains, such as movies, products, or content.


## Installation
Use pip to install from pypi:
```sh
pip install pysuggestify
```
or directly from github
```sh
pip install -e git+https://github.com/msoczi/pysuggestify#egg=pysuggestify
```

## Example

```python
from pysuggestify.PMF import PMF

# Load example dataset
ratings = pd.read_csv('data/ratings.csv')

# Defince instance of PMF class
PMF_model = PMF(n_dims = 30)

# Prepare data for modeling.
# Specify dataframe and names of ID columns for users, items, ratings. 
PMF_model.prepare_data(ratings, 'userId', 'movieId', 'rating')

# Fit model
PMF_model.fit(n_epochs=10)

# Get predictions
PMF_model.predict()

# Get predictions for specific user and item
PMF_model.predict_one(user_id=1, item_id=2)

```

**[Here](https://github.com/msoczi/pysuggestify/blob/main/Example.ipynb) is a notebook with example.**

## Contact

Mateusz Soczewka - msoczewkas@gmail.com <br>
<br>
Thank you for any comments. :smiley:

