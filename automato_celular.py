# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 23:30:08 2021

@author: danie
"""

import random
import numpy
import matplotlib.pyplot as plt

def condicao_inicial(CA_Y, CA_X, pct_ocupacao_inicial):
    CA_matriz_0 =  numpy.zeros((CA_Y, CA_X))
    CA_matriz_1 =  numpy.zeros((CA_Y, CA_X))
    for j in range(0, CA_Y):
        for i in range(0, CA_X):
            value = random.randint(0, 100)
            #p = j * CA_X + i + 1
            #if p % 2 == 0:
            #    CA_matriz_0[j][i] = 1
            if value < pct_ocupacao_inicial:
                CA_matriz_0[j][i] = 1
                CA_matriz_1[j][i] = 1
            
    return CA_matriz_0, CA_matriz_1

def matriz_atributos(CA_Y, CA_X):
    CA_atributo_transporte = numpy.zeros((CA_Y, CA_X))
    CA_atributo_saude = numpy.zeros((CA_Y, CA_X))
    CA_atributo_educacao = numpy.zeros((CA_Y, CA_X))
    CA_atributo_salario = numpy.zeros((CA_Y, CA_X))
    CA_atributo_escolaridade = numpy.zeros((CA_Y, CA_X))
    
    lista_atributos = [CA_atributo_transporte,
                       CA_atributo_saude,
                       CA_atributo_educacao,
                       CA_atributo_salario,
                       CA_atributo_escolaridade]
    
    for atributo in lista_atributos:
        for j in range(0, CA_Y):
            for i in range(0, CA_X):
                atributo[j,i] = random.random()
                
    return lista_atributos

def media_atributos(j,i):
    valor_total = 0
    for atributo in lista_atributos:
        valor_total = (valor_total + atributo[j][i])
    valor_media = (valor_total / len(lista_atributos))
    return valor_media


CA_X = int(input('Digite o tamanho da malha desejada (em células):\n'))
CA_Y = CA_X
pct_ocupacao_inicial = int(input('Digite a porcentagem inicial de ocupação da malha:\n'))
qtd_iteracoes = int(input('Digite a quantidade de iterações:\n'))
epsilon = float(input('Defina ε (entre 0 e 1):\n'))

#%%

lista_atributos = matriz_atributos(CA_Y, CA_X)
CA_matriz_0, CA_matriz_1 = condicao_inicial(CA_Y, CA_X, pct_ocupacao_inicial)
ocupacao_stats = {}

#%%

for iteracao in range(0,qtd_iteracoes):
    
    print('Células ocupadas na iteração {}: {}'.format(iteracao+1,int(sum(sum(CA_matriz_0)))))
    
    ocupacao_stats[iteracao] = (int(sum(sum(CA_matriz_0))))/(CA_Y*CA_X)
    
    fig = plt.figure(figsize=(8,8))
    plt.imshow(CA_matriz_0, cmap="YlGn")
    plt.title("Iteração {}/{}\nMalha: {} x {}\nOcupação Inicial: {}%\nε = {}".format(iteracao+1,qtd_iteracoes,CA_X,CA_Y,pct_ocupacao_inicial,epsilon))
    plt.show()   
    
    for j in range(0, CA_Y):
        for i in range(0, CA_X):
            
            if CA_matriz_0[j][i] == 0:
            
                valor_media_atributos = media_atributos(j,i)
                
                media_ocupacao_vizinhos = ((CA_matriz_0[j-1][i-1] if ((j-1 in range(0,CA_X)) and (i-1 in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j-1][i] if ((j-1 in range(0,CA_X)) and (i in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j-1][i+1] if ((j-1 in range(0,CA_X)) and (i+1 in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j][i-1] if ((j in range(0,CA_X)) and (i-1 in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j][i+1] if ((j in range(0,CA_X)) and (i+1 in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j+1][i-1] if ((j+1 in range(0,CA_X)) and (i-1 in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j+1][i] if ((j+1 in range(0,CA_X)) and (i in range(0,CA_X))) else 0) +
                                           (CA_matriz_0[j+1][i+1] if ((j+1 in range(0,CA_X)) and (i+1 in range(0,CA_X))) else 0)) / 8
                
                # score_final = (valor_media_atributos + media_ocupacao_vizinhos + random.random()) / 3
                score_final = (valor_media_atributos * media_ocupacao_vizinhos * random.random())
                
                if score_final > epsilon:
                    CA_matriz_1[j][i] = 1
                    
    CA_matriz_0 = CA_matriz_1

fig = plt.figure(figsize=(10,5))
plt.plot(list(ocupacao_stats.keys()), 
        list(ocupacao_stats.values()), 
        linestyle='--',
        marker='x',
        color ='blue')               
x1,x2,y1,y2 = plt.axis()  
plt.axis((x1,x2,0,1))  
plt.xlabel("Iteração") 
plt.ylabel("Células Ocupadas") 
plt.title("Evolução do AC\nIterações: {}\nMalha: {} x {}\nOcupação Inicial: {}%\nε = {}".format(qtd_iteracoes,CA_X,CA_Y,pct_ocupacao_inicial,epsilon))
plt.show() 
#%%

#curva de ocupação = 100, 2, 300, 0.15 (fig 10,5)