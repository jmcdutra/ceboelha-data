import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def display_fodmap_summary():
    """
    Exibe um resumo detalhado do banco de dados FODMAP.
    """
    with open(os.path.join(OUTPUT_DIR, 'fodmap_database.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 80)
    print("BANCO DE DADOS FODMAP - RESUMO COMPLETO")
    print("=" * 80)
    
    metadata = data['metadata']
    print(f"\n📊 ESTATÍSTICAS GERAIS")
    print(f"   Total de alimentos: {metadata['total_foods']}")
    print(f"   High FODMAP: {metadata['high_fodmap_count']}")
    print(f"   Low FODMAP: {metadata['low_fodmap_count']}")
    
    print(f"\n📂 CATEGORIAS ({len(metadata['categories'])})")
    by_category = data['by_category']
    for category in sorted(by_category.keys()):
        items = by_category[category]
        high_count = len([i for i in items if i['fodmap_level'] == 'high'])
        low_count = len([i for i in items if i['fodmap_level'] == 'low'])
        print(f"   • {category}")
        print(f"     - High FODMAP: {high_count} | Low FODMAP: {low_count}")
    
    # Exemplos detalhados por categoria
    print(f"\n" + "=" * 80)
    print("EXEMPLOS DETALHADOS POR CATEGORIA")
    print("=" * 80)
    
    examples_per_category = 3
    
    for category in ['Vegetables and Legumes', 'Fruit', 'Dairy Foods and Eggs', 'Cereals, Grains, Breads, Biscuits, Pasta, Nuts and Cakes']:
        if category in by_category:
            print(f"\n🥗 {category.upper()}")
            print("-" * 80)
            
            items = by_category[category]
            high_items = [i for i in items if i['fodmap_level'] == 'high'][:examples_per_category]
            low_items = [i for i in items if i['fodmap_level'] == 'low'][:examples_per_category]
            
            if high_items:
                print(f"\n  ❌ HIGH FODMAP (evitar/reduzir):")
                for item in high_items:
                    print(f"     • {item['name']}")
                    if item['portion_note']:
                        print(f"       Porção: {item['portion_note']}")
            
            if low_items:
                print(f"\n  ✅ LOW FODMAP (seguro):")
                for item in low_items:
                    print(f"     • {item['name']}")
                    if item['portion_note']:
                        print(f"       Porção: {item['portion_note']}")
    
    # Estrutura de exemplo para integração
    print(f"\n" + "=" * 80)
    print("ESTRUTURA DE DADOS PARA INTEGRAÇÃO")
    print("=" * 80)
    
    example_food = data['foods'][0]
    print(f"\nExemplo de estrutura de um alimento:")
    print(json.dumps(example_food, ensure_ascii=False, indent=2))
    
    print(f"\n" + "=" * 80)
    print("CAMPOS DISPONÍVEIS PARA CADA ALIMENTO")
    print("=" * 80)
    print("""
    {
      "name": "Nome do alimento",
      "category": "Categoria principal (Vegetables, Fruit, etc)",
      "fodmap_level": "high" ou "low",
      "portion_note": "Informação de porção segura/perigosa",
      "additional_notes": "Notas adicionais",
      "normalized_name": "nome normalizado para matching"
    }
    """)
    
    print(f"\n✓ Dados estruturados e prontos para integração!")
    print(f"✓ Arquivo: fodmap_database.json")
    print(f"✓ Total de {metadata['total_foods']} alimentos catalogados")


if __name__ == "__main__":
    display_fodmap_summary()
