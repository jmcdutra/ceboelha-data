import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def display_equivalences():
    """Exibe as equivalências de forma organizada."""
    
    with open(os.path.join(OUTPUT_DIR, 'fodmap_portuguese_equivalences.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 100)
    print("EQUIVALÊNCIAS FODMAP ↔ TABELA PORTUGUESA")
    print("=" * 100)
    
    metadata = data['metadata']
    print(f"\n📊 RESUMO DO MATCHING")
    print(f"   Alimentos FODMAP processados: {metadata['total_fodmap_foods']}")
    print(f"   Alimentos portugueses na base: {metadata['total_portuguese_foods']}")
    print(f"   ✓ Matches encontrados: {metadata['total_matches']}")
    print(f"   Taxa de sucesso: {metadata['match_rate']}")
    print(f"   Matches por dicionário: {metadata['dictionary_matches']}")
    print(f"   Matches por similaridade: {metadata['similarity_matches']}")
    
    matches = data['matches']
    
    # Agrupar por nível FODMAP
    by_level = {
        'high': [m for m in matches if m['fodmap_level'] == 'high'],
        'low': [m for m in matches if m['fodmap_level'] == 'low'],
        'free': [m for m in matches if m['fodmap_level'] == 'free']
    }
    
    print(f"\n📈 MATCHES POR NÍVEL FODMAP:")
    print(f"   🔴 High FODMAP (evitar): {len(by_level['high'])} matches")
    print(f"   🟡 Low FODMAP (moderado): {len(by_level['low'])} matches")
    print(f"   🟢 Free FODMAP (seguro): {len(by_level['free'])} matches")
    
    # Mostrar top matches de cada categoria
    print("\n" + "=" * 100)
    print("🔴 HIGH FODMAP - ALIMENTOS A EVITAR")
    print("=" * 100)
    print(f"{'INGLÊS (FODMAP)':<35} {'PORTUGUÊS':<40} {'SCORE':<10}")
    print("-" * 100)
    
    for match in by_level['high'][:20]:
        fodmap = match['fodmap_name'][:34]
        portuguese = match['portuguese_name'][:39]
        score = f"{match['match_score']:.3f}"
        note = f" ({match['fodmap_portion_note'][:30]}...)" if match['fodmap_portion_note'] else ""
        print(f"{fodmap:<35} {portuguese:<40} {score:<10}")
        if note:
            print(f"  └─ {note}")
    
    print("\n" + "=" * 100)
    print("🟡 LOW FODMAP - MODERAÇÃO RECOMENDADA")
    print("=" * 100)
    print(f"{'INGLÊS (FODMAP)':<35} {'PORTUGUÊS':<40} {'SCORE':<10}")
    print("-" * 100)
    
    for match in by_level['low'][:20]:
        fodmap = match['fodmap_name'][:34]
        portuguese = match['portuguese_name'][:39]
        score = f"{match['match_score']:.3f}"
        note = f" ({match['fodmap_portion_note'][:30]}...)" if match['fodmap_portion_note'] else ""
        print(f"{fodmap:<35} {portuguese:<40} {score:<10}")
        if note:
            print(f"  └─ {note}")
    
    print("\n" + "=" * 100)
    print("🟢 FREE FODMAP - ALIMENTOS SEGUROS")
    print("=" * 100)
    print(f"{'INGLÊS (FODMAP)':<35} {'PORTUGUÊS':<40} {'SCORE':<10}")
    print("-" * 100)
    
    for match in by_level['free'][:20]:
        fodmap = match['fodmap_name'][:34]
        portuguese = match['portuguese_name'][:39]
        score = f"{match['match_score']:.3f}"
        print(f"{fodmap:<35} {portuguese:<40} {score:<10}")
    
    # Exemplos de traduções específicas
    print("\n" + "=" * 100)
    print("🔤 TRADUÇÕES CHAVE (INGLÊS → PORTUGUÊS)")
    print("=" * 100)
    
    key_translations = {
        'garlic': 'alho',
        'onion': 'cebola',
        'apple': 'maçã',
        'banana': 'banana',
        'milk': 'leite',
        'cheese': 'queijo',
        'bread': 'pão',
        'rice': 'arroz',
        'wheat': 'trigo',
        'avocado': 'abacate',
        'carrot': 'cenoura',
        'tomato': 'tomate',
        'potato': 'batata',
        'chicken': 'frango',
        'beef': 'vaca',
        'fish': 'peixe'
    }
    
    found_translations = {}
    for match in matches:
        for en, pt in key_translations.items():
            if en in match['fodmap_normalized']:
                if en not in found_translations:
                    found_translations[en] = []
                found_translations[en].append({
                    'fodmap': match['fodmap_name'],
                    'portuguese': match['portuguese_name'],
                    'level': match['fodmap_level']
                })
    
    for en_word in sorted(found_translations.keys()):
        print(f"\n'{en_word.upper()}' encontrado em:")
        for item in found_translations[en_word][:3]:
            level_emoji = {'high': '🔴', 'low': '🟡', 'free': '🟢'}[item['level']]
            print(f"   {level_emoji} {item['fodmap']:<30} → {item['portuguese']}")
    
    print("\n" + "=" * 100)
    print(f"✓ ARQUIVO GERADO: fodmap_portuguese_equivalences.json")
    print(f"✓ Total de {metadata['total_matches']} equivalências prontas para uso!")
    print("=" * 100)


if __name__ == "__main__":
    display_equivalences()
