#!/usr/bin/env python
# coding: utf-8

# In[1]:


def build_ctb(train):
    '''
    Возвращает np.array предсказанных значений оптимального catboost для трейна в руб за кв.м.
    '''
    import typing
    import sklearn
    from sklearn.model_selection import KFold
    from sklearn.metrics import make_scorer
    from skopt.space import Real, Categorical, Integer
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from skopt import BayesSearchCV
    import catboost as ctb
    # def b_search(train):
    #     train = train.loc[train.price_type == 1, :]
    #     train = train.drop(['price_type'], axis = 1)    
    #     train = train.drop(['date', 'data_type'], axis = 1)

    #     kf = KFold(n_splits=5, shuffle=True, random_state=42)
    #     estimator = ctb.CatBoostRegressor(
    #         random_state=42,
    #         verbose = 1000
    #     )
    #     opt = BayesSearchCV(
    #         estimator = estimator,
    #         scoring = 'neg_mean_absolute_error',
    #         cv = kf,
    #         n_iter=1,
    #         refit = True,
    #         return_train_score = True,
    #         random_state = 42
    #         search_spaces = {
    #             'iterations': Integer(100, 2000),
    #              'depth': Integer(1, 8),
    #              'learning_rate': Real(0.01, 1.0, 'log-uniform'),
    #              'random_strength': Real(1e-9, 10, 'log-uniform'),
    #              'bagging_temperature': Real(0.0, 1.0),
    #              'border_count': Integer(1, 255),
    #              'l2_leaf_reg': Integer(2, 30),
    #              'od_type' : Categorical(['IncToDec', 'Iter'])
    #         }
    #     )
    #     opt.fit(train.drop('per_square_meter_price', axis = 1), train.loc[:, 'per_square_meter_price'])
    #     return(opt)
    # opt = b_search(train)
    # opt.best_params_
    # OrderedDict([('bagging_temperature', 1.0),
    #              ('border_count', 255),
    #              ('depth', 8),
    #              ('iterations', 1500),
    #              ('l2_leaf_reg', 2),
    #              ('learning_rate', 0.041243686053895036),
    #              ('od_type', 'IncToDec'),
    #              ('random_strength', 1e-09)])

    boost = ctb.CatBoostRegressor(
            random_state=42,
            verbose = 1000,
            iterations = 1500, depth = 8, learning_rate = 0.041243686053895036, random_strength = 1e-09,
            bagging_temperature = 1, border_count = 255, l2_leaf_reg = 2, od_type = 'IncToDec')
    boost1 = ctb.CatBoostRegressor(
            random_state=42,
            verbose = 1000,
            iterations = 1500, depth = 8, learning_rate = 0.041243686053895036, random_strength = 1e-09,
            bagging_temperature = 1, border_count = 255, l2_leaf_reg = 2, od_type = 'IncToDec')
    
    boost.fit(train.loc[train.price_type == 1, train.drop(['per_square_meter_price', 'date', 'data_type','price_type'],
                                                          axis = 1).columns], train.loc[train.price_type == 1,
                                                                                           'per_square_meter_price'])
    
    boost1.fit(train.loc[train.price_type == 1, train.drop(['per_square_meter_price', 'date', 'data_type',
                                                                    'price_type'], axis = 1)\
                 .columns[boost.feature_importances_ > 0.05]], 
               train.loc[train.price_type == 1, 'per_square_meter_price'])
    return(np.exp(boost1.predict(train.loc[train.price_type == 1, train.drop(['per_square_meter_price', 'date', 'data_type',
                                                                    'price_type'], axis = 1)\
                 .columns[boost.feature_importances_ > 0.05]])))

