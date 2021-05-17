# -*- coding: utf-8 -*-
"""
Created on Thu May 13 23:25:15 2021

@author: gabr8
"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import pandas as pd
import pickle
import numpy as np


with open(r'Particoes', 'rb') as pasta:
   participante, escola, at_espec, at_especif, rec_espec, local, prova_obj, redacao, socioec = pickle.load(pasta)
with open(r'dicionarios','rb') as pasta:
   micro_dict_na, itens_dict_na, micro_colunas = pickle.load(pasta)
# with open(r'Microdados', 'rb') as pasta:
#     microdados = pickle.load(pasta)



#ANÁLISE

#Distirbuição geral da nota descartando as não presenças
#Somando e calculando a média
nota_geral = (redacao['NU_NOTA_REDACAO'].add(prova_obj[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']].sum(axis = 1)))/5
nota_geral.dropna(inplace = True)
#plotando
plt.figure(figsize=(10,7))
sns.distplot(a=nota_geral, kde=False)
plt.title("Diatribuição geral de notas")
plt.xlabel('Nota Geral')
plt.ylabel('Participantes')

#Distirbuição geral da nota de todos as inscrições
#Somando e calculando a média
nota_geral_np = (redacao['NU_NOTA_REDACAO'].fillna(0).add(prova_obj[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']].fillna(0).sum(axis = 1)))/5
#plotando
plt.figure(figsize=(10,7))
sns.displot(x=nota_geral_np, label = 'Desconsiderando faltas')
plt.title("Diatribuição geral de notas")
plt.xlabel('Nota Geral')
plt.ylabel('Participantes')




#Análise da presenca e elimnação nas provas
#Monatagem da tabela de presença a partir do mapeamento com um dicionário
presenca_dict = {1:'Presente',
                 2:'Eliminado',
                 0:'Faltou'}
presenca_list = ['TP_PRESENCA_CN', 'TP_PRESENCA_CH','TP_PRESENCA_MT','TP_PRESENCA_LC']
presenca = microdados.filter(items = presenca_list , axis = 1).replace(presenca_dict).value_counts()
presenca.names = ['Ciencias Naturais', 'Ciencias Humanas', 'Matemática', 'Linguagens e Códigos']

#Exporta a tabela para uma planilha de excel para melhor visualização
with pd.ExcelWriter('Tabela_Presenca.xlsx',
                    mode='w') as writer:  
    presenca.to_excel(writer, sheet_name='Presenca em cada prova')



#Maiores dificuldades
#Criando um dataframe para as disciplinas
disciplinas = pd.concat([prova_obj[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']], redacao['NU_NOTA_REDACAO']], axis = 1)
disciplinas.columns=['Ciêcias Naturais','Ciências Humanas', 'Linguagens e Codigos','Matemática', 'Nota Redação']
#Plotando um gráfico com barras
sns.barplot(x=disciplinas.colmuns, y=disciplinas)
mean_discplinas = disciplinas.mean(axis = 0)
plt.title("Performance por área disciplinar")



#Distribuição dos status da redação
status_redacao = redacao['TP_STATUS_REDACAO'].dropna().value_counts()

legenda = ['1 - Sem problemas - {}'.format(status_redacao[1]),
'2 - Anulada - {}'.format(status_redacao[2]),
'3 - Cópia Texto Motivador - {} '.format(status_redacao[3]),
'4 - Em Branco - {}'.format(status_redacao[4]),
'6- Fuga ao tema - {}'.format(status_redacao[6]),
'7 - Não atendimento ao tipo textual - {}'.format(status_redacao[7]),
'8 - Texto insuficiente - {}'.format(status_redacao[8]),
'9 - Parte desconectada - {}'.format(status_redacao[9])]

#Plotando o gráfico com barras em diferentes cores
color = ('b', 'g', 'r' ,'c', 'm', 'y', 'k', 'yellow' )
cmap = dict(zip(status_redacao, color))
patches = [Patch(color=v, label=k) for k, v in cmap.items()]
sns.barplot(x=status_redacao.index, y=status_redacao, palette = color)
plt.ylabel('Número de ocorrências')
plt.legend(title="Diatribuição geral do status da redação", labels=legenda, handles=patches, bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0, fontsize=15, frameon=False)



#Distribuição dos status da redação (ocorrências anormais)
status_redacao_an = redacao['TP_STATUS_REDACAO'].dropna().value_counts().drop(1, axis = 0)

legenda = [
'2 - Anulada - {}'.format(status_redacao_an[2]),
'3 - Cópia Texto Motivador - {} '.format(status_redacao_an[3]),
'4 - Em Branco - {}'.format(status_redacao_an[4]),
'6- Fuga ao tema - {}'.format(status_redacao_an[6]),
'7 - Não atendimento ao tipo textual - {}'.format(status_redacao_an[7]),
'8 - Texto insuficiente - {}'.format(status_redacao_an[8]),
'9 - Parte desconectada - {}'.format(status_redacao_an[9])]

#Plotando o gráfico com barras em diferentes cores
color = ('g', 'r' ,'c', 'm', 'y', 'k', 'yellow')
cmap = dict(zip(status_redacao_an, color))
patches = [Patch(color=v, label=k) for k, v in cmap.items()]
sns.barplot(x=status_redacao_an.index, y=status_redacao_an, palette = color)
plt.ylabel('Número de ocorrências')
plt.legend(title="Diatribuição geral do status da redação", labels=legenda, handles=patches, bbox_to_anchor=(1.04, 0.5), loc='center left', borderaxespad=0, fontsize=15, frameon=False)






#CORRELAÇÕES ENTRE A NOTA EM DIFERENTES MATÉRIAS E DIVERSAS VARIÁVEIS
#OBJETIVO : TENTAR ACHAR FATORES DETERMINANTES PARA ALTA E BAIXA PERFORMANCE NO EXAME

#Criando um dataframe cuja as colunas representam variáveis as quais hipoteticamente influenciam a nota final
nota_influ = [prova_obj[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']], redacao, socioec[['Q024', 'Q025', 'Q022','Q006','Q001', 'Q002']],participante[['NU_IDADE','TP_ST_CONCLUSAO', 'IN_TREINEIRO', 'TP_ENSINO']], nota_geral.to_frame()]       
nota_influ = pd.concat(nota_influ, axis = 1)

#Transformando variáveis categoricas ordinais para a compatibilidade com o método de correlação
ordem = {'A' : 0,
'B' : 1,
'C' : 2,
'D' : 3,
'E' : 4,
'F' : 5,
'G' : 6,
'H' : None
}

ordem2 = {'A' : 0,
'B' : 1,
'C' : 2,
'D' : 3,
'E' : 4,
'F' : 5,
'G' : 6,
'H' : 7,
'I' : 8,
'J' : 9,
'K' : 10,
'L' : 11,
'M': 12,
'N': 13,
'O' : 14,
'P' : 15,
'Q' : 16  
}

nota_influ.Q006.replace(ordem2, inplace = True)

for categoria in ['Q024', 'Q025', 'Q022','Q001', 'Q002']:
    nota_influ[categoria].replace(ordem, inplace = True)

    
#Gerando a matriz correlação entre todas as colunas do dataframe em forma de heatmap
corr_spe = nota_influ.corr(method = 'spearman')
corr_pea = nota_influ.corr(method = 'pearson')
corr_ken = nota_influ.corr(method = 'kendall')

#Atualizando as colunas com a informação das variáveis
corr_ken.columns = corr_ken.index = nota_influ.columns = ['Ciêcias Naturais','Ciências Humanas', 'Linguagens e Codigos','Matemática', 'Status da Redação', 'Redação Competência 1', 'Redação Competência 2', 'Redação Competência 3', 'Redação Competência 4', 'Redação Competência 5', 'Nota da Redação', 'Computador na residência','Acesso à internet','Possui celular', 'Renda Mensal', 'Escolaridade do pai', 'Escolaridade da mãe', 'Idade', 'Conclusão Ensino Médio', 'Treineiro', 'Tipo de Ensino', 'Nota Geral' ]
plt.figure(figsize=(12,9))  
sns.heatmap(corr_ken, vmin=-1, vmax=1)




#Inferências a respeito da performance e suas correlações:         
        
#Acesso a informação e notas 

#Acesso a um computador e Redação x internet
plt.figure(figsize=(12,9))    
sns.boxplot(x = nota_influ.Q024  , y = redacao.NU_NOTA_REDACAO, hue = nota_influ.Q025)
plt.title("Redação x Número de computadores")
plt.ylabel('Redação')
plt.xlabel('Número de Computadores')

acess_info = sns.FacetGrid(nota_influ, col="Q025", height=5)
acess_info.map_dataframe(sns.regplot, x ='Q024' , y = 'NU_NOTA_REDACAO', x_estimator=np.mean, marker="+")

acess_info.axes[0,0].set_xlabel('Número de Computadores')
acess_info.axes[0,0].set_ylabel('Nota da Redação')
acess_info.axes[0,1].set_xlabel('Número de Computadores')
acess_info.axes[0,1].set_ylabel('Nota da Redação')
acess_info.axes[0,0].set_title('Sem acesso à internet')
acess_info.axes[0,1].set_title('Com acesso à internet')

        #Renda Mensal e Redação
plt.figure(figsize=(13,7))    
sns.boxplot( x = nota_influ['Q006']  , y = redacao['NU_NOTA_REDACAO'])
plt.title("Redação x Renda Mensal")
plt.ylabel('Redação')
plt.xlabel('Renda Mensal')

        #Ciências Humanas e Redação
plt.figure(figsize=(17,13))    
sns.regplot( x = nota_influ['NU_NOTA_CH']  , y = redacao['NU_NOTA_REDACAO'], marker="+")
plt.xlabel('Ciências Humanas')
plt.ylabel('Redação')
plt.title("Linguagens e Codigos, Ciencias Humanas e Redação")

        #linguagens e Codigoss e Redação
plt.figure(figsize=(17,13))    
sns.regplot( x = nota_influ['NU_NOTA_LC']  , y = redacao['NU_NOTA_REDACAO'], marker="+")
plt.xlabel('Linguagens e Códigos')
plt.ylabel('Redação')
plt.title("Linguagens e Codigos, Ciencias Humanas e Redação")

  
    #Nota de cada disciplina pela renda mensal
unstacked = pd.DataFrame(disciplinas.unstack()).reset_index()
unstacked.columns = ['Disciplina', 'Disciplina_Index', 'Nota']
plot_data = pd.merge(unstacked, nota_influ['Renda Mensal'], left_on = 'Disciplina_Index', right_index = True)
renda_nota = sns.FacetGrid(plot_data, col='Disciplina', col_wrap = 3, aspect = 1.06)
renda_nota.map_dataframe(sns.boxplot, x ='Renda Mensal'  , y = 'Nota')

   