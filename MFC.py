# %%
import pandas as pd

df = pd.read_csv('geral_pedidos.csv', sep=';', on_bad_lines="skip")


# %%
# %%

drop = [
    'Código',
    'Num. Caixa Plástica',
    'Num. Endereço',
    'Situação Sorter',
    'Num. Controle',
    'Cor LED',
    'Unnamed: 32',
    'Livre 1',
    'Livre 5',
    'Livre 2',
    'Livre 6.1'
    ]

df = df.drop(columns=drop)
# %%
df.head()
# %%
df.info()
# %%
check_weight = df[['Situação','Situação Conferência', 'Num. Picking','Data Início','Data Finalização','Data Conferência','Usuário Operador','Usuário Conferência']] 
# %%
eficiencia = check_weight[(check_weight['Situação'] == 'F') & (check_weight['Situação Conferência'] == 'F')]
eficiencia = eficiencia.drop_duplicates(subset='Num. Picking')
eficiencia = eficiencia.dropna(subset='Usuário Conferência')


# %%
#CHECK_WEIGHT

balança = eficiencia[eficiencia['Usuário Conferência'] == 'CHECK_WEIGHT']
reconf = eficiencia[eficiencia['Usuário Conferência'] != 'CHECK_WEIGHT']

# %%
total_bal = balança['Usuário Conferência'].count()
total_reconf =reconf['Usuário Conferência'].count()
# %%
total = total_bal + total_reconf

perc_bal = (total_bal / total) * 100
perc_reconf = (total_reconf / total) * 100

print(f"Total: {total}")
print(f"Balança: {total_bal} ({perc_bal:.2f}%)")
print(f"Reconferência: {total_reconf} ({perc_reconf:.2f}%)")

# %%
# import matplotlib.pyplot as plt

# # Labels e valores
# labels = ['Balança', 'Reconferência']
# valores = [total_bal, total_reconf]

# plt.figure(figsize=(6,6))
# plt.pie(valores, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#FF9800'], startangle=90)
# plt.title('Distribuição Balança vs Reconferência')
# plt.show()

# %%
