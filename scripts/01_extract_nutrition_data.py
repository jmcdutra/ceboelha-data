import pandas as pd
import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw-data')

# Ler o arquivo Excel
excel_file = os.path.join(RAW_DATA_DIR, 'insa_tca.xlsx')

# Ler todas as sheets disponíveis
xls = pd.ExcelFile(excel_file)
print(f"Sheets disponíveis: {xls.sheet_names}")

# Ler a sheet principal com os dados nutricionais
# A primeira linha contém os headers reais
df = pd.read_excel(excel_file, sheet_name='INSA_TCA_v7.0_2025', header=0)

# Usar a primeira linha como headers
new_columns = df.iloc[0].tolist()
df.columns = new_columns
df = df.drop(0).reset_index(drop=True)

print(f"\nDimensões da tabela: {df.shape}")
print(f"\nColunas:\n{df.columns.tolist()}")
print(f"\nPrimeiras 3 linhas:")
print(df.head(3).to_string())

# Converter para JSON
# Remover linhas com todos os valores NaN
df_clean = df.dropna(how='all')

# Limpar espaços em branco nos nomes das colunas
df_clean.columns = [str(col).strip().replace('\n', ' ') for col in df_clean.columns]

# Converter para dicionário
data = df_clean.to_dict(orient='records')

# Salvar como JSON
output_file = os.path.join(RAW_DATA_DIR, 'tabela_alimentar_portugal.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✓ Dados extraídos com sucesso!")
print(f"✓ Total de alimentos: {len(data)}")
print(f"✓ Arquivo salvo: {output_file}")
print(f"\nExemplo de um alimento:")
print(json.dumps(data[0], ensure_ascii=False, indent=2))
