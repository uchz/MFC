# %%

""""
Eficiência da Balança - OK
Caixas por Posto e total de caixas FINALIZADAS - OK
Apanhas por posto - Pendente
Apanhas pendentes por posto - Pendente

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#%%
df = pd.read_excel('geral_pedidos.xlsx')


#%%
drop = [
    'Código',
    'Num. Caixa Plástica',
    'Num. Endereço',
    'Situação Sorter',
    'Num. Controle',
    'Cor LED',
    'Livre 1',
    'Livre 5',
    'Livre 2',
    'Livre 6.1',
    'Livre 6.3',
    'Livre 6'
    ]

df = df.drop(columns=drop)
# %%

check_weight = df[['Situação','Situação Conferência', 'Num. Picking','Data Início','Data Finalização','Data Conferência','Usuário Operador','Usuário Conferência']] 
eficiencia = check_weight[(check_weight['Situação'] == 'F') & (check_weight['Situação Conferência'] == 'F')]
eficiencia = eficiencia.drop_duplicates(subset='Num. Picking')
eficiencia = eficiencia.dropna(subset='Usuário Conferência')


# %%
#CHECK_WEIGHT CHECAGEM DE EFICIENCIA DA BALANÇA DE PEDIDOS COMPLETAMENTE FINALIZADOS

balança = eficiencia[eficiencia['Usuário Conferência'] == 'CHECK_WEIGHT']
reconf = eficiencia[eficiencia['Usuário Conferência'] != 'CHECK_WEIGHT']

total_bal = balança['Usuário Conferência'].count()
total_reconf =reconf['Usuário Conferência'].count()

total = total_bal + total_reconf

perc_bal = (total_bal / total) * 100
perc_reconf = (total_reconf / total) * 100

print(f"Total: {total}")
print(f"Balança: {total_bal} ({perc_bal:.2f}%)")
print(f"Reconferência: {total_reconf} ({perc_reconf:.2f}%)")

# Dados
labels = ['OK', 'NOK']
valores = [total_bal, total_reconf]
cores = ["#90bae1", '#1c252d']

# Estilo Seaborn
sns.set_style("whitegrid")

plt.figure(figsize=(5,4))
wedges, texts, autotexts = plt.pie(
    valores, 
    labels=labels, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=cores,
    wedgeprops={"edgecolor": "white", "linewidth": 2}
)

# Personalizar texto
for text in texts:
    text.set_fontsize(12)
    text.set_fontweight("bold")

for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")

plt.title("Distribuição Balança vs Reconferência", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# %%
#DESVIOS POR POSTO - QUANTAS CAIXAS DESVIARAM POR POSTO

desv_posto = df[[
                'Situação',
                 'Situação Conferência',
                 'Num. Posto',
                    'Num. Picking','Data Início',
                   'Data Finalização','Data Conferência',
                   'Usuário Operador',
                   'Usuário Conferência']]



# 1) Tirar duplicados e filtrar somente situação 'F'
desv_posto = desv_posto.drop_duplicates(subset=['Num. Posto', 'Num. Picking'])
desv_posto = desv_posto[desv_posto['Situação'] == 'F']

# 2) Contagem de desvios por posto
contagem_postos = desv_posto['Num. Posto'].value_counts().sort_values(ascending=True)

# 3) Total de caixas (considerando unique picking)
total_caixas = desv_posto.drop_duplicates(subset='Num. Picking').shape[0]

# 4) Criar DataFrame resumo
resumo = pd.DataFrame({
    'Posto': contagem_postos.index,
    'Qtd Desvios': contagem_postos.values,
    '% do Total': (contagem_postos.values / total_caixas * 100).round(2)
}).sort_values(by='Qtd Desvios', ascending=True)

# 5) Gráfico horizontal
fig, ax = plt.subplots(figsize=(6,8), facecolor="#1c252d")  # fundo da figura escuro
ax.set_facecolor("#1c252d")  # fundo da área do gráfico
plt.barh(resumo['Posto'].astype(str), resumo['Qtd Desvios'], color="#90bae1")

# Adicionar valores no final das barras (% + qtd)
for i, (qtd, perc) in enumerate(zip(resumo['Qtd Desvios'], resumo['% do Total'])):
    plt.text(qtd + 5, i, f"{qtd} ({perc}%)", va='center', color='white')

plt.title("Desvios por Posto", fontsize=14, fontweight="bold",color='white' )
plt.xlabel("Quantidade de Desvios", color='white')
plt.ylabel("Número do Posto", color='white')

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')
ax.grid(False)

for spine in ax.spines.values():
    spine.set_visible(False)


plt.tight_layout()
plt.show()

# 6) Exibir resumo final
resumo = resumo.set_index('Posto')
resumo.sort_values(by='Qtd Desvios', ascending=False)
#%%

print(f"Total de caixas: {total_caixas}")

# %%

# Apanhas por posto - Pendente

apanha_posto = df


# %%
apanha_posto['Situação'].unique()

#%%
print(apanha_posto['Num. Posto'].value_counts())

total_apanhas = apanha_posto['Num. Posto'].value_counts().sum()



print(total_apanhas)
# %%
