# Database - Unified Portuguese Nutritional and FODMAP Database

This directory contains the data processing pipeline for creating a unified food database that combines Portuguese nutritional data with FODMAP (Fermentable Oligosaccharides, Disaccharides, Monosaccharides, and Polyols) information. This project was developed with the assistance of AI (GitHub Copilot/Claude) to parse, translate, match, and integrate data from multiple heterogeneous sources.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Data Sources](#data-sources)
- [Pipeline Execution](#pipeline-execution)
- [Scripts Description](#scripts-description)
- [Output Files](#output-files)
- [Utility Scripts](#utility-scripts)
- [Technical Details](#technical-details)
- [Notes](#notes)

---

## Overview

The goal of this pipeline is to create a comprehensive food database that:

1. Contains nutritional information from the Portuguese Food Composition Table (INSA - Tabela da Composicao de Alimentos)
2. Integrates FODMAP level information (high/low/free) from Monash University and other FODMAP sources
3. Provides Portuguese-English food name mappings
4. Detects multiple FODMAP ingredients in composite dishes
5. Supports dietary planning for individuals with IBS or FODMAP sensitivities

The main challenge was matching foods between English FODMAP databases and Portuguese nutritional tables, which required extensive translation dictionaries and fuzzy matching algorithms.

---

## Directory Structure

```
database/
├── README.md                          # This file
├── raw-data/                          # Source data files
│   ├── insa_tca.xlsx                  # Portuguese nutritional table (Excel)
│   ├── high_fodmap.txt                # High FODMAP foods list (English)
│   ├── low_fodmap.txt                 # Low FODMAP foods list (English)
│   ├── free_fodmap.txt                # FODMAP-free foods list (English)
│   ├── foodmap_pt.txt                 # FODMAP lists translated to Portuguese
│   ├── tabela_alimentar_portugal.json # Raw extracted nutritional data
│   ├── portuguese_food_names.json     # Extracted food names with metadata
│   └── portuguese_food_names_simple.json # Simplified food names list
├── scripts/                           # Processing scripts (numbered by execution order)
│   ├── 01_extract_nutrition_data.py   # Extract data from Excel
│   ├── 02_format_for_database.py      # Format nutritional data
│   ├── 03_extract_portuguese_names.py # Extract and normalize food names
│   ├── 04_process_fodmap_data.py      # Parse FODMAP text files
│   ├── 05_create_equivalences.py      # Create PT-EN food mappings
│   ├── 06_create_unified_database.py  # Basic unified database
│   └── 07_create_enhanced_unified_database.py # Enhanced with multi-ingredient detection
├── output/                            # Generated database files
│   ├── unified_food_database.json     # Final unified database
│   ├── fodmap_database.json           # Structured FODMAP data
│   ├── fodmap_database_pt.json        # FODMAP data in Portuguese
│   ├── fodmap_portuguese_equivalences.json # PT-EN food equivalences
│   └── tabela_alimentar_formatada.json # Formatted nutritional table
└── utils/                             # Visualization and exploration scripts
    ├── display_equivalences.py        # Display food equivalences
    ├── display_fodmap_summary.py      # Display FODMAP statistics
    ├── explore_unified_database.py    # Explore the unified database
    ├── show_improvements.py           # Show matching improvements
    ├── show_pasta_examples.py         # Example queries for pasta dishes
    └── show_summary.py                # General summary display
```

---

## Data Sources

### 1. Portuguese Nutritional Table (INSA TCA)

- **File**: `raw-data/insa_tca.xlsx`
- **Source**: Instituto Nacional de Saude Doutor Ricardo Jorge (INSA)
- **Content**: 1,372 foods with complete nutritional information
- **Fields**: Energy (kcal/kJ), macronutrients, vitamins, minerals (50+ fields)

### 2. FODMAP Lists

- **Files**: `raw-data/high_fodmap.txt`, `raw-data/low_fodmap.txt`, `raw-data/free_fodmap.txt`
- **Source**: Monash University FODMAP Database and multiple FODMAP sources
- **Content**: 559 foods categorized by FODMAP level
- **Levels**:
  - `high`: Foods to avoid or significantly reduce
  - `low`: Foods safe in moderate portions
  - `free`: Foods with negligible FODMAP content

---

## Pipeline Execution

Execute the scripts in numerical order from the `scripts/` directory. Each script uses relative paths, so they can be run from any directory:

```bash
cd database/scripts

# Step 1: Extract nutritional data from Excel
python 01_extract_nutrition_data.py

# Step 2: Format nutritional data with proper units
python 02_format_for_database.py

# Step 3: Extract and normalize Portuguese food names
python 03_extract_portuguese_names.py

# Step 4: Parse FODMAP text files into structured JSON
python 04_process_fodmap_data.py

# Step 5: Create Portuguese-English food equivalences
python 05_create_equivalences.py

# Step 6: Create basic unified database
python 06_create_unified_database.py

# Step 7: Create enhanced database with multi-ingredient detection
python 07_create_enhanced_unified_database.py
```

### Dependencies

```bash
pip install pandas openpyxl
```

The scripts use only Python standard library plus `pandas` for Excel parsing.

---

## Scripts Description

### 01_extract_nutrition_data.py

Reads the Portuguese nutritional table from Excel format and converts it to JSON.

- **Input**: `raw-data/insa_tca.xlsx`
- **Output**: `raw-data/tabela_alimentar_portugal.json`

### 02_format_for_database.py

Formats the raw nutritional data into a standardized structure with proper units (g, mg, ug, kcal, kJ).

- **Input**: `raw-data/tabela_alimentar_portugal.json`
- **Output**: `output/tabela_alimentar_formatada.json`

### 03_extract_portuguese_names.py

Extracts food names from the Portuguese table and creates normalized versions for text matching.

- **Input**: `raw-data/tabela_alimentar_portugal.json`
- **Output**: `raw-data/portuguese_food_names.json`

Normalization includes:
- Lowercase conversion
- Accent removal (a, e, i, o, u, c)
- Parenthetical content removal
- Punctuation standardization

### 04_process_fodmap_data.py

Parses the FODMAP text files (high, low, free) into structured JSON with categories, portion notes, and normalized names.

- **Input**: `raw-data/high_fodmap.txt`, `raw-data/low_fodmap.txt`, `raw-data/free_fodmap.txt`
- **Output**: `output/fodmap_database.json`

### 05_create_equivalences.py

Creates mappings between Portuguese food names and English FODMAP entries using:

1. **Dictionary matching**: 350+ English-Portuguese translations
2. **Fuzzy matching**: Sequence-based similarity for unmatched items

The translation dictionary covers:
- Vegetables (100+ terms)
- Fruits (60+ terms)
- Meats and fish (90+ terms)
- Dairy products (45+ terms)
- Cereals, grains, and pasta (90+ terms)
- Condiments and spices (100+ terms)

- **Input**: `output/fodmap_database.json`, `raw-data/portuguese_food_names.json`
- **Output**: `output/fodmap_portuguese_equivalences.json`
- **Match Rate**: ~72% (404 of 559 FODMAP foods matched)

### 06_create_unified_database.py

Creates the initial unified database by merging:
- All Portuguese nutritional entries
- FODMAP information where matches exist
- FODMAP-only entries for unmatched foods

- **Input**: `output/tabela_alimentar_formatada.json`, `output/fodmap_portuguese_equivalences.json`, `output/fodmap_database.json`
- **Output**: `output/unified_food_database.json` (v1)

### 07_create_enhanced_unified_database.py

Creates an enhanced version with multi-ingredient FODMAP detection for composite dishes.

Features:
- Keyword-based ingredient detection in food names
- Multiple FODMAP ingredients identification
- Aggregated FODMAP level calculation (highest level wins)
- Portuguese-to-English ingredient keyword mapping

- **Input**: `output/tabela_alimentar_formatada.json`, `output/fodmap_database.json`
- **Output**: `output/unified_food_database.json` (v2)

---

## Output Files

### unified_food_database.json (Main Output)

The primary output containing 1,931 foods with the following structure:

```json
{
  "metadata": {
    "database_name": "Enhanced Unified Portuguese Nutritional and FODMAP Database",
    "version": "2.0",
    "creation_date": "2025-12-09",
    "total_foods": 1931,
    "foods_with_fodmap_data": 1307,
    "foods_with_nutritional_data": 1372,
    "foods_with_multiple_ingredients": 512
  },
  "foods": [
    {
      "id": 624,
      "name": "Abacate, Hass",
      "source": "nutritional_table",
      "category_level_1": "Frutos e produtos derivados de frutos",
      "category_level_2": "Fruta utilizada como fruta",
      "category_level_3": "...",
      "fodmap": {
        "level": "high",
        "portion_note": "...",
        "additional_notes": "...",
        "search_information": {
          "match_type": "multiple_ingredients",
          "ingredients": [...]
        }
      },
      "nutrition": {
        "energy_kcal": 176.0,
        "macronutrients": {...},
        "vitamins": {...},
        "minerals": {...}
      }
    }
  ]
}
```

### fodmap_database.json

Structured FODMAP data with 559 foods:
- Organized by category and level
- Includes portion notes and recommendations
- Normalized names for matching

### fodmap_portuguese_equivalences.json

Portuguese-English food mappings with:
- Match scores (0-1)
- Match type (dictionary/similarity)
- Original and normalized names
- FODMAP information

---

## Utility Scripts

Located in `utils/`, these scripts help visualize and explore the data:

| Script | Description |
|--------|-------------|
| `display_equivalences.py` | Shows PT-EN food mappings organized by FODMAP level |
| `display_fodmap_summary.py` | Displays FODMAP database statistics and examples |
| `explore_unified_database.py` | Interactive exploration of the unified database |
| `show_improvements.py` | Compares matching rates before/after dictionary expansion |
| `show_pasta_examples.py` | Demonstrates multi-ingredient detection for pasta dishes |
| `show_summary.py` | General summary of all data files |

Run any utility script:
```bash
cd database/utils
python explore_unified_database.py
```

---

## Technical Details

### Matching Algorithm

1. **Normalization**: Both Portuguese and English names are normalized (lowercase, accent removal, punctuation standardization)

2. **Dictionary Lookup**: Direct translation using 350+ term dictionary covering:
   - British vs American English (courgette/zucchini, aubergine/eggplant)
   - Singular and plural forms (bean/beans, tomato/tomatoes)
   - Regional variations (prawns/shrimp, biscuit/cookie)

3. **Fuzzy Matching**: For unmatched items, uses `difflib.SequenceMatcher` with minimum threshold of 0.7

4. **Multi-ingredient Detection**: Scans composite dish names for FODMAP keywords (e.g., "Esparguete a bolonhesa" detects pasta, tomato, onion, garlic)

### FODMAP Level Aggregation

For foods with multiple detected ingredients:
- If any ingredient is `high` -> food is `high`
- Otherwise, if any ingredient is `low` -> food is `low`
- Otherwise -> food is `free`

### Data Coverage

| Metric | Count |
|--------|-------|
| Total foods in database | 1,931 |
| Foods with nutritional data | 1,372 |
| Foods with FODMAP data | 1,307 |
| Foods with multiple FODMAP ingredients | 512 |
| FODMAP foods matched to Portuguese | 404 (72.3%) |

---

## Notes

- This project was developed with AI assistance (GitHub Copilot/Claude) to handle the complexity of cross-language food matching and data integration
- The FODMAP information is based on publicly available sources and should not replace professional medical advice
- The Portuguese nutritional data comes from official INSA sources (v7.0, 2025)
- Some FODMAP entries remain in English when no Portuguese equivalent was found in the nutritional table
- The multi-ingredient detection is keyword-based and may not catch all ingredients in complex dishes

---

## License

The nutritional data is sourced from INSA's public database. FODMAP information is compiled from publicly available sources. Please refer to original sources for usage rights.
