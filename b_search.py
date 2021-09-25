#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
    def deviation_metric_one_sample(y_true: typing.Union[float, int], y_pred: typing.Union[float, int]) -> float:
        """
        Реализация кастомной метрики для хакатона.

        :param y_true: float, реальная цена
        :param y_pred: float, предсказанная цена
        :return: float, значение метрики
        """
        THRESHOLD = 0.15
        NEGATIVE_WEIGHT = 1.1
        deviation = (y_pred - y_true) / np.maximum(1e-8, y_true)
        if np.abs(deviation) <= THRESHOLD:
            return 0
        elif deviation <= - 4 * THRESHOLD:
            return 9 * NEGATIVE_WEIGHT
        elif deviation < -THRESHOLD:
            return NEGATIVE_WEIGHT * ((deviation / THRESHOLD) + 1)**2
        elif deviation < 4 * THRESHOLD:
            return ((deviation / THRESHOLD) - 1)**2
        else:
            return 9


    def deviation_metric(y_true: np.array, y_pred: np.array) -> float:
        return np.array([deviation_metric_one_sample(y_true[n], y_pred[n]) for n in range(len(y_true))]).mean()

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    estimator = ctb.CatBoostRegressor(
        random_state=42
    )
    opt = BayesSearchCV(
        estimator = estimator,
        scoring = make_scorer(deviation_metric, greater_is_better=False),
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
             'od_type' : Categorical(['IncToDec', 'Iter']),
             'scale_pos_weight':Real(0.01, 1.0, 'uniform'),
        }
    )
    opt.fit(train, test)
    return(opt)

