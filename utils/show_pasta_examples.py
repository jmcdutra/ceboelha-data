import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Carregar banco de dados
with open(os.path.join(OUTPUT_DIR, 'unified_food_database.json'), 'r', encoding='utf-8') as f:
    db = json.load(f)

# Buscar pratos com massa/esparguete/macarrão
massas = [f for f in db['foods'] if any(word in f['name'].lower() for word in ['massa', 'esparguete', 'macarrão', 'pasta'])]

print(f"📊 ENCONTRADOS: {len(massas)} pratos com massa/pasta\n")
print("="*80)

# Mostrar primeiros 10 exemplos
for i, prato in enumerate(massas[:10], 1):
    print(f"\n{i}. {prato['name']}")
    print(f"   FODMAP: {prato['fodmap']['level'].upper()}")
    
    ingredients = prato['fodmap'].get('search_information', {}).get('ingredients', [])
    if ingredients:
        print(f"   Ingredientes detectados: {len(ingredients)}")
        for ing in ingredients:
            print(f"      • {ing['portuguese_keyword']} → {ing['name_english']} ({ing['level']})")
    else:
        print(f"   Ingredientes detectados: 0")
    
    # Mostrar dados nutricionais se disponíveis
    if 'nutrition' in prato and prato['nutrition'].get('macronutrients'):
        carbs = prato['nutrition']['macronutrients'].get('carbohydrates_g', 'N/A')
        protein = prato['nutrition']['macronutrients'].get('protein_g', 'N/A')
        print(f"   Nutrição: Carboidratos {carbs}, Proteína {protein}")

print("\n" + "="*80)
print(f"\n📈 RESUMO:")
print(f"   Total de pratos: {len(massas)}")
high_count = sum(1 for m in massas if m.get('fodmap') and m['fodmap'].get('level') == 'high')
low_count = sum(1 for m in massas if m.get('fodmap') and m['fodmap'].get('level') == 'low')
free_count = sum(1 for m in massas if m.get('fodmap') and m['fodmap'].get('level') == 'free')
multi_count = sum(1 for m in massas if m.get('fodmap') and len(m['fodmap'].get('search_information', {}).get('ingredients', [])) > 1)
print(f"   Com FODMAP HIGH: {high_count}")
print(f"   Com FODMAP LOW: {low_count}")
print(f"   Com FODMAP FREE: {free_count}")
print(f"   Com múltiplos ingredientes: {multi_count}")
