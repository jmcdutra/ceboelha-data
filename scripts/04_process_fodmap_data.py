import json
import re
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw-data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def parse_fodmap_file(file_path, fodmap_level):
    """
    Parse o arquivo FODMAP e estrutura os dados.
    
    Args:
        file_path: Caminho do arquivo
        fodmap_level: 'high' ou 'low'
    
    Returns:
        Lista de dicionários com alimentos e suas informações FODMAP
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    foods = []
    current_category = None
    
    # Dividir por linhas
    lines = content.split('\n')
    
    # Categorias principais esperadas
    main_categories = [
        'Vegetables and Legumes',
        'Fruit',
        'Meats, Poultry and Meat Substitutes',
        'Fish and Seafood',
        'Cereals, Grains, Breads, Biscuits/Cookies, Pasta, Nuts and Cakes',
        'Cereals, Grains, Breads, Biscuits, Pasta, Nuts and Cakes',
        'Condiments, Dips, Sweets, Sweeteners and Spreads',
        'Prebiotic Foods',
        'Drinks and Protein Powders',
        'Dairy Foods',
        'Dairy Foods and Eggs',
        'Cooking ingredients'
    ]
    
    for line in lines:
        original_line = line
        line = line.strip()
        
        # Pular linhas vazias
        if not line:
            continue
        
        # Detectar categorias principais
        is_category = False
        for cat in main_categories:
            if cat in line:
                current_category = cat
                is_category = True
                break
        
        if is_category:
            continue
        
        # Pular linhas informativas
        skip_patterns = [
            'Want a more printer',
            'Go to the printable',
            'FODZYME helps',
            'Includes garlic',
            'Includes onion',
            'The follow',
            'be sure to check',
            'ensuring nothing else',
            'check ingredients',
            'sometimes has garlic',
            'see recipe page',
            'great onion substitute'
        ]
        
        if any(pattern in line for pattern in skip_patterns):
            continue
        
        # Detectar itens (começam com 4+ espaços na linha original)
        if current_category and original_line.startswith('    ') and line:
            # Extrair nome do alimento e observações
            food_name = line
            notes = None
            portion = None
            
            # Verificar se há observações com hífen
            if ' - ' in line:
                parts = line.split(' - ', 1)
                food_name = parts[0].strip()
                notes = parts[1].strip()
                portion = notes
            
            # Verificar se há observações com vírgula seguida de porção
            elif ',' in line:
                # Padrão: "Food name, portion info"
                match = re.match(r'(.+?),\s+(.+)', line)
                if match:
                    potential_name = match.group(1).strip()
                    potential_portion = match.group(2).strip()
                    # Verificar se a segunda parte parece uma porção
                    if re.search(r'\d|cup|tbsp|tsp|slice|pod|glass|up to|over|less than', potential_portion, re.IGNORECASE):
                        food_name = potential_name
                        portion = potential_portion
                        notes = potential_portion
            
            # Limpar o nome do alimento
            food_name = food_name.strip()
            
            # Pular se for muito curto ou for uma subcategoria
            if len(food_name) < 3 or food_name.endswith(':'):
                continue
            
            # Adicionar à lista
            foods.append({
                'name': food_name,
                'category': current_category,
                'fodmap_level': fodmap_level,
                'portion_note': portion,
                'additional_notes': notes
            })
    
    return foods


def normalize_food_name(name):
    """
    Normaliza o nome do alimento para facilitar matching.
    Remove variações, parênteses, e padroniza o texto.
    """
    # Converter para minúsculas
    name = name.lower()
    
    # Remover conteúdo entre parênteses
    name = re.sub(r'\([^)]*\)', '', name)
    
    # Remover pontuação extra
    name = re.sub(r'[/:,]', ' ', name)
    
    # Remover espaços múltiplos
    name = re.sub(r'\s+', ' ', name)
    
    # Remover espaços no início e fim
    name = name.strip()
    
    return name


def parse_free_fodmap_file(file_path):
    """
    Parse o arquivo FREE FODMAP (alimentos completamente seguros).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    foods = []
    current_category = None
    
    lines = content.split('\n')
    
    main_categories = ['Vegetables', 'Fruits', 'Meat and Fish', 'Other Foods']
    
    for line in lines:
        original_line = line
        line = line.strip()
        
        if not line:
            continue
        
        # Detectar categorias
        is_category = False
        for cat in main_categories:
            if cat == line:
                current_category = cat
                is_category = True
                break
        
        if is_category:
            continue
        
        # Detectar itens (começam com espaços na linha original)
        if current_category and original_line.startswith('    ') and line:
            food_name = line
            notes = None
            
            # Verificar se há notas entre hífens
            if ' - ' in line:
                parts = line.split(' - ', 1)
                food_name = parts[0].strip()
                notes = parts[1].strip()
            
            if len(food_name) >= 3:
                foods.append({
                    'name': food_name,
                    'category': current_category,
                    'fodmap_level': 'free',
                    'portion_note': None,
                    'additional_notes': notes
                })
    
    return foods


def create_fodmap_database():
    """
    Cria um banco de dados estruturado de alimentos FODMAP.
    """
    print("Processando arquivos FODMAP...")
    
    # Parse dos arquivos
    high_fodmap = parse_fodmap_file(os.path.join(RAW_DATA_DIR, 'high_fodmap.txt'), 'high')
    low_fodmap = parse_fodmap_file(os.path.join(RAW_DATA_DIR, 'low_fodmap.txt'), 'low')
    free_fodmap = parse_free_fodmap_file(os.path.join(RAW_DATA_DIR, 'free_fodmap.txt'))
    
    print(f"✓ High FODMAP: {len(high_fodmap)} alimentos")
    print(f"✓ Low FODMAP: {len(low_fodmap)} alimentos")
    print(f"✓ Free FODMAP: {len(free_fodmap)} alimentos")
    
    # Combinar todos os alimentos
    all_foods = high_fodmap + low_fodmap + free_fodmap
    
    # Adicionar nomes normalizados para matching
    for food in all_foods:
        food['normalized_name'] = normalize_food_name(food['name'])
    
    # Criar estrutura organizada por categoria
    by_category = {}
    for food in all_foods:
        category = food['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(food)
    
    # Criar estrutura por nível FODMAP
    by_level = {
        'high': high_fodmap,
        'low': low_fodmap,
        'free': free_fodmap
    }
    
    # Salvar estrutura completa
    output = {
        'metadata': {
            'total_foods': len(all_foods),
            'high_fodmap_count': len(high_fodmap),
            'low_fodmap_count': len(low_fodmap),
            'free_fodmap_count': len(free_fodmap),
            'categories': list(by_category.keys())
        },
        'foods': all_foods,
        'by_category': by_category,
        'by_level': by_level
    }
    
    with open(os.path.join(OUTPUT_DIR, 'fodmap_database.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Banco de dados FODMAP criado!")
    print(f"✓ Arquivo: output/fodmap_database.json")
    print(f"\nCategorias encontradas:")
    for category in by_category.keys():
        count = len(by_category[category])
        print(f"  - {category}: {count} alimentos")
    
    # Mostrar alguns exemplos
    print(f"\n--- Exemplos de alimentos HIGH FODMAP ---")
    for food in high_fodmap[:3]:
        print(f"\nNome: {food['name']}")
        print(f"Categoria: {food['category']}")
        if food['portion_note']:
            print(f"Porção: {food['portion_note']}")
    
    print(f"\n--- Exemplos de alimentos LOW FODMAP ---")
    for food in low_fodmap[:3]:
        print(f"\nNome: {food['name']}")
        print(f"Categoria: {food['category']}")
        if food['portion_note']:
            print(f"Porção: {food['portion_note']}")
    
    print(f"\n--- Exemplos de alimentos FREE FODMAP ---")
    for food in free_fodmap[:3]:
        print(f"\nNome: {food['name']}")
        print(f"Categoria: {food['category']}")
        if food['additional_notes']:
            print(f"Notas: {food['additional_notes']}")
    
    return output


if __name__ == "__main__":
    create_fodmap_database()
