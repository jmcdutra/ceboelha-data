import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def create_unified_database():
    """
    Cria banco de dados unificado com:
    1. Todos os alimentos da tabela nutricional portuguesa
    2. Informações FODMAP adicionadas quando existe match
    3. Alimentos FODMAP que não estão na tabela nutricional
    """
    
    print("Carregando dados...")
    
    # Carregar tabela nutricional formatada
    with open(os.path.join(OUTPUT_DIR, 'tabela_alimentar_formatada.json'), 'r', encoding='utf-8') as f:
        nutritional_data = json.load(f)
    
    # Carregar equivalências FODMAP
    with open(os.path.join(OUTPUT_DIR, 'fodmap_portuguese_equivalences.json'), 'r', encoding='utf-8') as f:
        equivalences = json.load(f)
    
    # Carregar dados FODMAP completos
    with open(os.path.join(OUTPUT_DIR, 'fodmap_database.json'), 'r', encoding='utf-8') as f:
        fodmap_data = json.load(f)
    
    print(f"✓ Tabela nutricional: {len(nutritional_data)} alimentos")
    print(f"✓ Equivalências: {equivalences['metadata']['total_matches']} matches")
    print(f"✓ Base FODMAP: {len(fodmap_data['foods'])} alimentos")
    
    # Criar mapeamento de códigos portugueses para dados FODMAP
    print("\nCriando mapeamento FODMAP...")
    fodmap_by_pt_code = {}
    fodmap_matched_names = set()
    
    for match in equivalences['matches']:
        pt_code = match['portuguese_code']
        fodmap_name = match['fodmap_name']
        
        # Buscar dados FODMAP completos
        fodmap_info = next(
            (f for f in fodmap_data['foods'] if f['name'] == fodmap_name),
            None
        )
        
        if fodmap_info and pt_code:
            fodmap_by_pt_code[pt_code] = {
                'level': fodmap_info['fodmap_level'],
                'portion_note': fodmap_info['portion_note'],
                'additional_notes': fodmap_info['additional_notes'],
                'search_information': {
                    'category': fodmap_info['category'],
                    'name_english': fodmap_info['name'],
                    'match_score': match['match_score'],
                    'match_type': match['match_type']
                }
            }
            fodmap_matched_names.add(fodmap_name)
    
    print(f"✓ {len(fodmap_by_pt_code)} códigos portugueses mapeados para FODMAP")
    
    # Criar banco de dados unificado
    unified_database = []
    
    # 1. Adicionar todos os alimentos da tabela nutricional com FODMAP quando disponível
    print("\nIntegrando dados nutricionais com FODMAP...")
    for food in nutritional_data:
        code = food.get('code')
        
        unified_entry = {
            # Identificação
            'id': code,
            'name': food.get('name'),
            'source': 'nutritional_table',
            
            # Categorias
            'category_level_1': food.get('category_level_1'),
            'category_level_2': food.get('category_level_2'),
            'category_level_3': food.get('category_level_3'),
            
            # Dados FODMAP (se disponível)
            'fodmap': None,
            
            # Dados nutricionais completos
            'nutrition': {
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
        }
        
        # Adicionar dados FODMAP se disponível
        if code in fodmap_by_pt_code:
            unified_entry['fodmap'] = fodmap_by_pt_code[code]
        
        unified_database.append(unified_entry)
    
    # 2. Adicionar alimentos FODMAP que não estão na tabela nutricional
    print("\nAdicionando alimentos FODMAP sem dados nutricionais...")
    fodmap_only_count = 0
    
    for fodmap_food in fodmap_data['foods']:
        if fodmap_food['name'] not in fodmap_matched_names:
            fodmap_only_count += 1
            
            unified_entry = {
                # Identificação
                'id': f"FODMAP_{fodmap_only_count}",
                'name': fodmap_food['name'],
                'source': 'fodmap_only',
                
                # Categorias
                'category_level_1': None,
                'category_level_2': None,
                'category_level_3': None,
                
                # Dados FODMAP completos
                'fodmap': {
                    'level': fodmap_food['fodmap_level'],
                    'portion_note': fodmap_food['portion_note'],
                    'additional_notes': fodmap_food['additional_notes'],
                    'search_information': {
                        'category': fodmap_food['category'],
                        'name_english': fodmap_food['name'],
                        'match_score': None,
                        'match_type': 'fodmap_only'
                    }
                },
                
                # Dados nutricionais (não disponíveis)
                'nutrition': None
            }
            
            unified_database.append(unified_entry)
    
    print(f"✓ {fodmap_only_count} alimentos FODMAP adicionados sem dados nutricionais")
    
    # Criar metadados
    total_foods = len(unified_database)
    foods_with_nutrition = len([f for f in unified_database if f['source'] == 'nutritional_table'])
    foods_with_fodmap = len([f for f in unified_database if f['fodmap'] is not None])
    foods_with_both = len([f for f in unified_database if f['source'] == 'nutritional_table' and f['fodmap'] is not None])
    foods_fodmap_only = len([f for f in unified_database if f['source'] == 'fodmap_only'])
    
    # Contar por nível FODMAP
    high_fodmap = len([f for f in unified_database if f['fodmap'] and f['fodmap']['level'] == 'high'])
    low_fodmap = len([f for f in unified_database if f['fodmap'] and f['fodmap']['level'] == 'low'])
    free_fodmap = len([f for f in unified_database if f['fodmap'] and f['fodmap']['level'] == 'free'])
    
    metadata = {
        'database_name': 'Unified Portuguese Nutritional and FODMAP Database',
        'version': '1.0',
        'creation_date': '2025-12-09',
        'total_foods': total_foods,
        'foods_with_nutritional_data': foods_with_nutrition,
        'foods_with_fodmap_data': foods_with_fodmap,
        'foods_with_complete_data': foods_with_both,
        'foods_fodmap_only': foods_fodmap_only,
        'fodmap_distribution': {
            'high': high_fodmap,
            'low': low_fodmap,
            'free': free_fodmap,
            'none': total_foods - foods_with_fodmap
        },
        'sources': {
            'nutritional_data': 'INSA - Tabela da Composição de Alimentos (Portugal)',
            'fodmap_data': 'Monash University FODMAP Database & Multiple FODMAP Sources'
        }
    }
    
    # Salvar banco de dados unificado
    output = {
        'metadata': metadata,
        'foods': unified_database
    }
    
    with open(os.path.join(OUTPUT_DIR, 'unified_food_database.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print("BANCO DE DADOS UNIFICADO CRIADO COM SUCESSO!")
    print(f"{'='*80}")
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"   Total de alimentos no banco: {total_foods}")
    print(f"   └─ Com dados nutricionais: {foods_with_nutrition}")
    print(f"   └─ Com dados FODMAP: {foods_with_fodmap}")
    print(f"   └─ Com ambos (completo): {foods_with_both}")
    print(f"   └─ Apenas FODMAP: {foods_fodmap_only}")
    print(f"\n🔴🟡🟢 DISTRIBUIÇÃO FODMAP:")
    print(f"   🔴 High FODMAP (evitar): {high_fodmap}")
    print(f"   🟡 Low FODMAP (moderado): {low_fodmap}")
    print(f"   🟢 Free FODMAP (seguro): {free_fodmap}")
    print(f"   ⚪ Sem dados FODMAP: {total_foods - foods_with_fodmap}")
    
    print(f"\n📁 ARQUIVO GERADO:")
    print(f"   unified_food_database.json")
    print(f"   Tamanho: ~{len(json.dumps(output, ensure_ascii=False)) / 1024 / 1024:.2f} MB")
    
    # Exemplos
    print(f"\n{'='*80}")
    print("EXEMPLOS DE ENTRADAS NO BANCO DE DADOS")
    print(f"{'='*80}")
    
    print("\n🟢 Exemplo 1: Alimento COM dados nutricionais E FODMAP")
    print("-" * 80)
    complete_example = next((f for f in unified_database if f['fodmap'] is not None and f['source'] == 'nutritional_table'), None)
    if complete_example:
        print(json.dumps({
            'id': complete_example['id'],
            'name': complete_example['name'],
            'source': complete_example['source'],
            'fodmap': complete_example['fodmap'],
            'nutrition': {
                'energy_kcal': complete_example['nutrition']['energy_kcal'],
                'energy_kj': complete_example['nutrition']['energy_kj'],
                'macronutrients': {
                    'carbohydrates_g': complete_example['nutrition']['macronutrients']['carbohydrates_g'],
                    'protein_g': complete_example['nutrition']['macronutrients']['protein_g'],
                    'lipids_g': complete_example['nutrition']['macronutrients']['lipids_g']
                }
            }
        }, ensure_ascii=False, indent=2))
    
    print("\n⚪ Exemplo 2: Alimento COM dados nutricionais SEM FODMAP")
    print("-" * 80)
    no_fodmap_example = next((f for f in unified_database if f['fodmap'] is None and f['source'] == 'nutritional_table'), None)
    if no_fodmap_example:
        print(json.dumps({
            'id': no_fodmap_example['id'],
            'name': no_fodmap_example['name'],
            'source': no_fodmap_example['source'],
            'fodmap': no_fodmap_example['fodmap'],
            'nutrition': 'Available (50+ fields)'
        }, ensure_ascii=False, indent=2))
    
    print("\n🔴 Exemplo 3: Alimento APENAS com dados FODMAP")
    print("-" * 80)
    fodmap_only_example = next((f for f in unified_database if f['source'] == 'fodmap_only'), None)
    if fodmap_only_example:
        print(json.dumps({
            'id': fodmap_only_example['id'],
            'name': fodmap_only_example['name'],
            'source': fodmap_only_example['source'],
            'fodmap': fodmap_only_example['fodmap'],
            'nutrition': fodmap_only_example['nutrition']
        }, ensure_ascii=False, indent=2))
    
    print(f"\n{'='*80}")
    print("✓ BANCO DE DADOS UNIFICADO COMPLETO E PRONTO PARA USO!")
    print(f"{'='*80}\n")
    
    return output


if __name__ == "__main__":
    create_unified_database()
