import json
import os
import re
import urllib.request
from PIL import Image
import io

CATALOG_INPUT = '/Users/LUMÈRA_LUXE/private-source/catalog_100_input.json'
LEPERFUME_CATALOG = '/Users/LUMÈRA_LUXE/private-source/leperfumeqa_catalog.json'
EXISTING_PRODUCTS_JSON = '/Users/LUMÈRA_LUXE/src/data/products.json'
PUBLIC_PRODUCTS_DIR = '/Users/LUMÈRA_LUXE/public/assets/products'

os.makedirs(PUBLIC_PRODUCTS_DIR, exist_ok=True)

with open(CATALOG_INPUT, 'r', encoding='utf-8') as f:
    raw_100 = json.load(f)

with open(LEPERFUME_CATALOG, 'r', encoding='utf-8') as f:
    lp_products = json.load(f)

with open(EXISTING_PRODUCTS_JSON, 'r', encoding='utf-8') as f:
    existing_25 = json.load(f)

print(f"Loaded existing products: {len(existing_25)}")
print(f"Loaded total raw target items: {len(raw_100)}")
print(f"Loaded LePerfume products: {len(lp_products)}")

# Slugs currently used
existing_slugs = set(p['slug'] for p in existing_25)

def clean_tokens(t):
    return set(re.sub(r'[^a-z0-9]', ' ', t.lower()).split())

# Mapping configuration: SKU -> (search_keywords, preferred_tokens, default_family, default_notes)
CONFIG = {
    'LL-026': (['armani', 'acqua', 'gio'], ['edt', '200ml', '100ml'], 'Woody Aquatic', ['Calabrian Bergamot', 'Neroli', 'Green Tangerine', 'Jasmine', 'Rock Rose', 'Rosemary', 'Patchouli']),
    'LL-027': (['armani', 'acqua', 'gio', 'profondo'], ['edp'], 'Aromatic Aquatic', ['Marine Notes', 'Aquozone', 'Bergamot', 'Green Mandarin', 'Rosemary', 'Lavender', 'Cypress', 'Patchouli', 'Musk']),
    'LL-028': (['armani', 'acqua', 'gio'], ['parfum'], 'Woody Aquatic', ['Marine Notes', 'Bergamot', 'Rosemary', 'Clary Sage', 'Geranium', 'Olibanum', 'Patchouli']),
    'LL-029': (['armani', 'code'], ['parfum'], 'Woody Aromatic', ['Bergamot', 'Bergamot Leaf', 'Iris', 'Orris', 'Clary Sage', 'Tonka Bean', 'Cedarwood']),
    'LL-030': (['armani', 'code'], ['edt'], 'Amber Woody', ['Bergamot', 'Lemon', 'Star Anise', 'Olive Blossom', 'Guaiac Wood', 'Leather', 'Tobacco', 'Tonka Bean']),
    'LL-031': (['armani', 'my', 'way'], ['edp'], 'Floral', ['Orange Blossom', 'Bergamot', 'Tuberose', 'Indian Jasmine', 'Madagascar Vanilla', 'White Musk', 'Virginian Cedar']),
    'LL-032': (['armani', 'my', 'way', 'intense'], ['edp'], 'Floral Woody', ['Orange Blossom', 'Bitter Orange', 'Indian Tuberose', 'Tuberose', 'Madagascar Vanilla', 'Sandalwood']),
    'LL-033': (['armani', 'si'], ['edp'], 'Chypre Fruity', ['Cassis', 'Blackcurrant Nectar', 'May Rose', 'Freesia', 'Vanilla', 'Patchouli', 'Ambroxan', 'Woody Notes']),
    'LL-034': (['armani', 'si', 'passione'], ['edp'], 'Floral Fruity', ['Pear', 'Blackcurrant', 'Pink Pepper', 'Grapefruit', 'Pineapple', 'Rose', 'Jasmine', 'Heliotrope', 'Vanilla', 'Cedarwood']),
    'LL-035': (['dior', 'sauvage'], ['edt', 'toilette'], 'Aromatic Fougere', ['Calabrian Bergamot', 'Pepper', 'Sichuan Pepper', 'Lavender', 'Pink Pepper', 'Vetiver', 'Patchouli', 'Geranium', 'Ambroxan', 'Cedar']),
    'LL-036': (['dior', 'sauvage'], ['edp', 'parfum'], 'Amber Fougere', ['Bergamot', 'Sichuan Pepper', 'Lavender', 'Star Anise', 'Nutmeg', 'Ambroxan', 'Vanilla']),
    'LL-037': (['dior', 'sauvage', 'elixir'], [], 'Aromatic Spiced', ['Cinnamon', 'Nutmeg', 'Cardamom', 'Grapefruit', 'Lavender', 'Licorice', 'Sandalwood', 'Amber', 'Patchouli', 'Haitian Vetiver']),
    'LL-038': (['miss', 'dior'], ['edp', 'parfum'], 'Floral', ['Iris', 'Peony', 'Lily-of-the-Valley', 'Centifolia Rose', 'Apricot', 'Peach', 'Vanilla', 'Tonka Bean', 'Musk', 'Benzoin', 'Sandalwood']),
    'LL-039': (['dior', 'adore'], ['edp'], 'Floral Fruity', ['Pear', 'Melon', 'Magnolia', 'Peach', 'Mandarin Orange', 'Bergamot', 'Jasmine', 'Lily-of-the-Valley', 'Tuberose', 'Freesia', 'Rose', 'Orchid', 'Vanilla', 'Blackberry']),
    'LL-040': (['dior', 'homme'], ['toilette', 'parfum', 'edt'], 'Woody Floral Musk', ['Lavender', 'Iris', 'Ambrette', 'Pear', 'Virginia Cedar', 'Vetiver']),
    'LL-041': (['dior', 'poison'], ['toilette', 'edt'], 'Amber Vanilla', ['Coconut', 'Plum', 'Apricot', 'Brazilian Rosewood', 'Jasmine', 'Caraway', 'Tuberose', 'Rose', 'Lily-of-the-Valley', 'Vanilla', 'Almond', 'Sandalwood']),
    'LL-042': (['libre'], ['edp'], 'Amber Floral', ['Lavender', 'Mandarin Orange', 'Blackcurrant', 'Petitgrain', 'Orange Blossom', 'Jasmine', 'Madagascar Vanilla', 'Musk', 'Cedar', 'Ambergris']),
    'LL-043': (['libre'], ['intense', 'edp'], 'Amber Floral', ['Lavender', 'Mandarin Orange', 'Bergamot', 'French Lavender', 'Orange Blossom', 'Jasmine Sambac', 'Orchid', 'Madagascar Vanilla', 'Tonka Bean', 'Ambergris']),
    'LL-044': (['libre'], ['edt'], 'Floral', ['Lavender', 'Bergamot', 'Mandarin Orange', 'Orange Blossom', 'Jasmine Tea', 'White Jasmine', 'Musk', 'Vanilla', 'Ambergris']),
    'LL-045': (['black', 'opium'], ['edp'], 'Amber Vanilla', ['Pear', 'Pink Pepper', 'Orange Blossom', 'Coffee', 'Jasmine', 'Bitter Almond', 'Licorice', 'Vanilla', 'Patchouli', 'Cashmere Wood', 'Cedar']),
    'LL-046': (['ysl', 'y'], ['edp'], 'Aromatic Fougere', ['Apple', 'Ginger', 'Bergamot', 'Sage', 'Juniper Berries', 'Geranium', 'Amberwood', 'Tonka Bean', 'Cedar', 'Vetiver', 'Olibanum']),
    'LL-047': (['ysl', 'y'], ['edt'], 'Aromatic Fougere', ['Aldehydes', 'Bergamot', 'Ginger', 'Mint', 'Lemon', 'Apple', 'Violet Leaf', 'Sage', 'Pineapple', 'Geranium', 'Ambergris', 'Musk', 'Cedar', 'Vetiver']),
    'LL-048': (['myslf'], ['edp', 'parfum'], 'Aromatic Floral', ['Calabrian Bergamot', 'Bergamot', 'Tunisian Orange Blossom', 'Ambrofix', 'Patchouli']),
    'LL-049': (['versace', 'eros'], ['edp', 'energy'], 'Amber Woody', ['Mint', 'Candy Apple', 'Lemon', 'Mandarin Orange', 'Ambroxan', 'Geranium', 'Clary Sage', 'Vanilla', 'Cedar', 'Sandalwood', 'Patchouli']),
    'LL-050': (['eros', 'flame'], ['edp'], 'Woody Spicy', ['Mandarin Orange', 'Black Pepper', 'Chinotto', 'Lemon', 'Rosemary', 'Pepper', 'Geranium', 'Rose', 'Vanilla', 'Tonka Bean', 'Sandalwood', 'Cedar', 'Oakmoss']),
    'LL-051': (['eros', 'femme'], ['edp'], 'Floral Woody Musk', ['Sicilian Lemon', 'Pomegranate', 'Calabrian Bergamot', 'Lemon Blossom', 'Jasmine Sambac', 'Jasmine', 'Peony', 'Musk', 'Ambroxan', 'Sandalwood']),
    'LL-052': (['dylan', 'blue'], ['edt'], 'Aromatic Fougere', ['Calabrian Bergamot', 'Water Notes', 'Grapefruit', 'Fig Leaf', 'Ambroxan', 'Black Pepper', 'Patchouli', 'Violet Leaf', 'Papyrus', 'Incense', 'Musk']),
    'LL-053': (['bright', 'crystal'], ['edt', 'parfum'], 'Floral Fruity', ['Yuzu', 'Pomegranate', 'Ice', 'Peony', 'Lotus', 'Magnolia', 'Musk', 'Mahogany', 'Amber']),
    'LL-054': (['crystal', 'noir'], ['edt', 'edp'], 'Amber Floral', ['Pepper', 'Ginger', 'Cardamom', 'Coconut', 'Gardenia', 'Orange Blossom', 'Peony', 'Sandalwood', 'Musk', 'Amber']),
    'LL-055': (['versace', 'homme'], ['edt'], 'Aromatic Fougere', ['Lemon', 'Bergamot', 'Neroli', 'Rose de Mai', 'Hyacinth', 'Cedar', 'Clary Sage', 'Geranium', 'Tonka Bean', 'Musk', 'Amber']),
    'LL-056': (['burberry', 'her'], ['edp'], 'Floral Fruity Gourmand', ['Strawberry', 'Raspberry', 'Blackberry', 'Sour Cherry', 'Blackcurrant', 'Mandarin Orange', 'Lemon', 'Violet', 'Jasmine', 'Musk', 'Vanilla', 'Amber']),
    'LL-057': (['burberry', 'her'], ['intense', 'elixir'], 'Floral Fruity Gourmand', ['Red Fruits', 'Dark Berries', 'Jasmine', 'Benzoin', 'Vanilla', 'Amber']),
    'LL-058': (['burberry', 'goddes'], ['edp'], 'Aromatic Gourmand', ['Vanilla Infusion', 'Lavender', 'Vanilla Caviar', 'Vanilla Absolute']),
    'LL-059': (['burberry', 'brit'], ['edt'], 'Amber Woody', ['Green Mandarin', 'Ginger', 'Bergamot', 'Cardamom', 'Nutmeg', 'Cedar', 'Wild Rose', 'Tonka Bean', 'Patchouli', 'Oriental Wood Notes']),
    'LL-060': (['burberry', 'hero'], ['edp'], 'Woody', ['Pine Needles', 'Olibanum', 'Benzoin', 'Incense', 'Atlas Cedar', 'Virginian Cedar', 'Himalayan Cedar']),
    'LL-061': (['burberry', 'mr'], ['edp', 'edt'], 'Woody Aromatic', ['Cardamom', 'Mint', 'Grapefruit', 'Tarragon', 'Lavender', 'Nutmeg', 'Cedar', 'Patchouli', 'Cinnamon', 'Amber', 'Benzoin', 'Vetiver']),
    'LL-062': (['gucci', 'bloom'], ['edp'], 'Floral', ['Jasmine', 'Tuberose', 'Rangoon Creeper']),
    'LL-063': (['gorgeous', 'gardenia'], ['edp'], 'Floral', ['Pear Blossom', 'Red Berries', 'Italian Mandarin', 'Gardenia', 'Jasmine', 'Frangipani', 'Brown Sugar', 'Patchouli']),
    'LL-064': (['gorgeous', 'jasmine'], ['edp'], 'Floral', ['Italian Mandarin', 'Bergamot', 'Black Pepper', 'Jasmine', 'Jasmine Sambac', 'Magnolia', 'Damask Rose', 'Benzoin', 'Patchouli']),
    'LL-065': (['gucci', 'guilty'], ['edt', 'men', 'm'], 'Woody Aromatic', ['Lavender', 'Amalfi Lemon', 'Orange Flower', 'Virginia Cedar', 'Patchouli', 'Vanilla']),
    'LL-066': (['gucci', 'guilty'], ['edp', 'women', 'w', 'femme'], 'Amber Floral', ['Pink Pepper', 'Mandora', 'Bergamot', 'Lilac', 'Violet', 'Geranium', 'Rose', 'Patchouli', 'Amber']),
    'LL-067': (['paradoxe'], ['edp'], 'Amber Floral', ['Pear', 'Tangerine', 'Calabrian Bergamot', 'Orange Blossom', 'Jasmine Sambac', 'Neroli Essence', 'Bourbon Vanilla', 'White Musk', 'Amber', 'Benzoin']),
    'LL-068': (['paradoxe', 'intense'], ['edp'], 'Amber Floral', ['Pear', 'Neroli', 'Bergamot', 'Moss', 'Jasmine', 'Neroli Essence', 'Bourbon Vanilla', 'Ambrofix', 'Amber', 'Serenolide']),
    'LL-069': (['luna', 'rossa', 'ocean'], ['edt', 'edp'], 'Aromatic Fougere', ['Bergamot', 'Pink Pepper', 'Artemisia', 'Lavender', 'Iris', 'Sage', 'Suede', 'Saffron', 'Musk', 'Haitian Vetiver', 'Caramel']),
    'LL-070': (['luna', 'rossa', 'carbon'], ['edt'], 'Aromatic Fougere', ['Bergamot', 'Pepper', 'Lavender', 'Metallic Notes', 'Coal', 'Watery Notes', 'Soil Tincture', 'Ambroxan', 'Patchouli']),
    'LL-071': (['vie', 'belle'], ['edp'], 'Floral Fruity Gourmand', ['Blackcurrant', 'Pear', 'Iris', 'Jasmine', 'Orange Blossom', 'Praline', 'Vanilla', 'Patchouli', 'Tonka Bean']),
    'LL-072': (['idole'], ['edp'], 'Amber Floral', ['Grasse Rose', 'Rose', 'Turkish Rose', 'Caramel', 'Popcorn', 'Vanilla']),
    'LL-073': (['tresor'], ['edp'], 'Floral Woody Musk', ['Raspberry', 'Rose', 'Cassis', 'Pink Pepper', 'Peony', 'Jasmine', 'Vanille', 'Musk', 'Virginia Cedar']),
    'LL-074': (['vie', 'belle', 'elixir'], ['edp'], 'Floral Fruity', ['Raspberry', 'Liquor', 'Calabrian Bergamot', 'Violet Leaf', 'Rose', 'Leather', 'Cocoa Butter', 'Cedarwood']),
    'LL-075': (['good', 'girl'], ['edp'], 'Amber Floral', ['Almond', 'Coffee', 'Bergamot', 'Lemon', 'Tuberose', 'Jasmine Sambac', 'Orange Blossom', 'Orris', 'Tonka Bean', 'Cacao', 'Vanilla', 'Praline']),
    'LL-076': (['good', 'girl', 'very'], ['edp'], 'Floral Fruity', ['Redcurrant', 'Litchi', 'Rose', 'Vanilla', 'Vetiver']),
    'LL-077': (['bad', 'boy'], ['edt'], 'Amber Spicy', ['White Pepper', 'Black Pepper', 'Bergamot', 'Cedar', 'Sage', 'Tonka Bean', 'Cacao', 'Amberwood']),
    'LL-078': (['212', 'vip', 'rose'], ['edp'], 'Floral Fruity', ['Champagne Rosé', 'Pink Pepper', 'Peach Blossom', 'Rose', 'White Musk', 'Woody Notes']),
    'LL-079': (['212', 'nyc'], ['edt'], 'Woody Floral Musk', ['Green Notes', 'Grapefruit', 'Spices', 'Bergamot', 'Lavender', 'Petitgrain', 'Ginger', 'Violet', 'Gardenia', 'Sage', 'Musk', 'Sandalwood']),
    'LL-080': (['light', 'blue'], ['women', 'w', 'femme', 'edt'], 'Floral Fruity', ['Sicilian Lemon', 'Apple', 'Cedar', 'Bellflower', 'Bamboo', 'Jasmine', 'White Rose', 'Cedar', 'Musk', 'Amber']),
    'LL-081': (['light', 'blue'], ['homme', 'men', 'm', 'edt'], 'Citrus Aromatic', ['Grapefruit', 'Bergamot', 'Sicilian Mandarin', 'Juniper', 'Pepper', 'Rosemary', 'Brazilian Rosewood', 'Musk']),
    'LL-082': (['dolce', 'k'], ['edp'], 'Woody Aromatic', ['Blood Orange', 'Pimento', 'Juniper Berries', 'Lemon', 'Sicilian Lemon', 'Cardamom', 'Fig Nectar', 'Geranium', 'Clary Sage', 'Lavender', 'Cedar', 'Patchouli']),
    'LL-083': (['dolce', 'one'], ['men', 'homme', 'm', 'edp'], 'Woody Spicy', ['Grapefruit', 'Coriander', 'Basil', 'Ginger', 'Cardamom', 'Orange Blossom', 'Amber', 'Tobacco', 'Cedar']),
    'LL-084': (['male'], ['edt'], 'Amber Fougere', ['Lavender', 'Mint', 'Cardamom', 'Bergamot', 'Artemisia', 'Cinnamon', 'Orange Blossom', 'Caraway', 'Vanilla', 'Tonka Bean', 'Amber', 'Sandalwood']),
    'LL-085': (['male', 'elixir'], ['parfum'], 'Amber Fougere', ['Lavender', 'Mint', 'Vanilla', 'Benzoin', 'Honey', 'Tonka Bean', 'Tobacco']),
    'LL-086': (['scandal'], ['edp'], 'Chypre Floral', ['Blood Orange', 'Mandarin Orange', 'Honey', 'Gardenia', 'Orange Blossom', 'Jasmine', 'Peach', 'Beeswax', 'Caramel', 'Patchouli', 'Licorice']),
    'LL-087': (['belle'], ['edp'], 'Amber Vanilla', ['Pear', 'Bergamot', 'Floral Notes', 'Leather', 'Vanilla', 'Vetiver', 'Amber', 'Musk']),
    'LL-088': (['explorer'], ['edp'], 'Woody Aromatic', ['Bergamot', 'Pink Pepper', 'Clary Sage', 'Haitian Vetiver', 'Leather', 'Ambroxan', 'Akigalawood', 'Patchouli Leaf', 'Cacao Pod']),
    'LL-089': (['montblanc', 'legend'] if True else ['mont', 'blanc', 'legend'], ['edt'], 'Aromatic Fougere', ['Lavender', 'Pineapple', 'Bergamot', 'Lemon Verbena', 'Red Apple', 'Dried Fruits', 'Oakmoss', 'Geranium', 'Coumarin']),
    'LL-090': (['legend', 'spirit'], ['edt'], 'Woody Aromatic', ['Grapefruit', 'Bergamot', 'Pink Pepper', 'Water Notes', 'Lavender', 'Cardamom', 'White Musk', 'White Woods', 'Cashmere Wood']),
    'LL-091': (['ck', 'one', 'edt'], ['200ml'], 'Citrus Aromatic', ['Lemon', 'Green Notes', 'Bergamot', 'Pineapple', 'Mandarin Orange', 'Cardamom', 'Papaya', 'Lily-of-the-Valley', 'Jasmine', 'Violet', 'Nutmeg']),
    'LL-092': (['euphoria'], ['edp'], 'Amber Floral', ['Pomegranate', 'Persimmon', 'Green Accord', 'Black Orchid', 'Lotus', 'Champaca', 'Mahogany', 'Amber', 'Black Violet', 'Whipped Cream']),
    'LL-093': (['eternity'], ['men', 'homme', 'm', 'edt'], 'Aromatic Fougere', ['Lavender', 'Lemon', 'Bergamot', 'Mandarin Orange', 'Sage', 'Juniper Berries', 'Basil', 'Geranium', 'Coriander', 'Jasmine']),
    'LL-094': (['boss', 'bottled'], ['edt'], 'Woody Spicy', ['Apple', 'Plum', 'Bergamot', 'Lemon', 'Oakmoss', 'Geranium', 'Cinnamon', 'Mahogany', 'Carnation', 'Vanilla', 'Sandalwood', 'Cedar']),
    'LL-095': (['boss', 'scent'], ['edt'], 'Aromatic Spicy', ['Ginger', 'Mandarin Orange', 'Bergamot', 'Maninka', 'Lavender', 'Leather', 'Woody Notes']),
    'LL-096': (['boss', 'bottled', 'elixir'], ['parfum'], 'Amber Woody', ['Frankincense', 'Cardamom', 'Patchouli', 'Vetiver', 'Labdanum', 'Cedarwood']),
    'LL-097': (['born', 'roma'], ['donna', 'women', 'w', 'edp'], 'Amber Floral', ['Blackcurrant', 'Pink Pepper', 'Bergamot', 'Jasmine', 'Jasmine Sambac', 'Jasmine Tea', 'Bourbon Vanilla', 'Cashmeran']),
    'LL-098': (['born', 'roma'], ['uomo', 'men', 'm', 'edt', 'edp'], 'Amber Vanilla', ['Vanilla', 'Bourbon Vanilla', 'Lavender', 'Vetiver']),
    'LL-099': (['valentino', 'donna'], ['edp'], 'Amber Floral', ['Italian Bergamot', 'Bulgarian Rose', 'Iris', 'Patchouli', 'Leather', 'Vanilla']),
    'LL-100': (['flowerbomb'], ['edp'], 'Amber Floral', ['Tea', 'Bergamot', 'Osmanthus', 'Orchid', 'Jasmine', 'Rose', 'Freesia', 'African Orange Flower', 'Patchouli', 'Musk', 'Vanilla']),
}

def extract_size_ml(title, default_ml=100):
    m = re.search(r'(\d+)\s*ml', title, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return default_ml

def extract_concentration(title, default_c="Eau de Parfum"):
    t = title.upper()
    if 'ELIXIR' in t: return 'Parfum Elixir'
    if 'PARFUM' in t: return 'Parfum'
    if 'EDT' in t or 'TOILETTE' in t: return 'Eau de Toilette'
    if 'EDP' in t: return 'Eau de Parfum'
    return default_c

def slugify(text):
    text = text.lower().replace('&', 'and')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

new_catalog_items = []
row_counter = 28

for raw_item in raw_100[25:]:
    sku = raw_item['SKU']
    brand = raw_item['Brand']
    orig_name = raw_item['Product Name']
    
    if sku not in CONFIG:
        print(f"Skipping unconfigured {sku}")
        continue
        
    req_tokens, pref_tokens, family, notes = CONFIG[sku]
    
    # Find matching product from LePerfume
    candidates = []
    for p in lp_products:
        t_clean = clean_tokens(p['title']) | clean_tokens(p.get('vendor', ''))
        if all(any(r in tok for tok in t_clean) for r in req_tokens):
            score = sum(3 for pr in pref_tokens if any(pr in tok for tok in t_clean))
            candidates.append((score, p))
            
    if not candidates:
        print(f"WARNING: No candidate found for {sku} ({orig_name})")
        price = 350.0
        lp_title = orig_name + " 100ml"
        img_src = None
    else:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_lp = candidates[0][1]
        price = float(best_lp['variants'][0]['price']) if best_lp.get('variants') else 350.0
        lp_title = best_lp['title']
        img_src = best_lp['images'][0]['src'] if best_lp.get('images') else None
        
    # Standardize clean perfume name
    clean_pname = orig_name
    if clean_pname.lower().startswith(brand.lower()):
        clean_pname = clean_pname[len(brand):].strip()
    display_name = re.sub(r'\b(EDP|EDT|Parfum|EDU)\b', '', clean_pname, flags=re.IGNORECASE).strip()
    
    size_ml = extract_size_ml(lp_title, default_ml=100)
    concentration = extract_concentration(lp_title)
    
    base_slug = slugify(f"{brand} {display_name}")
    slug = base_slug
    if slug in existing_slugs:
        slug = f"{base_slug}-{slugify(concentration)}"
    if slug in existing_slugs:
        slug = f"{slug}-{size_ml}ml"
    existing_slugs.add(slug)
    
    img_dest_path = f"/assets/products/{slug}.webp"
    local_img_file = os.path.join(PUBLIC_PRODUCTS_DIR, f"{slug}.webp")
    
    if img_src and not os.path.exists(local_img_file):
        try:
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
            req = urllib.request.Request(img_src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
            img = Image.open(io.BytesIO(data))
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            img.save(local_img_file, 'WEBP', quality=85)
            print(f"[{sku}] Processed image: {slug}.webp")
        except Exception as e:
            print(f"[{sku}] Image error for {img_src}: {e}")
    elif os.path.exists(local_img_file):
        print(f"[{sku}] Using existing image: {slug}.webp")
    else:
        print(f"[{sku}] No image available for {slug}")
        
    families = [f.strip() for f in family.split('/')] if '/' in family else [family]
    notes_str = ", ".join(notes)
    short_notes_preview = ", ".join(notes[:4])
    description = (
        f"An iconic fragrance masterpiece by {brand}. {display_name} unfolds with exquisite accords of "
        f"{short_notes_preview}, embodying timeless luxury, elegance, and distinction."
    )
    
    price_minor = int(price * 100)
    price_display = f"{int(price)} QAR"
    
    product_obj = {
        "id": f"lum_{str(row_counter).zfill(3)}",
        "row": row_counter,
        "sku": sku,
        "slug": slug,
        "brand": brand,
        "name": display_name,
        "fullName": f"{brand} {display_name}",
        "sizeMl": size_ml,
        "sizeDisplay": f"{size_ml}ml",
        "concentration": concentration,
        "currency": "QAR",
        "priceMinor": price_minor,
        "priceDisplay": price_display,
        "stickerPriceMinor": None,
        "image": img_dest_path,
        "scentFamilies": families,
        "keyNotes": notes,
        "rawNotes": notes_str,
        "description": description,
        "isDraft": False,
        "draftReason": [],
        "featured": sku in ['LL-035', 'LL-042', 'LL-049', 'LL-067', 'LL-075', 'LL-084', 'LL-100']
    }
    
    new_catalog_items.append(product_obj)
    row_counter += 1

print(f"\nGenerated {len(new_catalog_items)} new products!")

full_100_catalog = existing_25 + new_catalog_items
print(f"Total unified catalog count: {len(full_100_catalog)}")

with open(EXISTING_PRODUCTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(full_100_catalog, f, indent=2, ensure_ascii=False)

print(f"Successfully updated {EXISTING_PRODUCTS_JSON}!")
