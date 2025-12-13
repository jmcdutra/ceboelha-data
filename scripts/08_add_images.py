import json
import time
import random
from pathlib import Path
try:
    from ddgs import DDGS
except ImportError:
    # Handle the rename case where the package is installed as 'ddgs'
    from ddgs import DDGS
from tqdm import tqdm

def search_food_image(query):
    """
    Searches for a food image using DuckDuckGo.
    Returns the URL of the first result or None.
    """
    try:
        with DDGS() as ddgs:
            # Adding "food photography" or "real food" to improve quality
            search_query = f"{query} food photography"
            results = ddgs.images(
                search_query,
                region="wt-wt",
                safesearch="off",
                size="Medium",
                type_image="photo",
                layout="Wide",
                max_results=1
            )
            
            results_list = list(results)
            if results_list:
                return results_list[0]['image']
            
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
    
    return None

def main():
    base_dir = Path(__file__).parent.parent
    base_dir = Path(__file__).parent.parent
    original_file = base_dir / "output" / "unified_food_database.json"
    target_file = base_dir / "output" / "unified_food_database_with_images.json"
    
    # Logic to support resuming:
    # If the target file (with_images) exists, load it to allow skipping already fetched items.
    # Otherwise, load the original file.
    if target_file.exists():
        print(f"resuming from existing output file: {target_file.name}")
        load_path = target_file
    else:
        print(f"Starting fresh from original database: {original_file.name}")
        load_path = original_file
    
    print(f"Loading database from {load_path}...")
    with open(load_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    foods = data.get("foods", [])
    total_foods = len(foods)
    print(f"Found {total_foods} foods to process.")
    
    updated_count = 0
    skipped_count = 0
    
    print(f"Saving results to: {target_file.name}")
    
    print("Starting image enrichment...")
    
    try:
        for food in tqdm(foods, desc="Fetching images"):
            # Skip if already has image (in case we re-run)
            if "image_url" in food and food["image_url"]:
                skipped_count += 1
                continue
                
            # Prefer English name for better global results, fall back to Portuguese
            search_term = ""
            
            # Check for English name in fodmap -> search_information -> name_english
            # Or in search_information directly if structure matches
            # Let's inspect structure dynamically or just try potential paths
            
            name_en = None
            
            # Try to find english name in nested structures
            if "fodmap" in food and food["fodmap"]:
                fodmap_data = food["fodmap"]
                if "search_information" in fodmap_data:
                    search_info = fodmap_data["search_information"]
                    if "name_english" in search_info:
                        name_en = search_info["name_english"]
                    elif "ingredients" in search_info:
                         # composite dish, maybe take top ingredient or just use PT name
                         pass
            
            if name_en:
                # Clean up multiple English names if they are comma separated lista
                if "," in name_en:
                    # e.g. "Oils: Avocado oil, Canola oil..." -> take "Avocado oil"
                    # But simpler to just use the first part if it looks like a list
                    search_term = name_en.split(",")[0]
                else:
                    search_term = name_en
            else:
                search_term = food["name"]
                
                
            image_url = search_food_image(search_term)
            
            if image_url:
                food["image_url"] = image_url
                updated_count += 1
            else:
                # Fallback: try Portuguese name strict if English failed
                if name_en:
                     image_url = search_food_image(food["name"])
                     if image_url:
                        food["image_url"] = image_url
                        updated_count += 1
            
            # Rate limiting / politeness
            time.sleep(random.uniform(0.5, 1.5))
            
            # Periodic save (every 50 items)
            if updated_count % 50 == 0 and updated_count > 0:
                 with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
    except KeyboardInterrupt:
        print("\nStopping early... Saving progress.")
    except Exception as e:
        print(f"\nCritical error: {e}")
    finally:
        print(f"\nSaving final result to {target_file.name}...")
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Done! Updated: {updated_count}, Skipped: {skipped_count}, Total: {len(foods)}")

if __name__ == "__main__":
    main()
