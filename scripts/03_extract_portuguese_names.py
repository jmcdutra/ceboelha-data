import json
import re
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw-data')

def normalize_name(name):
    """
    Normaliza o nome do alimento para facilitar matching.
    """
    if not name:
        return ""
    
    # Converter para minúsculas
    name = name.lower()
    
    # Remover acentos comuns em português
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c'
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    # Remover conteúdo entre parênteses
    name = re.sub(r'\([^)]*\)', '', name)
    
    # Remover pontuação
    name = re.sub(r'[,/:;]', ' ', name)
    
    # Remover espaços múltiplos
    name = re.sub(r'\s+', ' ', name)
    
    return name.strip()


def extract_food_names():
    """
    Extrai todos os nomes de alimentos da tabela portuguesa.
    """
    print("Carregando tabela alimentar portuguesa...")
    
    with open(os.path.join(RAW_DATA_DIR, 'tabela_alimentar_portugal.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✓ Total de alimentos: {len(data)}")
    
    # Extrair informações de cada alimento
    foods_list = []
    
    for item in data:
        food_name = item.get('Nome do alimento', '')
        if food_name:
            # Separar por vírgula se houver variações
            # Ex: "Abacate, Hass" -> ["Abacate", "Hass"]
            name_parts = [part.strip() for part in food_name.split(',')]
            main_name = name_parts[0]
            variation = name_parts[1] if len(name_parts) > 1 else None
            
            foods_list.append({
                'code': item.get('Cod'),
                'original_name': food_name,
                'main_name': main_name,
                'variation': variation,
                'normalized_name': normalize_name(food_name),
                'normalized_main': normalize_name(main_name),
                'category_level_1': item.get('Nível 1'),
                'category_level_2': item.get('Nível 2'),
                'category_level_3': item.get('Nível 3')
            })
    
    # Salvar lista de nomes
    output = {
        'metadata': {
            'total_foods': len(foods_list),
            'source': 'INSA - Tabela da Composição de Alimentos'
        },
        'foods': foods_list
    }
    
    with open(os.path.join(RAW_DATA_DIR, 'portuguese_food_names.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Nomes extraídos com sucesso!")
    print(f"✓ Arquivo: raw-data/portuguese_food_names.json")
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de alimentos: {len(foods_list)}")
    
    # Contar por categoria nível 1
    categories = {}
    for food in foods_list:
        cat = food['category_level_1']
        if cat:
            categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📂 ALIMENTOS POR CATEGORIA:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {cat}: {count} alimentos")
    
    # Exemplos
    print(f"\n📋 EXEMPLOS DE NOMES EXTRAÍDOS:")
    for i, food in enumerate(foods_list[:10]):
        print(f"\n{i+1}. {food['original_name']}")
        print(f"   Nome principal: {food['main_name']}")
        if food['variation']:
            print(f"   Variação: {food['variation']}")
        print(f"   Normalizado: {food['normalized_name']}")
        print(f"   Categoria: {food['category_level_1']}")
    
    # Criar lista simples só com nomes para matching rápido
    simple_names = {
        'original_names': [f['original_name'] for f in foods_list],
        'normalized_names': [f['normalized_name'] for f in foods_list],
        'main_names': [f['main_name'] for f in foods_list]
    }
    
    with open(os.path.join(RAW_DATA_DIR, 'portuguese_food_names_simple.json'), 'w', encoding='utf-8') as f:
        json.dump(simple_names, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Lista simples criada: raw-data/portuguese_food_names_simple.json")
    print(f"\n🎯 Pronto para matching com dados FODMAP!")
    
    return output


if __name__ == "__main__":
    extract_food_names()
