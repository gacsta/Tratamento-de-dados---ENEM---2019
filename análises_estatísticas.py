# -*- coding: utf-8 -*-
"""
Created on Thu May 13 23:25:15 2021

@author: gabr8
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import numpy as np

file = open('Microdados', 'rb')
file2 = open('dicionarios', 'rb')

microdados = pickle.load(file)
dicionarios = pickle.load(file2)

plt.figure(figsize=(10,6))

# Add title
plt.title("Notas_Matemática por idade")

# Bar chart showing average arrival delay for Spirit Airlines flights by month
sns.regplot(x=microdados['NU_NOTA_REDACAO'], y = microdados['NU_NOTA_MT'])

# Add label for vertical axis
plt.ylabel("Nota Redação")
plt.xlabel("Nota Matemática")



