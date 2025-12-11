import json
import os

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw-data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def format_nutrition_data(raw_data):
    """
    Formata os dados nutricionais para uso em banco de dados,
    incluindo todos os campos com suas unidades corretas.
    """
    
    # Função auxiliar para adicionar unidade ao valor
    def add_unit(value, unit):
        if value is None or (isinstance(value, float) and str(value) == 'nan'):
            return None
        return f"{value}{unit}"
    
    # Função auxiliar para converter valores numéricos
    def to_number(value):
        if value is None or (isinstance(value, float) and str(value) == 'nan'):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    formatted = {
        # Informações básicas
        "code": raw_data.get("Cod"),
        "name": raw_data.get("Nome do alimento"),
        "category_level_1": raw_data.get("Nível 1"),
        "category_level_2": raw_data.get("Nível 2"),
        "category_level_3": raw_data.get("Nível 3"),
        
        # Energia
        "energy_kcal": to_number(raw_data.get("Energia [kcal]")),
        "energy_kj": to_number(raw_data.get("Energia [kJ]")),
        
        # Macronutrientes - Lípidos
        "lipids_g": add_unit(raw_data.get("Lípidos [g]"), "g"),
        "saturated_fatty_acids_g": add_unit(raw_data.get("Ácidos gordos saturados [g]"), "g"),
        "monounsaturated_fatty_acids_g": add_unit(raw_data.get("Ácidos gordos monoinsaturados  [g]"), "g"),
        "polyunsaturated_fatty_acids_g": add_unit(raw_data.get("Ácidos gordos polinsaturados  [g]"), "g"),
        "linoleic_acid_g": add_unit(raw_data.get("Ácido linoleico  [g]"), "g"),
        "trans_fatty_acids_g": add_unit(raw_data.get("Ácidos gordos trans  [g]"), "g"),
        "cholesterol_mg": add_unit(raw_data.get("Colesterol  [mg]"), "mg"),
        
        # Macronutrientes - Hidratos de Carbono
        "carbohydrates_g": add_unit(raw_data.get("Hidratos de carbono  [g]"), "g"),
        "sugars_g": add_unit(raw_data.get("Açúcares  [g]"), "g"),
        "oligosaccharides_g": add_unit(raw_data.get("Oligossacáridos  [g]"), "g"),
        "starch_g": add_unit(raw_data.get("Amido  [g]"), "g"),
        
        # Outros Macronutrientes
        "protein_g": add_unit(raw_data.get("Proteínas  [g]"), "g"),
        "fiber_g": add_unit(raw_data.get("Fibra   [g]"), "g"),
        "salt_g": add_unit(raw_data.get("Sal   [g]"), "g"),
        "alcohol_g": add_unit(raw_data.get("Álcool  [g]"), "g"),
        "water_g": add_unit(raw_data.get("Água  [g]"), "g"),
        "organic_acids_g": add_unit(raw_data.get("Ácidos orgânicos  [g]"), "g"),
        "ash_g": add_unit(raw_data.get("Cinza  [g]"), "g"),
        
        # Vitaminas Lipossolúveis
        "vitamin_a_ug": add_unit(raw_data.get("Vitamina A   [µg]"), "µg"),
        "carotene_ug": add_unit(raw_data.get("Caroteno  [µg]"), "µg"),
        "alpha_carotene_ug": add_unit(raw_data.get("alpha-caroteno [µg]"), "µg"),
        "beta_carotene_ug": add_unit(raw_data.get("beta-caroteno, total [µg]"), "µg"),
        "beta_cryptoxanthin_ug": add_unit(raw_data.get("beta-criptoxantina [µg]"), "µg"),
        "lycopene_ug": add_unit(raw_data.get("Licopeno [µg]"), "µg"),
        "lutein_ug": add_unit(raw_data.get("Luteína [µg]"), "µg"),
        "zeaxanthin_ug": add_unit(raw_data.get("Zeaxantina [µg]"), "µg"),
        "vitamin_d_ug": add_unit(raw_data.get("Vitamina D  [µg]"), "µg"),
        "alpha_tocopherol_mg": add_unit(raw_data.get("alfa-tocoferol  [mg]"), "mg"),
        
        # Vitaminas Hidrossolúveis
        "thiamin_mg": add_unit(raw_data.get("Tiamina  [mg]"), "mg"),
        "riboflavin_mg": add_unit(raw_data.get("Riboflavina  [mg]"), "mg"),
        "niacin_mg": add_unit(raw_data.get("Niacina  [mg]"), "mg"),
        "niacin_equivalents_mg": add_unit(raw_data.get("Equivalentes de niacina  [mg]"), "mg"),
        "tryptophan_60_mg": add_unit(raw_data.get("Triptofano/60  [mg]"), "mg"),
        "vitamin_b6_mg": add_unit(raw_data.get("Vitamina B6  [mg]"), "mg"),
        "vitamin_b12_ug": add_unit(raw_data.get("Vitamina B12  [µg]"), "µg"),
        "vitamin_c_mg": add_unit(raw_data.get("Vitamina C  [mg]"), "mg"),
        "folates_ug": add_unit(raw_data.get("Folatos  [µg]"), "µg"),
        
        # Minerais
        "sodium_mg": add_unit(raw_data.get("Sódio  [mg]"), "mg"),
        "potassium_mg": add_unit(raw_data.get("Potássio  [mg]"), "mg"),
        "calcium_mg": add_unit(raw_data.get("Cálcio  [mg]"), "mg"),
        "phosphorus_mg": add_unit(raw_data.get("Fósforo  [mg]"), "mg"),
        "magnesium_mg": add_unit(raw_data.get("Magnésio  [mg]"), "mg"),
        "iron_mg": add_unit(raw_data.get("Ferro  [mg]"), "mg"),
        "zinc_mg": add_unit(raw_data.get("Zinco  [mg]"), "mg"),
        "selenium_ug": add_unit(raw_data.get("Selénio  [µg]"), "µg"),
        "iodine_ug": add_unit(raw_data.get("Iodo  [µg]"), "µg"),
    }
    
    return formatted


def main():
    # Ler o arquivo JSON original
    with open(os.path.join(RAW_DATA_DIR, 'tabela_alimentar_portugal.json'), 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"Total de alimentos no arquivo: {len(raw_data)}")
    
    # Formatar todos os dados
    formatted_data = [format_nutrition_data(item) for item in raw_data]
    
    # Salvar o arquivo formatado
    output_file = os.path.join(OUTPUT_DIR, 'tabela_alimentar_formatada.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Dados formatados com sucesso!")
    print(f"✓ Arquivo salvo: {output_file}")
    print(f"\nExemplo do primeiro alimento formatado:")
    print(json.dumps(formatted_data[0], ensure_ascii=False, indent=2))
    
    # Mostrar um exemplo específico (Abacate se existir)
    abacate = next((item for item in formatted_data if "Abacate" in item.get("name", "")), None)
    if abacate:
        print(f"\nExemplo do Abacate formatado:")
        print(json.dumps(abacate, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
