# -*- coding: utf-8 -*-
"""
Created on Sun May 16 17:14:08 2021

@author: gabr8
"""

#ANÁLISE DE GABARITO


import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import pandas as pd
import pickle
import numpy as np

with open(r'Itens_Provas', 'rb') as pasta:
    itens_prova = pickle.load(pasta)
       
with open(r'Microdados', 'rb') as pasta:
     microdados = pickle.load(pasta)
     
habilidades_col= ['SG_AREA','CO_POSICAO', 'CO_PROVA', 'CO_HABILIDADE', 'TP_LINGUA']
respostas_col = ['TX_RESPOSTAS_CN', 
'TX_RESPOSTAS_CH',
'TX_RESPOSTAS_LC',
'TX_RESPOSTAS_MT']

gabarito_col =[
'TX_GABARITO_CN',
'TX_GABARITO_CH',
'TX_GABARITO_LC',
'TX_GABARITO_MT', 'CO_PROVA'
]

codigo_col = ['CO_PROVA_CN', 'CO_PROVA_CH', 'CO_PROVA_LC', 'CO_PROVA_MT']
lingua_col = ['TP_LINGUA']


habilidades = itens_prova.filter(items = habilidades_col, axis = 1).fillna(2)
respostas = microdados.filter(items = respostas_col + codigo_col + lingua_col, axis  =1).dropna()
gabarito = microdados.filter(items = gabarito_col, axis  =1).dropna()

#CONTANDO AS HABILIDADES DAS QUESTÕES CUJO OS CANDIDATOS ERRARAM

#Contando os erros

count = []
erros_count = pd.DataFrame([])
err_hab = pd.DataFrame([])
acerto_count = pd.DataFrame([])
habil_cert =  pd.DataFrame([])
habil_err =  pd.DataFrame([])
todas_habil_cert  = pd.DataFrame([])
todas_habil_err = pd.DataFrame([])

#Iterando pelas disciplinas
for coluna_res, coluna_gab, coluna_cod in zip(respostas_col, gabarito_col, codigo_col):
     
    #iterando pelos gabaritos, repostas, codigos e lingua dos candidatos
    for string_res, string_gab, codigo_res, lingua in zip(respostas[coluna_res], gabarito[coluna_gab], respostas[coluna_cod], respostas['TP_LINGUA']):
        
            #Criando uma lista booleana onde True = acerto e False = erro para cada cartela de cada candidato que passa pela iteração
            count = [True if item_res == item_gab else False for item_res, item_gab in zip(string_res, string_gab)] 
            count = pd.DataFrame(count)
                
            #COLETANDO O CÓDIGO DAS RESPOSTAS A SEREM ANALISADAS
            filter_cod = habilidades['CO_PROVA'].isin([codigo_res])
            #COLETANDO O TIPO DE LINGUA DA PROVA DO CANDIDATO
            filter_lingua =  habilidades['TP_LINGUA'].isin([lingua, 2])
            #FILTRANDO AS HABILIDADES REFERENTES À PROVA DO CANDIDATO
            string_hab = habilidades[filter_cod & filter_lingua].sort_values(by=['CO_POSICAO'])
            #PAREANDO O RESULTADO DAS QUESTOES COM A LISTA DE HABILIDADES DAS MESMAS
            count = pd.concat([count, string_hab['CO_HABILIDADE'].reset_index( drop = True)], axis = 1)
            #FILTRO PARA AS QUESTOES ERRADAS
            false_filter = count[0].isin([False])
            #FILTRO PARA AS QUESTOES ACERTADAS 
            true_filter = count[0].isin([True])
            #FILTRANDO AS QUESTOES ERRADAS E CERTAS
            count1 = count[false_filter]
            count2 = count[true_filter]
            #ARMAZENANDO DADOS DO CANDIDATO EM UM DATAFRAME
            erros_count = pd.concat([erros_count, count['CO_HABILIDADE']], axis = 0)
            acerto_count = pd.concat([acerto_count, count2['CO_HABILIDADE']], axis = 0)
            
    #Contando a frequência com que os candidatos erram as habilidades específicas de cada disciplina      
    habil_cert = erros_count.value_counts()
    habil_err = acerto_count.value_counts()
    todas_habil_cert = pd.concat([todas_habil_cert.reset_index( drop = True), habil_cert.reset_index( drop = True)], axis = 1)
    todas_habil_err = pd.concat([todas_habil_err.reset_index( drop = True), habil_err.reset_index( drop = True)], axis = 1)
         
      


