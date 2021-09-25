#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def price_corr_by_inf(df):
    import category_encoders
    '''
    создает два таргет-энкодинга, скорректированных на лаг базисного ИПЦ для города и региона соответственно
        ('city_avg_price_inf' и 'region_avg_price_inf')
    И ТРЕТЬЮ ПЕРЕМЕННУЮ 'corrected_price' ДЛЯ РАСЧЕТОВ ЦЕН БЛИЖАЙШИХ СОСЕДЕЙ КСЮШИ
    '''
    df[['city_avg_price_inf', 'region_avg_price_inf']] = 0
    at = category_encoders.target_encoder.TargetEncoder(cols = ['city', 'region'], smoothing=1000)
    temp_train = at.fit_transform(df.loc[df.per_square_meter_price.notnull(), ['city', 'region']],
                     np.log(df.loc[df.per_square_meter_price.notnull(), 'per_square_meter_price']) \
                     /df.loc[df.per_square_meter_price.notnull(), 'ipc_base'])
    
    temp_test = at.transform(df.loc[df.per_square_meter_price.isnull(), ['city', 'region']],
                     np.log(df.loc[df.per_square_meter_price.isnull(), 'per_square_meter_price']) \
                 /df.loc[df.per_square_meter_price.isnull(), 'ipc_base'])
    df.loc[df.per_square_meter_price.notnull(), 'city_avg_price_inf'] = temp_train['city']
    
    df.loc[df.per_square_meter_price.notnull(), 'region_avg_price_inf'] = temp_train['region']
    
    df.loc[df.per_square_meter_price.isnull(), 'city_avg_price_inf'] = temp_test['city']
    
    df.loc[df.per_square_meter_price.isnull(), 'region_avg_price_inf'] = temp_test['region']
    
    df.loc[df.per_square_meter_price.notnull(), 'corrected_price'] =     (np.log(df.loc[df.per_square_meter_price.notnull(), 'per_square_meter_price'])     /df.loc[df.per_square_meter_price.notnull(), 'ipc_base'])
    return(df)

