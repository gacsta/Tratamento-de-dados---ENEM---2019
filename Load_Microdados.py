# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:34:11 2021

@author: gabr8
"""

from tqdm import tqdm
import pandas as pd
import pickle
import numpy as np

#Diretório dos dados
file_micro = r'C:\Users\gabr8\Downloads\microdados_enem_2019\DADOS\MICRODADOS_ENEM_2019.csv'
file_itens = r'C:\Users\gabr8\Downloads\microdados_enem_2019\DADOS\ITENS_PROVA_2019.csv'
file_dict = r'C:\Users\gabr8\Downloads\microdados_enem_2019\DICIONÁRIO\Dicionário_Microdados_Enem_2019.xlsx'

#Lendo ambos os arquivos CSV com pandas
itens_prova = pd.read_csv(file_itens, encoding = 'latin_1', sep = ';')
microdados = pd.read_csv(file_micro, encoding='latin_1', sep = ';', header = 40, chunksize=1000)

#Armazenando seus respectivos dicionários em Dataframes para acessar os nomes de todas as features (colunas)
micro_dict_na = pd.read_excel(file_dict).reset_index(drop = True)
itens_dict_na = pd.read_excel(file_dict, sheet_name='ITENS_PROVA_2019').reset_index(drop = True)
 
#Função que reconhece se a entrada do dicionário realmente representa uma variável ou não
#Limpa os excessos do arquivo com origem .xls (Excel)
def isvariavel(variavel):
    if type(variavel) == str :
        if ' ' in variavel:
            return None
        else:
            return variavel
    else:
        return None
    
#Dataframe de todas as colunas dos microdados    
micro_colunas = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'].apply(isvariavel).dropna().reset_index(drop=True)


#DEVIDO À QUANTIDADE DE MEMÓRIA NECESSÁRIA PARA A ALOCAÇÃO DO ARQUIVO 'MICRODADOS' INTEIRO,
#SER MAIOR DO QUE A RAM ATUALMENTE DISPONÍVEL NA MÁQUINA QUE POSSUO, A LEITURA E ARMAZENAMENTO 
#DOS DADOS EM UM DATAFRAME FOI FEITA EM PEDAÇOS (CHUNKS), SEGUE O MÉTODO UTILIZADO:

#Lê 500000 datapoints por iteração     
chunksize = 500000

#Lista para armazenar os chunks gerados a cada iteração
microdados_list = []

#A cada iteração do loop se é adicionado um chunk à lista
for df_chunk in tqdm(pd.read_csv(file_micro, chunksize=chunksize, encoding = 'latin_1', sep=';', usecols = micro_colunas)):
    
    microdados_list.append(df_chunk) 

#Junta todos os pedaços da lista e os transforma em um DataFrame
microdados = pd.concat(microdados_list)

#Libera a memória ao deletar a lista e o pedaço restante do loop
del microdados_list
del df_chunk

#CATEGORIZANDO E PARTICIONANDO OS DADOS PARA AGILIZAÇÃO DO CÓDIGO E ANÁLISE
participante = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][4:68].dropna().reset_index(drop = True).values, axis = 1)

escola = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][69:87].dropna().reset_index(drop = True).values, axis = 1)

at_espec = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][88:114].dropna().reset_index(drop = True).values, axis = 1)

at_especif = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][115:123].dropna().reset_index(drop = True).values, axis = 1)

rec_espec = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][124:192].dropna().reset_index(drop = True).values, axis = 1)

local = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][193:201].dropna().reset_index(drop = True).values, axis = 1)

prova_obj = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][202:270].dropna().reset_index(drop = True).values, axis = 1)

redacao = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][271:285].dropna().reset_index(drop = True).values, axis = 1)

socioec = microdados.filter(items = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'][286:430].dropna().reset_index(drop = True).values, axis = 1)

particoes = [participante, escola, at_espec, at_especif, rec_espec, local, prova_obj, redacao, socioec]


#ARMAZENA OS DADOS EM ARQUIVOS PARA POSTERIOR ANÁLISE ATRAVÉS DO MÉTODO PICKLE
with open(r"Microdados", 'wb') as pasta:
    pickle.dump(microdados, pasta, protocol=pickle.HIGHEST_PROTOCOL)
with open(r'Particoes', 'wb') as pasta:
    pickle.dump(particoes, pasta, protocol=pickle.HIGHEST_PROTOCOL)
with open(r'Itens_Provas','wb') as pasta:
    pickle.dump(itens_prova, pasta)
with open(r'dicionarios','wb') as pasta:
    pickle.dump([micro_dict_na, itens_dict_na, micro_colunas], pasta)


