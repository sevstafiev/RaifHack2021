#!/usr/bin/env python
# coding: utf-8

# In[9]:


def add_extra(train, test, path = 'C:/Users/nicka/OneDrive/Рабочий стол/raifhack/estate_sber_data/'):
    '''
    train = трейн-часть сета
    test = тест-часть сета
    path = путь до файлов estate_sber_data.xlsx и rosstat_cbr.xlsx
    '''
    path_estate = path + 'estate_sber_data.xlsx'
    path_ros_cbr = path + 'rosstat_cbr.xlsx'
    data1 = pd.read_excel(path_estate)
    data2 = pd.read_excel(path_ros_cbr)
    data1['year'] = data1.date.apply(lambda x: x.year)
    data1['month'] = data1.date.apply(lambda x: x.month)
    data2['year'] = data2.date.apply(lambda x: x.year)
    data2['month'] = data2.date.apply(lambda x: x.month)
              
    def find_number(df, sub_column):
        # inplace появление колонки с кодом
        ### ЕСТЬ АЛТАЙСКИЙ КРАЙ (22) И РЕСПУБЛИКА АЛТАЙ (4)
        df.loc[df[sub_column].str.contains('Адыг'), 'Код'] = 1
        df.loc[(df[sub_column].str.contains('лтай')), 'Код'] = 4 # & (df[sub_column].str.contains('еспублик'))
        df.loc[df[sub_column].str.contains('Башкорт'), 'Код'] = 2
        df.loc[df[sub_column].str.contains('Бурят'), 'Код'] = 3
        df.loc[df[sub_column].str.contains('Дагест'), 'Код'] = 5
        df.loc[df[sub_column].str.contains('Ингуш'), 'Код'] = 6
        df.loc[df[sub_column].str.contains('Кабард'), 'Код'] = 7
        df.loc[df[sub_column].str.contains('Калмык'), 'Код'] = 8
        df.loc[df[sub_column].str.contains('Карачаев'), 'Код'] = 9
        df.loc[df[sub_column].str.contains('Карел'), 'Код'] = 10
        df.loc[df[sub_column].str.contains('Коми'), 'Код'] = 11
        df.loc[df[sub_column].str.contains('Крым'), 'Код'] = 91
        df.loc[df[sub_column].str.contains('Марий'), 'Код'] = 12
        df.loc[df[sub_column].str.contains('Мордов'), 'Код'] = 13
        df.loc[df[sub_column].str.contains('Якут'), 'Код'] = 14
        df.loc[df[sub_column].str.contains('Осети'), 'Код'] = 15
        df.loc[df[sub_column].str.contains('Татар'), 'Код'] = 16
        df.loc[df[sub_column].str.contains('Тыва'), 'Код'] = 17
        df.loc[df[sub_column].str.contains('Удмурт'), 'Код'] = 18
        df.loc[df[sub_column].str.contains('Хакас'), 'Код'] = 19
        df.loc[df[sub_column].str.contains('Чечен'), 'Код'] = 20
        df.loc[df[sub_column].str.contains('Чуваш'), 'Код'] = 21
        df.loc[(df[sub_column].str.contains('лтай')) & (df[sub_column].str.contains('рай')), 'Код'] = 22
        df.loc[df[sub_column].str.contains('байкал'), 'Код'] = 75
        df.loc[df[sub_column].str.contains('Камчат'), 'Код'] = 41
        df.loc[df[sub_column].str.contains('Краснодар'), 'Код'] = 23
        df.loc[df[sub_column].str.contains('Краснояр'), 'Код'] = 24
        df.loc[df[sub_column].str.contains('Перм'), 'Код'] = 59
        df.loc[df[sub_column].str.contains('Примор'), 'Код'] = 25
        df.loc[df[sub_column].str.contains('Ставропол'), 'Код'] = 26
        df.loc[df[sub_column].str.contains('Хабаров'), 'Код'] = 27
        df.loc[df[sub_column].str.contains('Амур'), 'Код'] = 28
        df.loc[df[sub_column].str.contains('Архангел'), 'Код'] = 29
        df.loc[df[sub_column].str.contains('Астрахан'), 'Код'] = 30
        df.loc[df[sub_column].str.contains('Белгород'), 'Код'] = 31
        df.loc[df[sub_column].str.contains('Брянск'), 'Код'] = 32
        df.loc[df[sub_column].str.contains('Владимир'), 'Код'] = 33
        df.loc[df[sub_column].str.contains('Волгоград'), 'Код'] = 34
        df.loc[df[sub_column].str.contains('Вологод'), 'Код'] = 35
        df.loc[df[sub_column].str.contains('Воронеж'), 'Код'] = 36
        df.loc[df[sub_column].str.contains('Иванов'), 'Код'] = 37
        df.loc[df[sub_column].str.contains('Иркутск'), 'Код'] = 38
        df.loc[df[sub_column].str.contains('Калинин'), 'Код'] = 39
        df.loc[df[sub_column].str.contains('Калуж'), 'Код'] = 40
        df.loc[df[sub_column].str.contains('Кемеров'), 'Код'] = 42
        df.loc[df[sub_column].str.contains('Киров'), 'Код'] = 43
        df.loc[df[sub_column].str.contains('Костром'), 'Код'] = 44
        df.loc[df[sub_column].str.contains('Курган'), 'Код'] = 45
        df.loc[df[sub_column].str.contains('Курск'), 'Код'] = 46
        df.loc[df[sub_column].str.contains('Ленин'), 'Код'] = 47
        df.loc[df[sub_column].str.contains('Липецк'), 'Код'] = 48
        df.loc[df[sub_column].str.contains('Магадан'), 'Код'] = 49
        df.loc[df[sub_column].str.contains('Моско'), 'Код'] = 50
        df.loc[df[sub_column].str.contains('Мурман'), 'Код'] = 51
        df.loc[df[sub_column].str.contains('Нижегород'), 'Код'] = 52
        df.loc[df[sub_column].str.contains('Новгород'), 'Код'] = 53
        df.loc[df[sub_column].str.contains('Новосиб'), 'Код'] = 54
        df.loc[df[sub_column].str.contains('Омск'), 'Код'] = 55
        df.loc[df[sub_column].str.contains('Оренбург'), 'Код'] = 56
        df.loc[df[sub_column].str.contains('Орлов'), 'Код'] = 57
        df.loc[df[sub_column].str.contains('Пенз'), 'Код'] = 58
        df.loc[df[sub_column].str.contains('Псков'), 'Код'] = 60
        df.loc[df[sub_column].str.contains('Ростов'), 'Код'] = 61
        df.loc[df[sub_column].str.contains('Рязан'), 'Код'] = 62
        df.loc[df[sub_column].str.contains('Самар'), 'Код'] = 63
        df.loc[df[sub_column].str.contains('Саратов'), 'Код'] = 64
        df.loc[df[sub_column].str.contains('Сахалин'), 'Код'] = 65
        df.loc[df[sub_column].str.contains('Свердлов'), 'Код'] = 66
        df.loc[df[sub_column].str.contains('Смоленск'), 'Код'] = 67
        df.loc[df[sub_column].str.contains('Тамбов'), 'Код'] = 68
        df.loc[df[sub_column].str.contains('Тверск'), 'Код'] = 69
        df.loc[df[sub_column].str.contains('Томск'), 'Код'] = 70
        df.loc[df[sub_column].str.contains('Тульск'), 'Код'] = 71
        df.loc[df[sub_column].str.contains('Тюмен'), 'Код'] = 72
        df.loc[df[sub_column].str.contains('Ульяновск'), 'Код'] = 73
        df.loc[df[sub_column].str.contains('Челяб'), 'Код'] = 74
        df.loc[df[sub_column].str.contains('Ярослав'), 'Код'] = 76
        df.loc[df[sub_column].str.contains('байкал'), 'Код'] = 75
        df.loc[df[sub_column].str.contains('Москва'), 'Код'] = 77
        df.loc[df[sub_column].str.contains('Санкт'), 'Код'] = 78
        df.loc[df[sub_column].str.contains('Севастоп'), 'Код'] = 92
        df.loc[df[sub_column].str.contains('Еврейс'), 'Код'] = 79
        df.loc[df[sub_column].str.contains('Ненец'), 'Код'] = 83
        df.loc[df[sub_column].str.contains('Ханты'), 'Код'] = 86
        df.loc[df[sub_column].str.contains('Чукот'), 'Код'] = 87
        df.loc[df[sub_column].str.contains('Ямало'), 'Код'] = 89
        df['Код'] = df['Код'].astype(np.int64)
        return(df)
    
    train = find_number(train, 'region')
    test = find_number(test, 'region')
    df = pd.concat([train, test])
    df = df.reset_index(drop = True)
    df['year'] = df.date.apply(lambda x: np.int64(x.split('-')[0]))
    df['month'] = df.date.apply(lambda x: np.int64(x.split('-')[1]))
             
    for i in df['Код'].unique():
        for k in df.loc[df['Код'] == i, 'month'].unique():
            if k != 1:
                df.loc[(df['Код'] == i) & (df['month'] == k), 'number_of_supply1'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[0].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'number_of_supply2'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[1].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'price_dynamic1'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[2].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'price_dynamic2'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[3].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'mean_sqm_price1'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[4].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'mean_sqm_price2'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[5].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'exp_time'] =                 data1.loc[(data1.month == (k-1)) & (data1.year == 2020), data1.columns == i].iloc[6].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_all_month'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[3].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_all_year'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[4].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_goods_month'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[5].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_goods_year'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[6].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_build_month'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[7].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_build_year'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[8].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'miacr'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[9].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_base'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[10].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_chain'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[11].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'interest_rate'] =                 data2.loc[(data2.month == (k-1)) & (data2.year == 2020), data2.columns == i].iloc[12].values[0]
            else:
                df.loc[(df['Код'] == i) & (df['month'] == k), 'number_of_supply1'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[0].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'number_of_supply2'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[1].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'price_dynamic1'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[2].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'price_dynamic2'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[3].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'mean_sqm_price1'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[4].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'mean_sqm_price2'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[5].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'exp_time'] =                 data1.loc[(data1.month == 12) & (data1.year == 2019), data1.columns == i].iloc[6].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_all_month'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[3].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_all_year'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[4].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_goods_month'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[5].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_goods_year'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[6].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_build_month'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[7].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_build_year'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[8].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'miacr'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[9].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_base'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[10].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'ipc_chain'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[11].values[0]

                df.loc[(df['Код'] == i) & (df['month'] == k), 'interest_rate'] =                 data2.loc[(data2.month == 12) & (data2.year == 2019), data2.columns == i].iloc[12].values[0]
    df = df.drop(['Код', 'year', 'month'], axis = 1)
    return(df)

