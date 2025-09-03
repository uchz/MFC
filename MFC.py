# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    'Livre 6.1'
    ]

df = df.drop(columns=drop)
# %%

check_weight = df[['Situação','Situação Conferência', 'Num. Picking','Data Início','Data Finalização','Data Conferência','Usuário Operador','Usuário Conferência']] 
eficiencia = check_weight[(check_weight['Situação'] == 'F') & (check_weight['Situação Conferência'] == 'F')]
eficiencia = eficiencia.drop_duplicates(subset='Num. Picking')
eficiencia = eficiencia.dropna(subset='Usuário Conferência')


# %%
#CHECK_WEIGHT CHECAGEM DE EFICIENCIA DA BALANÇA

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

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# Dados
labels = ['OK', 'NOK']
valores = [total_bal, total_reconf]
cores = ['#4CAF50', '#FF9800']

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
df.columns
#DESVIOS POR POSTO
df.head()

desv_posto = df[[
                'Situação',
                 'Situação Conferência',
                 'Num. Posto',
                    'Num. Picking','Data Início',
                   'Data Finalização','Data Conferência',
                   'Usuário Operador',
                   'Usuário Conferência']]


#%%


desv_posto = desv_posto.drop_duplicates(subset=['Num. Posto','Num. Picking'])

desv_posto = desv_posto[desv_posto['Situação'] == 'F']


contagem_total = desv_posto['Num. Posto'].value_counts().sort_values()

# Gráfico horizontal
plt.figure(figsize=(5,8))
plt.barh(contagem.index.astype(str), contagem_total.values, color="#FF2600")

# Adicionar valores no final das barras
for i, v in enumerate(contagem_total.values):
    plt.text(v + 5, i, str(v), va='center')

plt.title("Quantidade por Posto", fontsize=14,)
plt.xlabel("Quantidade")
plt.ylabel("Número do Posto")
plt.tight_layout()
plt.show()

# Total de caixas desviadas por posto
total_desviadas = desv_posto['Num. Posto'].value_counts()

# Total de caixas (todos os registros)
total_caixas = desv_posto.shape[0]

print(f"Total de caixas desviadas por posto: {total_desviadas}")
print(f"Total de caixas: {total_caixas}")


# %%
total_caixas = desv_posto.drop_duplicates(subset='Num. Picking')

contagem_postos = desv_posto['Num. Posto'].value_counts().sort_index()

# Total de caixas
total_caixas = total_caixas.shape[0]

# Criar DataFrame resumo
resumo = pd.DataFrame({
    'Posto': contagem_postos.index,
    'Qtd Desvios': contagem_postos.values,
    '% do Total': (contagem_total.values / total_caixas * 100).round(2)
})

# Exibir
resumo.sort_values(by='Qtd Desvios', ascending=False)
print(f"Total de caixas: {total_caixas}")
# %%
