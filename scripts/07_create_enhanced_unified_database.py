import json
import re
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def normalize_name(name):
    """Normaliza nome para matching."""
    if not name:
        return ""
    name = name.lower()
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'è': 'e',
        'í': 'i', 'ì': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o', 'ò': 'o',
        'ú': 'u', 'ü': 'u', 'ù': 'u',
        'ç': 'c'
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'[,/:;.\-]', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()


def create_enhanced_unified_database():
    """
    Cria banco de dados unificado com detecção de múltiplos ingredientes FODMAP.
    """
    
    print("Carregando dados...")
    
    with open(os.path.join(OUTPUT_DIR, 'tabela_alimentar_formatada.json'), 'r', encoding='utf-8') as f:
        nutritional_data = json.load(f)
    
    with open(os.path.join(OUTPUT_DIR, 'fodmap_database.json'), 'r', encoding='utf-8') as f:
        fodmap_data = json.load(f)
    
    print(f"✓ Tabela nutricional: {len(nutritional_data)} alimentos")
    print(f"✓ Base FODMAP: {len(fodmap_data['foods'])} alimentos")
    
    # Criar índice FODMAP por palavras-chave
    print("\nCriando índice FODMAP por ingredientes...")
    fodmap_index = {}
    
    for fodmap_food in fodmap_data['foods']:
        name_normalized = fodmap_food['normalized_name']
        words = name_normalized.split()
        
        # Adicionar o alimento completo
        fodmap_index[name_normalized] = fodmap_food
        
        # Adicionar palavras individuais (mínimo 3 caracteres)
        for word in words:
            if len(word) >= 3 and word not in ['the', 'and', 'with', 'for']:
                if word not in fodmap_index:
                    fodmap_index[word] = []
                if isinstance(fodmap_index[word], list):
                    fodmap_index[word].append(fodmap_food)
                else:
                    fodmap_index[word] = [fodmap_index[word], fodmap_food]
    
    print(f"✓ Índice FODMAP criado com {len(fodmap_index)} entradas")
    
    # Palavras-chave portuguesas -> FODMAP
    ingredient_keywords = {
        # Massas e cereais
        'massa': ['pasta', 'wheat', 'spaghetti', 'noodle'],
        'esparguete': ['spaghetti', 'pasta', 'wheat'],
        'macarrao': ['pasta', 'wheat', 'noodle'],
        'massa': ['pasta', 'wheat'],
        'pao': ['bread', 'wheat'],
        'trigo': ['wheat'],
        'arroz': ['rice'],
        'aveia': ['oat'],
        'cevada': ['barley'],
        'centeio': ['rye'],
        
        # Vegetais
        'alho': ['garlic'],
        'cebola': ['onion'],
        'cebolinha': ['scallion', 'spring onion'],
        'cenoura': ['carrot'],
        'tomate': ['tomato'],
        'cogumelo': ['mushroom'],
        'espargo': ['asparagus'],
        'brocolis': ['broccoli'],
        'couve': ['cabbage', 'kale'],
        'couve-flor': ['cauliflower'],
        'espinafre': ['spinach'],
        'alface': ['lettuce'],
        'pepino': ['cucumber'],
        'abobora': ['pumpkin', 'squash'],
        'beringela': ['eggplant', 'aubergine'],
        'feijao': ['bean'],
        'ervilha': ['pea'],
        'grao': ['chickpea'],
        'lentilha': ['lentil'],
        'batata': ['potato'],
        'aipo': ['celery'],
        'alcachofra': ['artichoke'],
        
        # Frutas
        'maca': ['apple'],
        'pera': ['pear'],
        'banana': ['banana'],
        'morango': ['strawberry'],
        'uva': ['grape'],
        'laranja': ['orange'],
        'limao': ['lemon'],
        'abacate': ['avocado'],
        'manga': ['mango'],
        'pessego': ['peach'],
        'ameixa': ['plum'],
        'cereja': ['cherry'],
        'melancia': ['watermelon'],
        'melao': ['melon'],
        
        # Carnes e peixes
        'vaca': ['beef'],
        'frango': ['chicken'],
        'porco': ['pork'],
        'borrego': ['lamb'],
        'peixe': ['fish'],
        'bacalhau': ['cod'],
        'atum': ['tuna'],
        'salmao': ['salmon'],
        'camarao': ['shrimp', 'prawn'],
        
        # Laticínios
        'leite': ['milk'],
        'queijo': ['cheese'],
        'iogurte': ['yogurt', 'yoghurt'],
        'manteiga': ['butter'],
        'nata': ['cream'],
        
        # Outros
        'azeite': ['olive oil', 'oil'],
        'oleo': ['oil'],
        'mel': ['honey'],
        'acucar': ['sugar'],
    }
    
    # Processar cada alimento
    unified_database = []
    foods_with_multiple_ingredients = 0
    
    print("\nAnalisando ingredientes em cada alimento...")
    
    for food in nutritional_data:
        name = food.get('name', '')
        name_normalized = normalize_name(name)
        
        # Detectar ingredientes FODMAP
        detected_ingredients = []
        
        # 1. Buscar por palavras-chave portuguesas
        for pt_keyword, en_keywords in ingredient_keywords.items():
            if pt_keyword in name_normalized:
                # Buscar cada equivalente em inglês no índice FODMAP
                for en_keyword in en_keywords:
                    en_normalized = normalize_name(en_keyword)
                    
                    # Buscar matches no índice
                    if en_normalized in fodmap_index:
                        fodmap_match = fodmap_index[en_normalized]
                        if isinstance(fodmap_match, list):
                            for match in fodmap_match:
                                if match not in detected_ingredients:
                                    detected_ingredients.append({
                                        'portuguese_keyword': pt_keyword,
                                        'fodmap_data': match
                                    })
                                    break
                        else:
                            if fodmap_match not in [d['fodmap_data'] for d in detected_ingredients]:
                                detected_ingredients.append({
                                    'portuguese_keyword': pt_keyword,
                                    'fodmap_data': fodmap_match
                                })
                    
                    # Buscar também por palavras parciais
                    for key in fodmap_index.keys():
                        if en_normalized in key or key in en_normalized:
                            fodmap_match = fodmap_index[key]
                            if not isinstance(fodmap_match, list):
                                if fodmap_match not in [d['fodmap_data'] for d in detected_ingredients]:
                                    detected_ingredients.append({
                                        'portuguese_keyword': pt_keyword,
                                        'fodmap_data': fodmap_match
                                    })
                                    break
        
        # Remover duplicatas baseado no nome FODMAP
        unique_ingredients = []
        seen_names = set()
        for ingredient in detected_ingredients:
            fodmap_name = ingredient['fodmap_data']['name']
            if fodmap_name not in seen_names:
                seen_names.add(fodmap_name)
                unique_ingredients.append(ingredient)
        
        detected_ingredients = unique_ingredients
        
        if len(detected_ingredients) > 1:
            foods_with_multiple_ingredients += 1
        
        # Criar entrada unificada
        unified_entry = {
            'id': food.get('code'),
            'name': name,
            'source': 'nutritional_table',
            'category_level_1': food.get('category_level_1'),
            'category_level_2': food.get('category_level_2'),
            'category_level_3': food.get('category_level_3'),
        }
        
        # Adicionar dados FODMAP
        if detected_ingredients:
            if len(detected_ingredients) == 1:
                # Apenas um ingrediente
                ingredient = detected_ingredients[0]
                fodmap = ingredient['fodmap_data']
                unified_entry['fodmap'] = {
                    'level': fodmap['fodmap_level'],
                    'portion_note': fodmap['portion_note'],
                    'additional_notes': fodmap['additional_notes'],
                    'search_information': {
                        'category': fodmap['category'],
                        'name_english': fodmap['name'],
                        'detected_keyword': ingredient['portuguese_keyword'],
                        'match_type': 'single_ingredient'
                    }
                }
            else:
                # Múltiplos ingredientes
                ingredients_list = []
                highest_level = 'free'
                
                for ingredient in detected_ingredients:
                    fodmap = ingredient['fodmap_data']
                    ingredients_list.append({
                        'portuguese_keyword': ingredient['portuguese_keyword'],
                        'name_english': fodmap['name'],
                        'level': fodmap['fodmap_level'],
                        'portion_note': fodmap['portion_note'],
                        'category': fodmap['category']
                    })
                    
                    # Determinar nível mais alto
                    if fodmap['fodmap_level'] == 'high':
                        highest_level = 'high'
                    elif fodmap['fodmap_level'] == 'low' and highest_level != 'high':
                        highest_level = 'low'
                
                unified_entry['fodmap'] = {
                    'level': highest_level,
                    'portion_note': f"Contains {len(ingredients_list)} FODMAP ingredients",
                    'additional_notes': "Multiple ingredients detected - check individual ingredients below",
                    'search_information': {
                        'match_type': 'multiple_ingredients',
                        'total_ingredients': len(ingredients_list),
                        'ingredients': ingredients_list
                    }
                }
        else:
            unified_entry['fodmap'] = None
        
        # Adicionar dados nutricionais
        unified_entry['nutrition'] = {
            'energy_kcal': food.get('energy_kcal'),
            'energy_kj': food.get('energy_kj'),
            'macronutrients': {
                'lipids_g': food.get('lipids_g'),
                'saturated_fatty_acids_g': food.get('saturated_fatty_acids_g'),
                'monounsaturated_fatty_acids_g': food.get('monounsaturated_fatty_acids_g'),
                'polyunsaturated_fatty_acids_g': food.get('polyunsaturated_fatty_acids_g'),
                'linoleic_acid_g': food.get('linoleic_acid_g'),
                'trans_fatty_acids_g': food.get('trans_fatty_acids_g'),
                'cholesterol_mg': food.get('cholesterol_mg'),
                'carbohydrates_g': food.get('carbohydrates_g'),
                'sugars_g': food.get('sugars_g'),
                'oligosaccharides_g': food.get('oligosaccharides_g'),
                'starch_g': food.get('starch_g'),
                'protein_g': food.get('protein_g'),
                'fiber_g': food.get('fiber_g'),
                'salt_g': food.get('salt_g'),
                'alcohol_g': food.get('alcohol_g'),
                'water_g': food.get('water_g'),
                'organic_acids_g': food.get('organic_acids_g'),
                'ash_g': food.get('ash_g'),
            },
            'vitamins': {
                'vitamin_a_ug': food.get('vitamin_a_ug'),
                'carotene_ug': food.get('carotene_ug'),
                'alpha_carotene_ug': food.get('alpha_carotene_ug'),
                'beta_carotene_ug': food.get('beta_carotene_ug'),
                'beta_cryptoxanthin_ug': food.get('beta_cryptoxanthin_ug'),
                'lycopene_ug': food.get('lycopene_ug'),
                'lutein_ug': food.get('lutein_ug'),
                'zeaxanthin_ug': food.get('zeaxanthin_ug'),
                'vitamin_d_ug': food.get('vitamin_d_ug'),
                'alpha_tocopherol_mg': food.get('alpha_tocopherol_mg'),
                'thiamin_mg': food.get('thiamin_mg'),
                'riboflavin_mg': food.get('riboflavin_mg'),
                'niacin_mg': food.get('niacin_mg'),
                'niacin_equivalents_mg': food.get('niacin_equivalents_mg'),
                'tryptophan_60_mg': food.get('tryptophan_60_mg'),
                'vitamin_b6_mg': food.get('vitamin_b6_mg'),
                'vitamin_b12_ug': food.get('vitamin_b12_ug'),
                'vitamin_c_mg': food.get('vitamin_c_mg'),
                'folates_ug': food.get('folates_ug'),
            },
            'minerals': {
                'sodium_mg': food.get('sodium_mg'),
                'potassium_mg': food.get('potassium_mg'),
                'calcium_mg': food.get('calcium_mg'),
                'phosphorus_mg': food.get('phosphorus_mg'),
                'magnesium_mg': food.get('magnesium_mg'),
                'iron_mg': food.get('iron_mg'),
                'zinc_mg': food.get('zinc_mg'),
                'selenium_ug': food.get('selenium_ug'),
                'iodine_ug': food.get('iodine_ug'),
            }
        }
        
        unified_database.append(unified_entry)
    
    # Adicionar alimentos FODMAP puros
    print("\nAdicionando alimentos FODMAP sem dados nutricionais...")
    fodmap_only_count = 0
    
    for fodmap_food in fodmap_data['foods']:
        fodmap_only_count += 1
        
        unified_entry = {
            'id': f"FODMAP_{fodmap_only_count}",
            'name': fodmap_food['name'],
            'source': 'fodmap_only',
            'category_level_1': None,
            'category_level_2': None,
            'category_level_3': None,
            'fodmap': {
                'level': fodmap_food['fodmap_level'],
                'portion_note': fodmap_food['portion_note'],
                'additional_notes': fodmap_food['additional_notes'],
                'search_information': {
                    'category': fodmap_food['category'],
                    'name_english': fodmap_food['name'],
                    'match_type': 'fodmap_only'
                }
            },
            'nutrition': None
        }
        
        unified_database.append(unified_entry)
    
    # Estatísticas
    total_foods = len(unified_database)
    foods_with_fodmap = len([f for f in unified_database if f['fodmap'] is not None])
    foods_with_nutrition = len([f for f in unified_database if f['nutrition'] is not None])
    
    metadata = {
        'database_name': 'Enhanced Unified Portuguese Nutritional and FODMAP Database',
        'version': '2.0',
        'creation_date': '2025-12-09',
        'features': [
            'Multiple ingredient detection',
            'Composite dish analysis',
            'Enhanced FODMAP matching'
        ],
        'total_foods': total_foods,
        'foods_with_fodmap_data': foods_with_fodmap,
        'foods_with_nutritional_data': foods_with_nutrition,
        'foods_with_multiple_ingredients': foods_with_multiple_ingredients,
        'sources': {
            'nutritional_data': 'INSA - Tabela da Composição de Alimentos (Portugal)',
            'fodmap_data': 'Monash University FODMAP Database & Multiple FODMAP Sources'
        }
    }
    
    output = {
        'metadata': metadata,
        'foods': unified_database
    }
    
    with open(os.path.join(OUTPUT_DIR, 'unified_food_database.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print("BANCO DE DADOS APRIMORADO CRIADO!")
    print(f"{'='*80}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total: {total_foods} alimentos")
    print(f"   Com dados FODMAP: {foods_with_fodmap}")
    print(f"   Com dados nutricionais: {foods_with_nutrition}")
    print(f"   Com múltiplos ingredientes: {foods_with_multiple_ingredients}")
    
    # Exemplos
    print(f"\n{'='*80}")
    print("EXEMPLOS DE DETECÇÃO DE MÚLTIPLOS INGREDIENTES")
    print(f"{'='*80}")
    
    multi_examples = [f for f in unified_database 
                     if f['fodmap'] and 
                     f['fodmap'].get('search_information', {}).get('match_type') == 'multiple_ingredients'][:5]
    
    for example in multi_examples:
        print(f"\n📦 {example['name']}")
        print(f"   Nível FODMAP: {example['fodmap']['level'].upper()}")
        ingredients = example['fodmap']['search_information']['ingredients']
        for ing in ingredients:
            print(f"   • {ing['portuguese_keyword']} → {ing['name_english']} ({ing['level']})")
    
    print(f"\n✓ Arquivo salvo: unified_food_database.json\n")
    
    return output


if __name__ == "__main__":
    create_enhanced_unified_database()
