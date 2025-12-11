import json
import re
import os
from difflib import SequenceMatcher

# Diretório base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw-data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Dicionário de traduções conhecidas (inglês -> português)
TRANSLATION_DICT = {
    # Vegetables - Expanded
    'garlic': 'alho',
    'onion': 'cebola',
    'onions': 'cebola',
    'shallot': 'chalota',
    'shallots': 'chalota',
    'scallion': 'cebolinha',
    'spring onion': 'cebolinha',
    'leek': 'alho-francês',
    'artichoke': 'alcachofra',
    'asparagus': 'espargo',
    'beetroot': 'beterraba',
    'beet': 'beterraba',
    'carrot': 'cenoura',
    'carrots': 'cenoura',
    'cauliflower': 'couve-flor',
    'celery': 'aipo',
    'celeriac': 'aipo',
    'mushroom': 'cogumelo',
    'mushrooms': 'cogumelo',
    'pea': 'ervilha',
    'peas': 'ervilha',
    'cabbage': 'couve',
    'broccoli': 'brócolis',
    'broccolini': 'brócolis',
    'spinach': 'espinafre',
    'lettuce': 'alface',
    'iceberg': 'alface',
    'rocket': 'rúcula',
    'arugula': 'rúcula',
    'radicchio': 'alface roxa',
    'tomato': 'tomate',
    'tomatoes': 'tomate',
    'potato': 'batata',
    'potatoes': 'batata',
    'sweet potato': 'batata-doce',
    'yam': 'inhame',
    'pumpkin': 'abóbora',
    'squash': 'abóbora',
    'butternut': 'abóbora',
    'cucumber': 'pepino',
    'eggplant': 'beringela',
    'aubergine': 'beringela',
    'pepper': 'pimento',
    'bell pepper': 'pimento',
    'capsicum': 'pimento',
    'chili': 'piri-piri',
    'chilli': 'piri-piri',
    'ginger': 'gengibre',
    'corn': 'milho',
    'maize': 'milho',
    'radish': 'rabanete',
    'turnip': 'nabo',
    'swede': 'rutabaga',
    'zucchini': 'courgette',
    'courgette': 'curgete',
    'bean': 'feijão',
    'beans': 'feijão',
    'broad bean': 'fava',
    'fava bean': 'fava',
    'black bean': 'feijão preto',
    'kidney bean': 'feijão',
    'lima bean': 'feijão',
    'butter bean': 'feijão manteiga',
    'haricot': 'feijão',
    'lentil': 'lentilha',
    'lentils': 'lentilha',
    'chickpea': 'grão-de-bico',
    'chickpeas': 'grão',
    'chick pea': 'grão',
    'soy': 'soja',
    'soya': 'soja',
    'soybean': 'soja',
    'tofu': 'tofu',
    'tempeh': 'tempeh',
    'kale': 'couve',
    'collard': 'couve',
    'chard': 'acelga',
    'silverbeet': 'acelga',
    'swiss chard': 'acelga',
    'rhubarb': 'ruibarbo',
    'bamboo': 'bambu',
    'okra': 'quiabo',
    'parsnip': 'pastinaca',
    'seaweed': 'alga',
    'nori': 'nori',
    'kelp': 'alga',
    'olive': 'azeitona',
    'olives': 'azeitona',
    'pickle': 'picles',
    'pickled': 'picles',
    'gherkin': 'pepino',
    'brussels sprout': 'couve-de-bruxelas',
    'fennel': 'funcho',
    'watercress': 'agrião',
    'endive': 'endívia',
    'chicory': 'chicória',
    'beansprout': 'rebentos',
    'sprout': 'rebentos',
    'chive': 'cebolinho',
    'chives': 'cebolinho',
    'parsley': 'salsa',
    'cilantro': 'coentros',
    'coriander': 'coentros',
    'basil': 'manjericão',
    'mint': 'hortelã',
    'oregano': 'orégãos',
    'rosemary': 'alecrim',
    'thyme': 'tomilho',
    'sage': 'salva',
    'tarragon': 'estragão',
    'dill': 'endro',
    
    # Fruits - Expanded
    'apple': 'maçã',
    'apples': 'maçã',
    'apricot': 'alperce',
    'apricots': 'alperce',
    'avocado': 'abacate',
    'banana': 'banana',
    'bananas': 'banana',
    'blackberry': 'amora',
    'blackberries': 'amora',
    'blueberry': 'mirtilo',
    'blueberries': 'mirtilo',
    'bilberry': 'mirtilo',
    'cranberry': 'arando',
    'lingonberry': 'arando',
    'boysenberry': 'amora',
    'cherry': 'cereja',
    'cherries': 'cereja',
    'grape': 'uva',
    'grapes': 'uva',
    'grapefruit': 'toranja',
    'kiwi': 'kiwi',
    'kiwifruit': 'kiwi',
    'lemon': 'limão',
    'lime': 'lima',
    'lychee': 'lichia',
    'mango': 'manga',
    'mangoes': 'manga',
    'melon': 'melão',
    'cantaloupe': 'melão',
    'honeydew': 'melão',
    'watermelon': 'melancia',
    'nectarine': 'nectarina',
    'orange': 'laranja',
    'oranges': 'laranja',
    'papaya': 'papaia',
    'pawpaw': 'papaia',
    'peach': 'pêssego',
    'peaches': 'pêssego',
    'pear': 'pera',
    'pears': 'pera',
    'pineapple': 'ananás',
    'plum': 'ameixa',
    'plums': 'ameixa',
    'pomegranate': 'romã',
    'raspberry': 'framboesa',
    'raspberries': 'framboesa',
    'strawberry': 'morango',
    'strawberries': 'morango',
    'mandarin': 'tangerina',
    'tangerine': 'tangerina',
    'clementine': 'clementina',
    'tangelo': 'tangerina',
    'passion fruit': 'maracujá',
    'guava': 'goiaba',
    'fig': 'figo',
    'figs': 'figo',
    'date': 'tâmara',
    'dates': 'tâmara',
    'prune': 'ameixa seca',
    'raisin': 'passa',
    'raisins': 'passa',
    'sultana': 'uva passa',
    'currant': 'groselha',
    'persimmon': 'dióspiro',
    'tamarillo': 'tomate',
    'feijoa': 'feijoa',
    'carambola': 'carambola',
    'dragon fruit': 'pitaia',
    'breadfruit': 'fruta-pão',
    'jackfruit': 'jaca',
    'tamarind': 'tamarindo',
    'anona': 'anona',
    'custard apple': 'anona',
    
    # Meats - Expanded
    'beef': 'vaca',
    'veal': 'vitela',
    'steak': 'bife',
    'mince': 'picada',
    'minced': 'picada',
    'ground beef': 'carne picada',
    'chicken': 'frango',
    'pork': 'porco',
    'lamb': 'borrego',
    'mutton': 'carneiro',
    'goat': 'cabrito',
    'kid': 'cabrito',
    'turkey': 'peru',
    'duck': 'pato',
    'goose': 'ganso',
    'quail': 'codorniz',
    'rabbit': 'coelho',
    'hare': 'lebre',
    'venison': 'veado',
    'wild boar': 'javali',
    'sausage': 'salsicha',
    'chorizo': 'chouriço',
    'ham': 'fiambre',
    'bacon': 'bacon',
    'prosciutto': 'presunto',
    'salami': 'salame',
    'pastrami': 'pastrami',
    'liver': 'fígado',
    'kidney': 'rim',
    'heart': 'coração',
    'tongue': 'língua',
    'tripe': 'tripas',
    'offal': 'miúdos',
    'foie gras': 'foie gras',
    
    # Fish & Seafood - Expanded
    'fish': 'peixe',
    'tuna': 'atum',
    'salmon': 'salmão',
    'cod': 'bacalhau',
    'hake': 'pescada',
    'plaice': 'solha',
    'sole': 'linguado',
    'flounder': 'solha',
    'sardine': 'sardinha',
    'sardines': 'sardinha',
    'anchovy': 'anchova',
    'anchovies': 'anchova',
    'herring': 'arenque',
    'mackerel': 'cavala',
    'trout': 'truta',
    'sea bass': 'robalo',
    'sea bream': 'dourada',
    'bream': 'dourada',
    'swordfish': 'espadarte',
    'monkfish': 'tamboril',
    'grouper': 'garoupa',
    'red snapper': 'pargo',
    'snapper': 'pargo',
    'mullet': 'tainha',
    'ray': 'raia',
    'skate': 'raia',
    'eel': 'enguia',
    'conger': 'safio',
    'dogfish': 'cação',
    'shark': 'tubarão',
    'octopus': 'polvo',
    'squid': 'lula',
    'cuttlefish': 'choco',
    'shrimp': 'camarão',
    'prawn': 'camarão',
    'prawns': 'camarão',
    'crab': 'caranguejo',
    'lobster': 'lagosta',
    'crayfish': 'lagostim',
    'langoustine': 'lagostim',
    'clam': 'amêijoa',
    'clams': 'amêijoa',
    'cockle': 'berbigão',
    'cockles': 'berbigão',
    'mussel': 'mexilhão',
    'mussels': 'mexilhão',
    'oyster': 'ostra',
    'oysters': 'ostra',
    'scallop': 'vieira',
    'scallops': 'vieira',
    'whelk': 'búzio',
    'periwinkle': 'caracol',
    'snail': 'caracol',
    'sea urchin': 'ouriço',
    'caviar': 'caviar',
    'roe': 'ovas',
    
    # Dairy - Expanded
    'milk': 'leite',
    'whole milk': 'leite gordo',
    'skimmed milk': 'leite magro',
    'semi-skimmed': 'leite meio-gordo',
    'buttermilk': 'leitelho',
    'lactose free': 'sem lactose',
    'almond milk': 'bebida de amêndoa',
    'soy milk': 'bebida de soja',
    'oat milk': 'bebida de aveia',
    'rice milk': 'bebida de arroz',
    'coconut milk': 'leite de coco',
    'cheese': 'queijo',
    'yogurt': 'iogurte',
    'yoghurt': 'iogurte',
    'greek yogurt': 'iogurte grego',
    'butter': 'manteiga',
    'ghee': 'ghee',
    'margarine': 'margarina',
    'cream': 'nata',
    'whipped cream': 'chantilly',
    'sour cream': 'nata azeda',
    'creme fraiche': 'nata',
    'ice cream': 'gelado',
    'gelato': 'gelado',
    'sorbet': 'sorvete',
    'ricotta': 'ricota',
    'mozzarella': 'mozzarella',
    'cheddar': 'cheddar',
    'parmesan': 'parmesão',
    'feta': 'feta',
    'brie': 'brie',
    'camembert': 'camembert',
    'cottage cheese': 'queijo fresco',
    'cream cheese': 'queijo creme',
    'goat cheese': 'queijo cabra',
    'sheep cheese': 'queijo ovelha',
    'swiss cheese': 'queijo suíço',
    'gouda': 'gouda',
    'edam': 'edam',
    'emmental': 'emmental',
    'gruyere': 'gruyère',
    'blue cheese': 'queijo azul',
    'roquefort': 'roquefort',
    'gorgonzola': 'gorgonzola',
    'halloumi': 'halloumi',
    'paneer': 'paneer',
    'quark': 'quark',
    'mascarpone': 'mascarpone',
    'kefir': 'kefir',
    'custard': 'pudim',
    'pudding': 'pudim',
    
    # Grains & Cereals - Expanded
    'wheat': 'trigo',
    'whole wheat': 'trigo integral',
    'wholegrain': 'integral',
    'wholewheat': 'integral',
    'bread': 'pão',
    'white bread': 'pão branco',
    'brown bread': 'pão escuro',
    'sourdough': 'pão de massa azeda',
    'rye bread': 'pão de centeio',
    'baguette': 'baguete',
    'ciabatta': 'ciabatta',
    'flatbread': 'pão achatado',
    'pita': 'pita',
    'naan': 'naan',
    'tortilla': 'tortilha',
    'wrap': 'wrap',
    'croissant': 'croissant',
    'roll': 'pãozinho',
    'bun': 'pão',
    'bagel': 'bagel',
    'muffin': 'muffin',
    'scone': 'scone',
    'crumpet': 'crumpet',
    'pasta': 'massa',
    'spaghetti': 'esparguete',
    'macaroni': 'macarrão',
    'penne': 'penne',
    'fusilli': 'fusilli',
    'tagliatelle': 'tagliatelle',
    'fettuccine': 'fettuccine',
    'linguine': 'linguine',
    'lasagna': 'lasanha',
    'lasagne': 'lasanha',
    'cannelloni': 'canelone',
    'ravioli': 'ravioli',
    'gnocchi': 'gnocchi',
    'rice': 'arroz',
    'white rice': 'arroz branco',
    'brown rice': 'arroz integral',
    'basmati': 'basmati',
    'jasmine': 'jasmim',
    'wild rice': 'arroz selvagem',
    'risotto': 'risoto',
    'rice noodle': 'massa de arroz',
    'oat': 'aveia',
    'oats': 'aveia',
    'oatmeal': 'aveia',
    'porridge': 'papa de aveia',
    'barley': 'cevada',
    'rye': 'centeio',
    'corn': 'milho',
    'cornmeal': 'farinha de milho',
    'cornflour': 'farinha de milho',
    'cornflake': 'flocos de milho',
    'polenta': 'polenta',
    'quinoa': 'quinoa',
    'bulgur': 'bulgur',
    'couscous': 'cuscus',
    'millet': 'milhete',
    'sorghum': 'sorgo',
    'buckwheat': 'trigo sarraceno',
    'spelt': 'espelta',
    'kamut': 'kamut',
    'amaranth': 'amaranto',
    'teff': 'teff',
    'flour': 'farinha',
    'starch': 'amido',
    'bran': 'farelo',
    'germ': 'gérmen',
    'cereal': 'cereal',
    'granola': 'granola',
    'muesli': 'muesli',
    'biscuit': 'bolacha',
    'cookie': 'bolacha',
    'cracker': 'bolacha',
    'wafer': 'wafer',
    'cake': 'bolo',
    'sponge cake': 'pão de ló',
    'pastry': 'pastelaria',
    'pie': 'tarte',
    'tart': 'tarte',
    'donut': 'donut',
    'doughnut': 'donut',
    'pancake': 'panqueca',
    'waffle': 'waffle',
    'crepe': 'crepe',
    'breadcrumb': 'pão ralado',
    'noodle': 'massa',
    'noodles': 'massa',
    'egg noodle': 'massa com ovo',
    'udon': 'udon',
    'ramen': 'ramen',
    'vermicelli': 'aletria',
    
    # Nuts & Seeds - Expanded
    'almond': 'amêndoa',
    'almonds': 'amêndoa',
    'cashew': 'caju',
    'cashews': 'caju',
    'walnut': 'noz',
    'walnuts': 'noz',
    'pistachio': 'pistácio',
    'pistachios': 'pistácio',
    'peanut': 'amendoim',
    'peanuts': 'amendoim',
    'groundnut': 'amendoim',
    'hazelnut': 'avelã',
    'hazelnuts': 'avelã',
    'filbert': 'avelã',
    'pecan': 'noz-pecã',
    'pecans': 'noz-pecã',
    'macadamia': 'macadâmia',
    'brazil nut': 'castanha do brasil',
    'chestnut': 'castanha',
    'chestnuts': 'castanha',
    'pine nut': 'pinhão',
    'pine nuts': 'pinhão',
    'coconut': 'coco',
    'seed': 'semente',
    'seeds': 'semente',
    'chia': 'chia',
    'chia seed': 'semente de chia',
    'sesame': 'sésamo',
    'sesame seed': 'semente de sésamo',
    'sunflower': 'girassol',
    'sunflower seed': 'semente de girassol',
    'pumpkin seed': 'semente de abóbora',
    'flax': 'linhaça',
    'flaxseed': 'linhaça',
    'linseed': 'linhaça',
    'hemp seed': 'semente de cânhamo',
    'poppy seed': 'semente de papoila',
    
    # Condiments & Others - Expanded
    'honey': 'mel',
    'sugar': 'açúcar',
    'brown sugar': 'açúcar amarelo',
    'white sugar': 'açúcar branco',
    'icing sugar': 'açúcar em pó',
    'syrup': 'xarope',
    'maple syrup': 'xarope de ácer',
    'golden syrup': 'xarope dourado',
    'molasses': 'melaço',
    'treacle': 'melaço',
    'agave': 'agave',
    'stevia': 'stevia',
    'salt': 'sal',
    'sea salt': 'sal marinho',
    'pepper': 'pimenta',
    'black pepper': 'pimenta preta',
    'white pepper': 'pimenta branca',
    'cayenne': 'pimenta caiena',
    'paprika': 'paprica',
    'turmeric': 'curcuma',
    'cumin': 'cominho',
    'coriander': 'coentros',
    'cardamom': 'cardamomo',
    'cinnamon': 'canela',
    'clove': 'cravinho',
    'nutmeg': 'noz-moscada',
    'saffron': 'açafrão',
    'curry': 'caril',
    'garam masala': 'garam masala',
    'vinegar': 'vinagre',
    'wine vinegar': 'vinagre de vinho',
    'balsamic': 'balsâmico',
    'cider vinegar': 'vinagre de cidra',
    'rice vinegar': 'vinagre de arroz',
    'oil': 'óleo',
    'olive oil': 'azeite',
    'vegetable oil': 'óleo vegetal',
    'sunflower oil': 'óleo de girassol',
    'coconut oil': 'óleo de coco',
    'sesame oil': 'óleo de sésamo',
    'canola oil': 'óleo de canola',
    'peanut oil': 'óleo de amendoim',
    'lard': 'banha',
    'dripping': 'gordura',
    'soy sauce': 'molho de soja',
    'tamari': 'tamari',
    'worcestershire': 'worcestershire',
    'fish sauce': 'molho de peixe',
    'oyster sauce': 'molho de ostra',
    'mustard': 'mostarda',
    'dijon': 'dijon',
    'ketchup': 'ketchup',
    'tomato sauce': 'molho de tomate',
    'tomato paste': 'concentrado de tomate',
    'mayonnaise': 'maionese',
    'mayo': 'maionese',
    'pesto': 'pesto',
    'hummus': 'húmus',
    'tahini': 'tahini',
    'miso': 'miso',
    'wasabi': 'wasabi',
    'horseradish': 'rábano',
    'chutney': 'chutney',
    'relish': 'conserva',
    'pickle': 'picles',
    'jam': 'compota',
    'jelly': 'geleia',
    'marmalade': 'compota',
    'preserve': 'conserva',
    'chocolate': 'chocolate',
    'dark chocolate': 'chocolate negro',
    'milk chocolate': 'chocolate de leite',
    'white chocolate': 'chocolate branco',
    'cocoa': 'cacau',
    'cacao': 'cacau',
    'vanilla': 'baunilha',
    'coffee': 'café',
    'espresso': 'expresso',
    'instant coffee': 'café solúvel',
    'tea': 'chá',
    'black tea': 'chá preto',
    'green tea': 'chá verde',
    'white tea': 'chá branco',
    'herbal tea': 'infusão',
    'chamomile': 'camomila',
    'peppermint': 'hortelã-pimenta',
    'wine': 'vinho',
    'red wine': 'vinho tinto',
    'white wine': 'vinho branco',
    'beer': 'cerveja',
    'ale': 'cerveja',
    'lager': 'cerveja',
    'cider': 'sidra',
    'vodka': 'vodka',
    'gin': 'gin',
    'rum': 'rum',
    'whiskey': 'whisky',
    'whisky': 'whisky',
    'brandy': 'brandy',
    'cognac': 'conhaque',
    'liqueur': 'licor',
    'juice': 'sumo',
    'orange juice': 'sumo de laranja',
    'apple juice': 'sumo de maçã',
    'lemon juice': 'sumo de limão',
    'water': 'água',
    'sparkling water': 'água gaseificada',
    'mineral water': 'água mineral',
    'soda': 'refrigerante',
    'cola': 'cola',
    'lemonade': 'limonada',
    'egg': 'ovo',
    'eggs': 'ovo',
    'yolk': 'gema',
    'white': 'clara',
    'gelatin': 'gelatina',
    'gelatine': 'gelatina',
    'agar': 'agar',
    'pectin': 'pectina',
    'yeast': 'fermento',
    'baking powder': 'fermento',
    'baking soda': 'bicarbonato',
    'bicarbonate': 'bicarbonato',
}


def normalize_name(name):
    """Normaliza nome para matching."""
    if not name:
        return ""
    name = name.lower()
    # Remover acentos
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
    
    # Remover parênteses e conteúdo
    name = re.sub(r'\([^)]*\)', '', name)
    # Remover pontuação
    name = re.sub(r'[,/:;.\-]', ' ', name)
    # Remover espaços múltiplos
    name = re.sub(r'\s+', ' ', name)
    return name.strip()


def similarity(a, b):
    """Calcula similaridade entre duas strings."""
    return SequenceMatcher(None, a, b).ratio()


def find_matches():
    """Encontra equivalências entre FODMAP e tabela portuguesa."""
    print("Carregando dados...")
    
    # Carregar dados FODMAP
    with open(os.path.join(OUTPUT_DIR, 'fodmap_database.json'), 'r', encoding='utf-8') as f:
        fodmap_data = json.load(f)
    
    # Carregar nomes portugueses
    with open(os.path.join(RAW_DATA_DIR, 'portuguese_food_names.json'), 'r', encoding='utf-8') as f:
        portuguese_data = json.load(f)
    
    print(f"✓ FODMAP: {len(fodmap_data['foods'])} alimentos")
    print(f"✓ Português: {len(portuguese_data['foods'])} alimentos")
    
    matches = []
    auto_matches = 0
    dict_matches = 0
    similarity_matches = 0
    
    print("\nProcessando matches...")
    
    for fodmap_food in fodmap_data['foods']:
        fodmap_name = fodmap_food['name']
        fodmap_normalized = fodmap_food['normalized_name']
        
        best_match = None
        best_score = 0
        match_type = None
        
        # Extrair palavra-chave do nome FODMAP
        fodmap_keywords = fodmap_normalized.split()
        
        # Tentar matching via dicionário de traduções
        for keyword in fodmap_keywords:
            if keyword in TRANSLATION_DICT:
                translation = TRANSLATION_DICT[keyword]
                translation_normalized = normalize_name(translation)
                
                # Procurar na tabela portuguesa
                for pt_food in portuguese_data['foods']:
                    pt_normalized = pt_food['normalized_main']
                    
                    # Match exato com tradução
                    if translation_normalized in pt_normalized or pt_normalized in translation_normalized:
                        score = 1.0
                        if score > best_score:
                            best_score = score
                            best_match = pt_food
                            match_type = 'dictionary'
                    
                    # Match parcial com tradução
                    elif translation_normalized and len(translation_normalized) > 3:
                        sim = similarity(translation_normalized, pt_normalized)
                        if sim > 0.85 and sim > best_score:
                            best_score = sim
                            best_match = pt_food
                            match_type = 'dictionary_partial'
        
        # Se não encontrou match por dicionário, tentar similaridade direta
        if best_score < 0.7:
            for pt_food in portuguese_data['foods']:
                pt_normalized = pt_food['normalized_main']
                
                # Tentar similaridade com nome normalizado
                sim = similarity(fodmap_normalized, pt_normalized)
                if sim > 0.8 and sim > best_score:
                    best_score = sim
                    best_match = pt_food
                    match_type = 'similarity'
        
        # Se encontrou um match válido
        if best_match and best_score > 0.7:
            match_entry = {
                'fodmap_name': fodmap_name,
                'fodmap_normalized': fodmap_normalized,
                'fodmap_level': fodmap_food['fodmap_level'],
                'fodmap_category': fodmap_food['category'],
                'fodmap_portion_note': fodmap_food['portion_note'],
                'portuguese_name': best_match['original_name'],
                'portuguese_code': best_match['code'],
                'portuguese_main_name': best_match['main_name'],
                'portuguese_category': best_match['category_level_1'],
                'match_score': round(best_score, 3),
                'match_type': match_type
            }
            matches.append(match_entry)
            
            if match_type == 'dictionary':
                dict_matches += 1
            elif match_type == 'dictionary_partial':
                dict_matches += 1
            elif match_type == 'similarity':
                similarity_matches += 1
    
    # Ordenar por score
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Salvar resultados
    output = {
        'metadata': {
            'total_fodmap_foods': len(fodmap_data['foods']),
            'total_portuguese_foods': len(portuguese_data['foods']),
            'total_matches': len(matches),
            'dictionary_matches': dict_matches,
            'similarity_matches': similarity_matches,
            'match_rate': f"{(len(matches) / len(fodmap_data['foods']) * 100):.1f}%"
        },
        'matches': matches
    }
    
    with open(os.path.join(OUTPUT_DIR, 'fodmap_portuguese_equivalences.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Matching concluído!")
    print(f"✓ Arquivo: output/fodmap_portuguese_equivalences.json")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de alimentos FODMAP: {len(fodmap_data['foods'])}")
    print(f"   Total de alimentos portugueses: {len(portuguese_data['foods'])}")
    print(f"   Total de matches encontrados: {len(matches)}")
    print(f"   Taxa de match: {(len(matches) / len(fodmap_data['foods']) * 100):.1f}%")
    print(f"   Matches por dicionário: {dict_matches}")
    print(f"   Matches por similaridade: {similarity_matches}")
    
    # Mostrar exemplos de matches por nível FODMAP
    print(f"\n🔴 HIGH FODMAP - Exemplos de matches:")
    high_matches = [m for m in matches if m['fodmap_level'] == 'high'][:5]
    for m in high_matches:
        print(f"   {m['fodmap_name']:30} → {m['portuguese_name']}")
        print(f"      Score: {m['match_score']:.3f} | Type: {m['match_type']}")
    
    print(f"\n🟡 LOW FODMAP - Exemplos de matches:")
    low_matches = [m for m in matches if m['fodmap_level'] == 'low'][:5]
    for m in low_matches:
        print(f"   {m['fodmap_name']:30} → {m['portuguese_name']}")
        print(f"      Score: {m['match_score']:.3f} | Type: {m['match_type']}")
    
    print(f"\n🟢 FREE FODMAP - Exemplos de matches:")
    free_matches = [m for m in matches if m['fodmap_level'] == 'free'][:5]
    for m in free_matches:
        print(f"   {m['fodmap_name']:30} → {m['portuguese_name']}")
        print(f"      Score: {m['match_score']:.3f} | Type: {m['match_type']}")
    
    return output


if __name__ == "__main__":
    find_matches()
