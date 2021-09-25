import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
import datetime
from itertools import compress
import seaborn as sns; sns.set(rc = {'figure.figsize':(15,8)})


def preprocessing(train, test):
    test['per_square_meter_price'] = np.nan
    train['data_type'] = 'train'
    test['data_type'] = 'test'
    data = train.append(test)
    
    return data

def add_time_values(data):
    data.date = pd.to_datetime(data.date)
    data['month'] = data.date.dt.month
    data['year'] = data.date.dt.year
    data['day'] = data.date.dt.day
    
    return data


# на вход подается датафрейм с номером id и координатами
# на выход bs_nn: дикт с ключами - номерами id и значениями - номерами соседних id
# на выход bs_dist: дикт с ключами - номерами id и значениями - расстояния до соседей
def get_bs_neighbors(id_coords, radius):
    R = 6367000
    id_coords = id_coords.copy()
    id_coords[['lat', 'lng']] = np.radians(id_coords[['lat', 'lng']])
    
    tree = BallTree(id_coords[['lat', 'lng']], leaf_size=40, metric='haversine')
    ind, dist = tree.query_radius(id_coords[['lat', 'lng']], r=radius/R, return_distance=True)
    
    id_nn = {}
    id_dist = {}
    id_coords_values = id_coords['new_id'].values
    
    for id_ind in range(len(ind)):
        nn_mask = ind[id_ind] != id_ind
        nn_ind = ind[id_ind][nn_mask]
        source_id = id_coords_values[id_ind]
        neighbors_id = list(id_coords_values[nn_ind])
        neighbors_dist = list(R * dist[id_ind][nn_mask])
        id_nn[source_id] = neighbors_id
        id_dist[source_id] = neighbors_dist
    
    return id_nn, id_dist



# на вход: дата фрейм целиковый
# дикт с ключами - номерами id и значениями - номера соседей
# дикт с ключами - датами и номерами id и некими значениями
# агрегационная функция
# на выход: лист - колонка в датафрейме
def compute_bs_neighbors_stat(df, bs_nn_dct, feature_dct, func):
    values = []
    for ind in df['new_id'].values: # проходимся по каждому наблюдению (дата - id)
        nearest_bs = bs_nn_dct[ind] # ищем намера соседей, если они есть
        value = [feature_dct[(neighbor)] for neighbor in nearest_bs]
        value = func(value) if value else np.nan
        values.append(value)
        
    return values


def add_neighbours_price(data):
    data_for_coords = data[['id', 'lat', 'lng', 'date', 'per_square_meter_price']]
    data_for_coords = data_for_coords.sort_values(by = 'date')
    data_for_coords['new_id'] = np.arange(data_for_coords.shape[0])
    
    id_coords = data_for_coords[['new_id', 'lat', 'lng']]
    id_nn_100m, _ = get_bs_neighbors(id_coords, radius=100)
    id_nn_300m, _ = get_bs_neighbors(id_coords, radius=300)
    id_nn_1000m, _ = get_bs_neighbors(id_coords, radius=1000)

    for new_id in data_for_coords.new_id:
        mask_100 = [True if i < new_id else False for i in id_nn_100m[new_id]]
        id_nn_100m[new_id] = list(compress(id_nn_100m[new_id], mask_100))
        
        mask_300 = [True if i < new_id else False for i in id_nn_300m[new_id]]
        id_nn_300m[new_id] = list(compress(id_nn_300m[new_id], mask_300))
        
        mask_1000 = [True if i < new_id else False for i in id_nn_1000m[new_id]]
        id_nn_1000m[new_id] = list(compress(id_nn_1000m[new_id], mask_1000))

    # compute mean neaighbors price
    price_dct = data_for_coords.groupby('new_id').per_square_meter_price.sum().to_dict()
    data_for_coords['nn_100m_price'] = compute_bs_neighbors_stat(data_for_coords, id_nn_100m, price_dct, np.nanmean)
    data_for_coords['nn_300m_price'] = compute_bs_neighbors_stat(data_for_coords, id_nn_300m, price_dct, np.nanmean)
    data_for_coords['nn_1000m_price'] = compute_bs_neighbors_stat(data_for_coords, id_nn_1000m, price_dct, np.nanmean)
    data = data.merge(data_for_coords[['id', 'nn_100m_price', 'nn_300m_price', 'nn_1000m_price']], how = 'left')
    
    return data


# на вход: исходные данные и дата фрейм с индексом
# на выход: дата фрейм с двумя новыми колонками mmvb_lag1 и mmvb_lag2
def add_mmvb_index(data, idx_mmvb):
    result = []
    current = datetime.date(2019, 11, 1)    

    while current <= datetime.date(2020, 11, 1)  :
        result.append(current)
        current += relativedelta(months=1)
        
    mmvb = idx_mmvb.iloc[:, :2].rename(columns = {'Дата': 'date', 'Цена': 'mmvb'})
    mmvb['date'] = result[::-1]
    mmvb = mmvb.append({'date': '2020-12-01', 'mmvb': '3107'}, ignore_index=True)
    mmvb.mmvb = mmvb.mmvb.astype(int)
    mmvb.date = pd.to_datetime(mmvb.date)
    mmvb['month'] = mmvb.date.dt.month
    mmvb['year'] = mmvb.date.dt.year
    mmvb = mmvb.sort_values(by = 'date', ascending = False)
    mmvb['mmvb_lag1'] = mmvb.mmvb.shift(-1)
    mmvb['mmvb_lag2'] = mmvb.mmvb.shift(-2)
    data = data.merge(mmvb[['mmvb_lag1', "mmvb_lag2", 'month', 'year']], how = 'left')
    
    return data