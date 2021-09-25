#!/usr/bin/env python
# coding: utf-8

# In[1]:


import typing
import numpy as np
from sklearn.metrics import  r2_score, mean_squared_error
from sklearn.model_selection import KFold
from sklearn.metrics import make_scorer
from skopt.space import Real, Categorical, Integer
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
from skopt import BayesSearchCV
import catboost as ctb
import joblib

def b_search(train, test, with_correction = True):
    '''
    with_correction - применять ли коррекцию для переменных с price_type = 0
    '''
    if with_correction == True:
        train.loc[train.price_type == 0, 'per_square_meter_price'] =             (train.loc[train.price_type == 0, 'per_square_meter_price'] + 13)/2.23
        train = train.drop('price_type', axis = 1)
        
    train = train.drop(['date', 'data_type'], axis = 1)
    test = test.drop(['date', 'data_type'], axis = 1)
 
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    estimator = ctb.CatBoostRegressor(
        random_state=42,
        verbose = 1000
    )
    opt = BayesSearchCV(
        estimator = estimator,
        scoring = 'neg_mean_absolute_error',
        cv = kf,
        n_iter=500,
        refit = True,
        return_train_score = True,
        random_state = 42,
        search_spaces = {
            'iterations': Integer(10, 2000),
             'depth': Integer(1, 8),
             'learning_rate': Real(0.01, 1.0, 'log-uniform'),
             'random_strength': Real(1e-9, 10, 'log-uniform'),
             'bagging_temperature': Real(0.0, 1.0),
             'border_count': Integer(1, 255),
             'l2_leaf_reg': Integer(2, 30),
             'od_type' : Categorical(['IncToDec', 'Iter'])
        }
    )
    opt.fit(train.drop('per_square_meter_price', axis = 1), train.loc[:, 'per_square_meter_price'])
    return(opt)

