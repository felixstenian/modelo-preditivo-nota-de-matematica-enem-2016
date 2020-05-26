# -*- coding: utf-8 -*-
"""Codenation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c5NDM5Di8NfSwRHRXEFrmrmwcQYMhko2
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn import ensemble
from sklearn import tree

df = pd.read_csv("train.csv")



df['SG_UF_RESIDENCIA'].unique()

#var_numb_test = df_test.select_dtypes(include=['int64', 'float64'])
#var_numb_train = df_train.select_dtypes(include=['int64', 'float64'])

variaveis = ['SG_UF_RESIDENCIA',
             'NU_IDADE',
             'TP_SEXO',
             'TP_COR_RACA',
             'TP_NACIONALIDADE',
             'TP_ST_CONCLUSAO',
             'TP_ANO_CONCLUIU',
             'TP_ESCOLA',
             'TP_ENSINO',
             'IN_TREINEIRO',
             'TP_DEPENDENCIA_ADM_ESC',
             'IN_BAIXA_VISAO',
             'IN_CEGUEIRA',
             'IN_SURDEZ',
             'IN_DISLEXIA',
             'IN_DISCALCULIA',
             'IN_SABATISTA',
             'IN_GESTANTE',
             'IN_IDOSO',
             'TP_PRESENCA_CN',
             'TP_PRESENCA_CH',
             'TP_PRESENCA_LC',
             'CO_PROVA_CN',
             'CO_PROVA_CH',
             'CO_PROVA_LC',
             'CO_PROVA_MT',
             'NU_NOTA_CN',
             'NU_NOTA_CH',
             'NU_NOTA_LC',
             'TP_LINGUA',
             'TP_STATUS_REDACAO',
             'NU_NOTA_COMP1',
             'NU_NOTA_COMP2',
             'NU_NOTA_COMP3',
             'NU_NOTA_COMP4',
             'NU_NOTA_COMP5',
             'NU_NOTA_REDACAO'
]

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
plt.figure(figsize=(20,20))
sns.heatmap(df_test[variaveis_numericas].corr(), annot=True, linewidths=0.5, linecolor='black', cmap='Blues')
plt.xticks(rotation=90)
plt.show()

target = 'NU_NOTA_MT'

categorias = ['TP', 'SG', 'CO']
variaveis_categoricas = [i for i in variaveis if i[:2] in categorias]
variaveis_numericas = list(set(variaveis) - set(variaveis_categoricas))

#Removendo inscritos com todas as colunas vazias
df = df.loc[(df['NU_NOTA_CN'].notnull()) & (df['NU_NOTA_CH'].notnull()) & (df['NU_NOTA_LC'].notnull()) & (df['NU_NOTA_REDACAO'].notnull()) & (df['NU_NOTA_MT'].notnull())]

df.dropna(how = 'all', subset=[target])

df[variaveis_categoricas] = df[variaveis_categoricas].fillna(-1).astype(str)
df[variaveis_numericas] = df[variaveis_numericas].fillna(-1)
df = df.reset_index(drop=True)

onehot = preprocessing.OneHotEncoder( sparse=False, handle_unknown='ignore' )
onehot.fit(df[variaveis_categoricas])

df_onehot = pd.DataFrame(onehot.transform(df[variaveis_categoricas]), columns=onehot.get_feature_names(variaveis_categoricas))

#Juntando as variaveis
df_train = pd.concat([df[variaveis_numericas], df_onehot], axis=1, ignore_index=True)

df_train.isna().sum()

regressao = tree.DecisionTreeRegressor(max_depth=12, min_samples_leaf=5)

regressao.fit(df_train, df[target])

features = df_train.columns.tolist()

#Salvando modelo
modelo = pd.Series([variaveis_numericas, variaveis_categoricas, features, regressao, onehot], index=['variaveis_numericas', 'variaveis_categoricas', 'features', 'modelo', 'onehot'])

modelo.to_pickle('modelo.pkl')

list(modelo)

df_result = [variaveis_categoricas, variaveis_numericas]

df_result[modelo[variaveis_categoricas]]

