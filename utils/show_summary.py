import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw-data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

print("=" * 80)
print("RESUMO CONSOLIDADO - DADOS PRONTOS PARA INTEGRAÇÃO")
print("=" * 80)

# Carregar dados FODMAP
with open(os.path.join(OUTPUT_DIR, 'fodmap_database.json'), 'r', encoding='utf-8') as f:
    fodmap_data = json.load(f)

# Carregar nomes portugueses
with open(os.path.join(RAW_DATA_DIR, 'portuguese_food_names.json'), 'r', encoding='utf-8') as f:
    portuguese_data = json.load(f)

print("\n📊 DADOS FODMAP")
print("-" * 80)
print(f"Total de alimentos FODMAP: {fodmap_data['metadata']['total_foods']}")
print(f"  • High FODMAP (evitar): {fodmap_data['metadata']['high_fodmap_count']}")
print(f"  • Low FODMAP (moderado): {fodmap_data['metadata']['low_fodmap_count']}")
print(f"  • Free FODMAP (100% seguro): {fodmap_data['metadata']['free_fodmap_count']}")
print(f"Arquivo: fodmap_database.json")

print("\n📊 DADOS TABELA PORTUGUESA")
print("-" * 80)
print(f"Total de alimentos: {portuguese_data['metadata']['total_foods']}")
print(f"Arquivo principal: tabela_alimentar_formatada.json")
print(f"Arquivo de nomes: portuguese_food_names.json")

print("\n📁 ARQUIVOS CRIADOS")
print("-" * 80)
print("1. fodmap_database.json")
print("   └─ Base completa FODMAP com 559 alimentos")
print("   └─ Estrutura: foods, by_category, by_level")
print("")
print("2. tabela_alimentar_formatada.json")
print("   └─ Tabela nutricional portuguesa com 1372 alimentos")
print("   └─ Todos os campos com unidades (g, mg, µg, kcal, kJ)")
print("")
print("3. portuguese_food_names.json")
print("   └─ Lista de nomes extraídos para matching")
print("   └─ Inclui nomes normalizados e categorizados")
print("")
print("4. portuguese_food_names_simple.json")
print("   └─ Lista simplificada para matching rápido")

print("\n🔧 ESTRUTURA DOS DADOS")
print("-" * 80)

print("\nFODMAP (cada alimento):")
print("""
{
  "name": "Garlic",
  "category": "Vegetables and Legumes",
  "fodmap_level": "high" | "low" | "free",
  "portion_note": "avoid entirely if possible",
  "additional_notes": "...",
  "normalized_name": "garlic"
}
""")

print("\nTABELA PORTUGUESA (cada alimento):")
print("""
{
  "code": 624,
  "name": "Abacate, Hass",
  "category_level_1": "Frutos e produtos derivados de frutos",
  "energy_kcal": 176.0,
  "energy_kj": 726.0,
  "lipids_g": "17.4g",
  "sugars_g": "2.3g",
  "protein_g": "1.1g",
  "fiber_g": "3g",
  "vitamin_c_mg": "3mg",
  "calcium_mg": "4mg",
  ...50+ campos nutricionais
}
""")

print("\n🎯 PRÓXIMO PASSO")
print("-" * 80)
print("Criar script de MATCHING para combinar:")
print("  1. Nomes portugueses → Nomes FODMAP inglês")
print("  2. Adicionar campo 'fodmap_level' na tabela nutricional")
print("  3. Gerar arquivo final: tabela_completa_com_fodmap.json")

print("\n" + "=" * 80)
print("✓ TODOS OS DADOS ESTRUTURADOS E PRONTOS!")
print("=" * 80)

# Mostrar alguns exemplos de possíveis matches
print("\n💡 EXEMPLOS DE POSSÍVEIS MATCHES:")
print("-" * 80)

examples = [
    ("Abacate", "Avocado"),
    ("Alho", "Garlic"),
    ("Cebola", "Onions"),
    ("Cenoura", "Carrots"),
    ("Espinafre", "Spinach"),
    ("Banana", "Bananas"),
    ("Maçã", "Apples"),
    ("Leite", "Milk"),
    ("Queijo", "Cheese"),
    ("Arroz", "Rice")
]

for pt, en in examples:
    print(f"  {pt:20} → {en}")

print("\n" + "=" * 80)
