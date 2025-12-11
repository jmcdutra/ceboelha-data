import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def explore_unified_database():
    """Explora e visualiza o banco de dados unificado."""
    
    with open(os.path.join(OUTPUT_DIR, 'unified_food_database.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data['metadata']
    foods = data['foods']
    
    print("=" * 100)
    print("EXPLORAÇÃO DO BANCO DE DADOS UNIFICADO")
    print("=" * 100)
    
    print(f"\n📋 INFORMAÇÕES GERAIS")
    print("-" * 100)
    print(f"Nome: {metadata['database_name']}")
    print(f"Versão: {metadata['version']}")
    print(f"Data de criação: {metadata['creation_date']}")
    print(f"Total de alimentos: {metadata['total_foods']}")
    
    print(f"\n📊 COBERTURA DE DADOS")
    print("-" * 100)
    print(f"Alimentos com dados nutricionais: {metadata['foods_with_nutritional_data']} ({metadata['foods_with_nutritional_data']/metadata['total_foods']*100:.1f}%)")
    print(f"Alimentos com dados FODMAP: {metadata['foods_with_fodmap_data']} ({metadata['foods_with_fodmap_data']/metadata['total_foods']*100:.1f}%)")
    print(f"Alimentos com dados completos: {metadata['foods_with_complete_data']} ({metadata['foods_with_complete_data']/metadata['total_foods']*100:.1f}%)")
    print(f"Alimentos apenas FODMAP: {metadata['foods_fodmap_only']}")
    
    print(f"\n🔴🟡🟢 DISTRIBUIÇÃO FODMAP")
    print("-" * 100)
    fodmap_dist = metadata['fodmap_distribution']
    print(f"🔴 High FODMAP (evitar): {fodmap_dist['high']} alimentos")
    print(f"🟡 Low FODMAP (moderado): {fodmap_dist['low']} alimentos")
    print(f"🟢 Free FODMAP (100% seguro): {fodmap_dist['free']} alimentos")
    print(f"⚪ Sem informação FODMAP: {fodmap_dist['none']} alimentos")
    
    print(f"\n📚 FONTES DOS DADOS")
    print("-" * 100)
    for key, value in metadata['sources'].items():
        print(f"• {key}: {value}")
    
    # Análise detalhada
    print(f"\n" + "=" * 100)
    print("ANÁLISE DETALHADA POR CATEGORIA")
    print("=" * 100)
    
    # Top alimentos HIGH FODMAP com dados nutricionais
    print(f"\n🔴 TOP 10 HIGH FODMAP COM DADOS NUTRICIONAIS COMPLETOS")
    print("-" * 100)
    print(f"{'NOME':<50} {'CALORIAS':<12} {'PORÇÃO FODMAP':<30}")
    print("-" * 100)
    
    high_with_nutrition = [
        f for f in foods 
        if f['fodmap_level'] == 'high' and f['nutrition'] is not None
    ][:10]
    
    for food in high_with_nutrition:
        name = food['name'][:49]
        kcal = food['nutrition']['energy_kcal'] if food['nutrition']['energy_kcal'] else 'N/A'
        portion = food['fodmap_portion_note'][:29] if food['fodmap_portion_note'] else '-'
        print(f"{name:<50} {str(kcal):<12} {portion:<30}")
    
    # Top alimentos FREE FODMAP com dados nutricionais
    print(f"\n🟢 TOP 10 FREE FODMAP COM DADOS NUTRICIONAIS COMPLETOS")
    print("-" * 100)
    print(f"{'NOME':<50} {'CALORIAS':<12} {'PROTEÍNA':<15}")
    print("-" * 100)
    
    free_with_nutrition = [
        f for f in foods 
        if f['fodmap_level'] == 'free' and f['nutrition'] is not None
    ][:10]
    
    for food in free_with_nutrition:
        name = food['name'][:49]
        kcal = food['nutrition']['energy_kcal'] if food['nutrition']['energy_kcal'] else 'N/A'
        protein = food['nutrition']['macronutrients']['protein_g'] if food['nutrition']['macronutrients']['protein_g'] else 'N/A'
        print(f"{name:<50} {str(kcal):<12} {protein:<15}")
    
    # Alimentos LOW FODMAP ricos em nutrientes
    print(f"\n🟡 TOP 10 LOW FODMAP RICOS EM FIBRA")
    print("-" * 100)
    print(f"{'NOME':<50} {'FIBRA':<12} {'PORÇÃO FODMAP':<30}")
    print("-" * 100)
    
    low_with_fiber = [
        f for f in foods 
        if f['fodmap_level'] == 'low' and f['nutrition'] is not None
        and f['nutrition']['macronutrients']['fiber_g']
    ]
    
    # Ordenar por fibra (extrair valor numérico)
    def get_fiber_value(food):
        fiber = food['nutrition']['macronutrients']['fiber_g']
        if fiber:
            try:
                return float(fiber.replace('g', ''))
            except:
                return 0
        return 0
    
    low_with_fiber.sort(key=get_fiber_value, reverse=True)
    
    for food in low_with_fiber[:10]:
        name = food['name'][:49]
        fiber = food['nutrition']['macronutrients']['fiber_g'] if food['nutrition']['macronutrients']['fiber_g'] else 'N/A'
        portion = food['fodmap_portion_note'][:29] if food['fodmap_portion_note'] else '-'
        print(f"{name:<50} {fiber:<12} {portion:<30}")
    
    # Alimentos FODMAP sem dados nutricionais
    print(f"\n⚠️  ALIMENTOS FODMAP SEM DADOS NUTRICIONAIS (primeiros 20)")
    print("-" * 100)
    print(f"{'NOME (INGLÊS)':<40} {'NÍVEL FODMAP':<15} {'CATEGORIA':<35}")
    print("-" * 100)
    
    fodmap_only = [f for f in foods if f['source'] == 'fodmap_only'][:20]
    
    for food in fodmap_only:
        name = food['name'][:39]
        level_emoji = {'high': '🔴', 'low': '🟡', 'free': '🟢'}[food['fodmap_level']]
        level = f"{level_emoji} {food['fodmap_level']}"
        category = food['fodmap_category'][:34] if food['fodmap_category'] else 'N/A'
        print(f"{name:<40} {level:<15} {category:<35}")
    
    # Resumo de campos disponíveis
    print(f"\n" + "=" * 100)
    print("CAMPOS DISPONÍVEIS NO BANCO DE DADOS")
    print("=" * 100)
    
    print(f"\n🏷️  CAMPOS DE IDENTIFICAÇÃO:")
    print("   • id - Código único do alimento")
    print("   • name - Nome do alimento (português ou inglês)")
    print("   • source - Origem: 'nutritional_table' ou 'fodmap_only'")
    print("   • has_fodmap_data - Boolean indicando presença de dados FODMAP")
    
    print(f"\n📂 CAMPOS DE CATEGORIZAÇÃO:")
    print("   • category_level_1 - Categoria principal (ex: Frutos)")
    print("   • category_level_2 - Subcategoria")
    print("   • category_level_3 - Categoria específica")
    
    print(f"\n🔴🟡🟢 CAMPOS FODMAP:")
    print("   • fodmap_level - 'high', 'low', 'free' ou null")
    print("   • fodmap_category - Categoria FODMAP (ex: Vegetables and Legumes)")
    print("   • fodmap_portion_note - Notas sobre porção segura/perigosa")
    print("   • fodmap_additional_notes - Notas adicionais")
    print("   • fodmap_name_english - Nome em inglês do FODMAP")
    print("   • fodmap_match_score - Score de confiança do match (0-1)")
    print("   • fodmap_match_type - Tipo de match usado")
    
    print(f"\n🥗 CAMPOS NUTRICIONAIS (50+ campos):")
    print("   • nutrition.energy_kcal / energy_kj")
    print("   • nutrition.macronutrients.*")
    print("     - lipids_g, saturated_fatty_acids_g, carbohydrates_g,")
    print("     - sugars_g, protein_g, fiber_g, salt_g, water_g, etc")
    print("   • nutrition.vitamins.*")
    print("     - vitamin_a_ug, vitamin_c_mg, vitamin_d_ug, etc")
    print("   • nutrition.minerals.*")
    print("     - sodium_mg, potassium_mg, calcium_mg, iron_mg, etc")
    
    print(f"\n" + "=" * 100)
    print("✓ EXPLORAÇÃO COMPLETA DO BANCO DE DADOS")
    print("=" * 100)
    
    # Estatísticas de uso
    print(f"\n💡 CASOS DE USO SUGERIDOS:")
    print("-" * 100)
    print("1. Buscar alimentos seguros para dieta FODMAP:")
    print("   → Filtrar por fodmap_level='free' ou 'low'")
    print()
    print("2. Encontrar alternativas nutritivas:")
    print("   → Comparar nutrition.energy_kcal e macronutrients entre alimentos")
    print()
    print("3. Planejar refeições balanceadas:")
    print("   → Combinar alimentos com has_fodmap_data=true e nutrition disponível")
    print()
    print("4. Identificar alimentos a evitar:")
    print("   → Filtrar por fodmap_level='high'")
    print()
    print("5. Analisar conteúdo nutricional detalhado:")
    print("   → Usar campos de vitamins e minerals para análise completa")
    
    print(f"\n✓ Total: {metadata['total_foods']} alimentos prontos para uso!")
    print()


if __name__ == "__main__":
    explore_unified_database()
