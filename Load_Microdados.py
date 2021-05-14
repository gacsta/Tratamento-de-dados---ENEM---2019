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
micro_dict_na = pd.read_excel(file_dict)
itens_dict_na = pd.read_excel(file_dict, sheet_name='ITENS_PROVA_2019')

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
micro_colunas = micro_dict_na['DICIONÁRIO DE VARIÁVEIS - ENEM 2019'].apply(isvariavel).dropna()


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

#ARMAZENA OS DADOS EM ARQUIVOS PARA POSTERIOR ANÁLISE ATRAVÉS DO MÉTODO PICKLE
pasta_microdados = open(r"Microdados", 'wb')
pasta_itens_provas = open(r'Itens_Provas','wb') 
pasta_dicionarios = open(r'dicionarios','wb')

pickle.dump(microdados, pasta_microdados)
pickle.dump(itens_prova, pasta_itens_provas)
pickle.dump([micro_dict_na, itens_dict_na, micro_colunas], pasta_dicionarios)
