import json
import os
import re
import urllib.request
from PIL import Image
import io

CATALOG_INPUT_100 = '/Users/LUMÈRA_LUXE/private-source/catalog_100_input.json'
LEPERFUME_CATALOG = '/Users/LUMÈRA_LUXE/private-source/leperfumeqa_catalog.json'
EXISTING_PRODUCTS_JSON = '/Users/LUMÈRA_LUXE/src/data/products.json'
PUBLIC_PRODUCTS_DIR = '/Users/LUMÈRA_LUXE/public/assets/products'

os.makedirs(PUBLIC_PRODUCTS_DIR, exist_ok=True)

with open(EXISTING_PRODUCTS_JSON, 'r', encoding='utf-8') as f:
    existing_all = json.load(f)

# The original 25 products from the client's Excel sheet are indices 0..24
original_25 = existing_all[:25]

# Fix lum_021 Juicy Couture name if blank
for p in original_25:
    if p['id'] == 'lum_021' and (not p.get('name') or p.get('name').strip() == ''):
        p['name'] = 'Viva La Juicy'
        p['fullName'] = 'Juicy Couture Viva La Juicy'
        p['slug'] = 'juicy-couture-viva-la-juicy'
        p['category'] = 'oriental'
        p['scentFamilies'] = ['Amber & Oriental', 'Gourmand']

# Precise category mapping for the original 25
ORIGINAL_25_CATEGORIES = {
    'lum_003': ('floral', ['Floral & Rose', 'Floral Oriental']),
    'lum_004': ('fresh', ['Fresh & Citrus', 'Floral Woody Musk']),
    'lum_005': ('oriental', ['Amber & Oriental', 'Fruity Gourmand']),
    'lum_006': ('floral', ['Floral & Rose', 'Amber Floral']),
    'lum_007': ('oriental', ['Amber & Oriental', 'Warm Floral Leather']),
    'lum_008': ('floral', ['Floral & Rose', 'Floral Aldehydic']),
    'lum_009': ('woody', ['Woody & Earthy', 'Chypre Floral']),
    'lum_010': ('fresh', ['Fresh & Citrus', 'Fresh Floral']),
    'lum_011': ('oriental', ['Amber & Oriental', 'Amber Floral']),
    'lum_012': ('oriental', ['Amber & Oriental', 'Gourmand Citrus']),
    'lum_013': ('oriental', ['Amber & Oriental', 'Warm Amber Floral']),
    'lum_014': ('oriental', ['Amber & Oriental', 'Gourmand Vanilla']),
    'lum_015': ('floral', ['Floral & Rose', 'Floral Fruity']),
    'lum_016': ('fresh', ['Fresh & Citrus', 'Aquatic Floral']),
    'lum_017': ('floral', ['Floral & Rose', 'Solar Floral']),
    'lum_018': ('oriental', ['Amber & Oriental', 'Spicy Fruity Amber']),
    'lum_019': ('oriental', ['Amber & Oriental', 'Honey Amber Floral']),
    'lum_020': ('floral', ['Floral & Rose', 'Solar Floral Amber']),
    'lum_021': ('oriental', ['Amber & Oriental', 'Floral Fruity Gourmand']),
    'lum_022': ('floral', ['Floral & Rose', 'Floral Musky']),
    'lum_023': ('floral', ['Floral & Rose', 'Fruity Floral']),
    'lum_024': ('floral', ['Floral & Rose', 'Berry Floral']),
    'lum_025': ('woody', ['Woody & Earthy', 'Floral Woody Musk']),
    'lum_026': ('oriental', ['Amber & Oriental', 'Honey White Floral']),
    'lum_027': ('oriental', ['Amber & Oriental', 'Amber Floral'])
}

for p in original_25:
    pid = p['id']
    if pid in ORIGINAL_25_CATEGORIES:
        cat, fams = ORIGINAL_25_CATEGORIES[pid]
        p['category'] = cat
        p['scentFamilies'] = fams

with open(LEPERFUME_CATALOG, 'r', encoding='utf-8') as f:
    lp_products = json.load(f)

print(f"Loaded {len(original_25)} original client products.")
print(f"Loaded {len(lp_products)} products from LePerfume catalog.")

def is_men_title(t):
    t_clean = re.sub(r'women|femme', '', t.lower())
    if re.search(r'\b(men|homme|uomo|boy|male)\b', t_clean):
        return True
    if '(m)' in t.lower() or ' (m)' in t.lower():
        return True
    return False

def find_leperfume_product(req_tokens, pref_tokens=[]):
    candidates = []
    for item in lp_products:
        t = item['title'].lower()
        if not item.get('images'):
            continue
        if is_men_title(t):
            continue
        if all(r in t for r in req_tokens):
            score = sum(3 for pr in pref_tokens if pr in t)
            candidates.append((score, item))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    return None

# The 75 carefully selected WOMEN'S PERFUMES across top luxury houses:
NEW_75_WOMENS = [
    # --- FRESH & CITRUS (18 items) ---
    ('LL-026', 'Dolce & Gabbana', 'Light Blue', ['light blue', 'edt'], ['100ml', 'women', '(w)', 'l'], 'fresh', ['Fresh & Citrus', 'Citrus Woody'], ['Sicilian Lemon', 'Apple', 'Cedar', 'Bellflower', 'Bamboo', 'Jasmine', 'White Rose', 'Amber', 'Musk'], 360.0, 100, 'Eau de Toilette'),
    ('LL-027', 'Chanel', 'Chance Eau Tendre', ['chance', 'eau tendre'], ['100ml', 'edt'], 'fresh', ['Fresh & Citrus', 'Fruity Fresh'], ['Grapefruit', 'Quince', 'Jasmine', 'Hyacinth', 'White Musk', 'Iris', 'Cedar', 'Amber'], 585.0, 100, 'Eau de Toilette'),
    ('LL-028', 'Guerlain', 'Aqua Allegoria Pamplelune', ['aqua allegoria', 'pamplelune'], ['75'], 'fresh', ['Fresh & Citrus', 'Citrus Aromatic'], ['Grapefruit', 'Bergamot', 'Petitgrain', 'Cassis', 'Neroli', 'Patchouli', 'Vanilla'], 299.0, 75, 'Eau de Toilette'),
    ('LL-029', 'Versace', 'Dylan Turquoise', ['dylan turquoise'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Floral Woody'], ['Primofiore Lemon', 'Sicilian Mandarin', 'Pink Pepper', 'Guava', 'Freesia', 'Cassis', 'Jasmine', 'Clearwood', 'Musk', 'Cedar'], 340.0, 100, 'Eau de Toilette'),
    ('LL-030', 'Dolce & Gabbana', 'Dolce Shine', ['dolce', 'shine'], ['75ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral Fresh'], ['Mango', 'Grapefruit', 'Quince', 'Jasmine', 'Orange Blossom', 'Solar Notes', 'White Woods', 'Australian Sandalwood', 'White Musk'], 345.0, 75, 'Eau de Parfum'),
    ('LL-031', 'Moschino', 'Toy 2', ['toy 2'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Floral Woody'], ['Granny Smith Apple', 'Mandarin Orange', 'Magnolia', 'White Currant', 'Peony', 'Jasmine', 'Musk', 'Sandalwood', 'Amberwood'], 260.0, 100, 'Eau de Parfum'),
    ('LL-032', 'Moschino', 'Cheap & Chic So Real', ['cheap & chic', 'so real'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Citrus Floral'], ['Bitter Orange', 'Tangerine', 'Raspberry', 'Blackcurrant', 'Pink Peony', 'Magnolia', 'Jasmine', 'Ambroxan', 'Cedar', 'Oakmoss'], 159.0, 100, 'Eau de Toilette'),
    ('LL-033', 'Hermès', 'Twilly Eau Ginger', ['twilly', 'ginger'], ['85ml'], 'fresh', ['Fresh & Citrus', 'Floral Spicy Fresh'], ['Candied Ginger', 'Peony', 'Cedarwood'], 435.0, 85, 'Eau de Parfum'),
    ('LL-034', 'Bvlgari', 'Omnia Crystalline', ['omnia', 'crystalline'], ['100ml', '65ml'], 'fresh', ['Fresh & Citrus', 'Aquatic Floral'], ['Bamboo', 'Nashi Pear', 'Lotus', 'Cassia', 'Tea', 'Guaiac Wood', 'Musk', 'Oakmoss'], 340.0, 65, 'Eau de Toilette'),
    ('LL-035', 'Lancôme', 'Miracle', ['miracle'], ['women', '100ml'], 'fresh', ['Fresh & Citrus', 'Fresh Spicy Floral'], ['Litchi', 'Freesia', 'Magnolia', 'Pepper', 'Ginger', 'Mandarin Orange', 'Jasmine', 'Musk', 'Amber'], 360.0, 100, 'Eau de Parfum'),
    ('LL-036', 'Versace', 'Bright Crystal', ['bright crystal'], ['90ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral'], ['Yuzu', 'Pomegranate', 'Ice Accord', 'Peony', 'Lotus', 'Magnolia', 'Musk', 'Mahogany', 'Amber'], 320.0, 90, 'Eau de Toilette'),
    ('LL-037', 'Giorgio Armani', 'My Way Floral', ['my way', 'floral'], ['90ml'], 'fresh', ['Fresh & Citrus', 'Fresh Floral'], ['Green Mandarin', 'Orange Blossom', 'Tuberose', 'Neroli', 'Bourbon Vanilla', 'White Musk'], 450.0, 90, 'Eau de Parfum'),
    ('LL-038', 'Dior', 'Joy', ['joy'], ['90ml', '100ml'], 'fresh', ['Fresh & Citrus', 'Citrus Floral'], ['Bergamot', 'Mandarin Orange', 'Grasse Rose', 'Jasmine', 'Sandalwood', 'Cedar', 'White Musk', 'Patchouli'], 520.0, 90, 'Eau de Parfum'),
    ('LL-039', 'Calvin Klein', 'Eternity for Women', ['ck eternity', 'w'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Green Floral'], ['Green Notes', 'Freesia', 'Sage', 'Citrus', 'Mandarin Orange', 'Carnation', 'Lily', 'Lily-of-the-Valley', 'Jasmine', 'Marigold', 'Rose', 'Heliotrope', 'Musk', 'Sandalwood', 'Patchouli', 'Amber'], 210.0, 100, 'Eau de Parfum'),
    ('LL-040', 'Cartier', 'Baiser Volé', ['baiser', 'vole'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Fresh Green Floral'], ['Lily', 'Citrus', 'Green Lily Leaves', 'Green Notes'], 390.0, 100, 'Eau de Parfum'),
    ('LL-041', 'Paco Rabanne', 'Olympéa Solar', ['olympea', 'solar'], ['80ml'], 'fresh', ['Fresh & Citrus', 'Solar Citrus Floral'], ['Orange Blossom', 'Mandarin Orange', 'Orange Peel', 'Solar Notes', 'Tiare Flower', 'White Flowers', 'Oakmoss', 'Benzoin', 'Ylang-Ylang'], 249.0, 80, 'Eau de Parfum Intense'),
    ('LL-042', 'Parfums de Marly', 'Valaya', ['valaya'], ['75ml'], 'fresh', ['Fresh & Citrus', 'Floral Aldehydic'], ['Aldehydes', 'White Peach', 'Bergamot', 'Mandarin Orange', 'Orange Blossom', 'Petalia', 'Lily-of-the-Valley', 'Vetiver', 'Akigalawood', 'Ambrofix', 'Vanilla'], 850.0, 75, 'Eau de Parfum'),
    ('LL-043', 'Dolce & Gabbana', 'L’Impératrice', ['imperatrice'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Aquatic Fruity Citrus'], ['Kiwi', 'Rhubarb', 'Pink Pepper', 'Watermelon', 'Cyclamen', 'Jasmine', 'Lemon Tree', 'Sandalwood', 'Musk'], 340.0, 100, 'Eau de Toilette'),

    # --- FLORAL & ROSE (26 items) ---
    ('LL-044', 'Chanel', 'Coco Mademoiselle', ['coco', 'mademoiselle'], ['100ml', 'edp'], 'floral', ['Floral & Rose', 'Amber Floral'], ['Orange', 'Bergamot', 'Mandarin Orange', 'Turkish Rose', 'Jasmine', 'Mimosa', 'Ylang-Ylang', 'Patchouli', 'White Musk', 'Vanilla', 'Vetiver', 'Tonka Bean'], 699.0, 100, 'Eau de Parfum'),
    ('LL-045', 'Dior', 'Miss Dior', ['miss dior'], ['100ml', 'edp'], 'floral', ['Floral & Rose', 'Floral Bouquet'], ['Centifolia Rose', 'Lily-of-the-Valley', 'Peony', 'Iris', 'Apricot', 'Peach', 'Vanilla', 'Tonka Bean', 'Musk', 'Benzoin', 'Sandalwood'], 550.0, 100, 'Eau de Parfum'),
    ('LL-046', 'Dior', 'J’adore', ['adore'], ['women', '100ml'], 'floral', ['Floral & Rose', 'Grand Floral'], ['Ylang-Ylang', 'Damascus Rose', 'Jasmine Sambac', 'Grasse Tuberose', 'Pear', 'Melon', 'Magnolia', 'Peach', 'Mandarin', 'Plum', 'Orchid', 'Vanilla', 'Blackberry', 'Cedar', 'Musk'], 550.0, 100, 'Eau de Parfum'),
    ('LL-047', 'Gucci', 'Bloom', ['gucci', 'bloom'], ['100ml'], 'floral', ['Floral & Rose', 'White Floral'], ['Rangoon Creeper', 'Jasmine Bud', 'Natural Tuberose'], 329.0, 100, 'Eau de Parfum'),
    ('LL-048', 'Gucci', 'Flora Gorgeous Gardenia', ['gorgeous gardenia'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Floral'], ['Pear Blossom', 'White Gardenia', 'Jasmine', 'Red Berries', 'Italian Mandarin', 'Brown Sugar', 'Patchouli'], 399.0, 100, 'Eau de Parfum'),
    ('LL-049', 'Gucci', 'Flora Gorgeous Jasmine', ['gorgeous jasmine'], ['100ml'], 'floral', ['Floral & Rose', 'Bright Floral'], ['Grandiflorum Jasmine', 'Italian Mandarin', 'Bergamot', 'Damask Rose', 'Magnolia', 'Sandalwood', 'Benzoin', 'Patchouli'], 415.0, 100, 'Eau de Parfum'),
    ('LL-050', 'Gucci', 'Flora Gorgeous Orchid', ['gorgeous orchid'], ['100ml'], 'floral', ['Floral & Rose', 'Solar Floral'], ['Vanilla Orchid', 'Ozone Accord', 'Vanilla Absolute'], 429.0, 100, 'Eau de Parfum Intense'),
    ('LL-051', 'Giorgio Armani', 'My Way', ['my way'], ['90ml', 'edp'], 'floral', ['Floral & Rose', 'White Floral'], ['Orange Blossom', 'Bergamot', 'Tuberose', 'Indian Jasmine', 'Madagascar Vanilla', 'White Musk', 'Virginian Cedar'], 420.0, 90, 'Eau de Parfum'),
    ('LL-052', 'Giorgio Armani', 'My Way Intense', ['my way', 'intense'], ['90ml'], 'floral', ['Floral & Rose', 'Woody Floral'], ['Orange Blossom', 'Bitter Orange', 'Indian Tuberose', 'Tuberose', 'Madagascar Vanilla', 'Sandalwood'], 460.0, 90, 'Eau de Parfum'),
    ('LL-053', 'Giorgio Armani', 'Sì Passione', ['si passione'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Floral'], ['Blackcurrant', 'Pear', 'Pink Pepper', 'Grapefruit', 'Pineapple', 'Rose', 'Jasmine', 'Heliotrope', 'Vanilla', 'Cedarwood', 'Amberwood'], 440.0, 100, 'Eau de Parfum'),
    ('LL-054', 'Giorgio Armani', 'Sì Nude Bloom', ['si nude bloom'], ['100ml'], 'floral', ['Floral & Rose', 'Soft Rose Floral'], ['Neroli', 'Rose de Mai', 'White Musk', 'Patchouli', 'Freesia'], 449.0, 100, 'Eau de Parfum'),
    ('LL-055', 'Parfums de Marly', 'Delina', ['delina'], ['75ml'], 'floral', ['Floral & Rose', 'Turkish Rose Floral'], ['Turkish Rose', 'Lychee', 'Rhubarb', 'Bergamot', 'Nutmeg', 'Peony', 'Petalia', 'Vanilla', 'Musk', 'Cashmeran', 'Haitian Vetiver', 'Cedar'], 890.0, 75, 'Eau de Parfum'),
    ('LL-056', 'Parfums de Marly', 'Delina Exclusif', ['delina exclusif'], ['75ml'], 'floral', ['Floral & Rose', 'Amber Rose'], ['Turkish Rose', 'Pear', 'Lychee', 'Bergamot', 'Oud', 'Incense', 'Amber', 'Vanilla', 'Woody Notes'], 960.0, 75, 'Parfum'),
    ('LL-057', 'Yves Saint Laurent', 'Mon Paris', ['mon paris'], ['women', '90'], 'floral', ['Floral & Rose', 'Chypre Fruity Floral'], ['Strawberry', 'Raspberry', 'Pear', 'Calabrian Bergamot', 'Datura Flower', 'Peony', 'Orange Blossom', 'Jasmine Sambac', 'White Musk', 'Patchouli', 'Cedar'], 440.0, 90, 'Eau de Parfum'),
    ('LL-058', 'Chloé', 'Chloé Eau de Parfum', ['chloe', 'edp'], ['75ml'], 'floral', ['Floral & Rose', 'Rose Floral'], ['Peony', 'Lychee', 'Freesia', 'Rose', 'Lily-of-the-Valley', 'Magnolia', 'Virginia Cedar', 'Amber'], 360.0, 75, 'Eau de Parfum'),
    ('LL-059', 'Lancôme', 'Idôle Nectar', ['idole', 'nectar'], ['100ml'], 'floral', ['Floral & Rose', 'Gourmand Rose'], ['Rose Soufflé', 'Ispahan Rose', 'Centifolia Rose', 'Popcorn Accord', 'Caramel', 'Bourbon Vanilla'], 410.0, 100, 'Eau de Parfum'),
    ('LL-060', 'Lancôme', 'Trésor Midnight Rose', ['tresor', 'midnight rose'], ['75ml'], 'floral', ['Floral & Rose', 'Berry Rose'], ['Raspberry', 'Blackcurrant', 'Rose', 'Peony', 'Jasmine', 'Pink Pepper', 'Vanilla', 'Cedar', 'Musk'], 380.0, 75, 'Eau de Parfum'),
    ('LL-061', 'Givenchy', 'L’Interdit', ['interdit', 'edp'], ['80ml'], 'floral', ['Floral & Rose', 'White Floral'], ['Orange Blossom', 'Jasmine Sambac', 'Tuberose', 'Patchouli', 'Vetiver', 'Ambroxan', 'Vanilla'], 415.0, 80, 'Eau de Parfum'),
    ('LL-062', 'Givenchy', 'Irresistible', ['irresistible'], ['80ml'], 'floral', ['Floral & Rose', 'Fruity Rose'], ['Sparkling Pear', 'Ambrette', 'Rose Essential', 'Iris', 'Virginia Cedar', 'Musk'], 385.0, 80, 'Eau de Parfum'),
    ('LL-063', 'Versace', 'Bright Crystal Absolu', ['bright crystal absolu'], ['90ml'], 'floral', ['Floral & Rose', 'Intense Fruity Floral'], ['Pomegranate', 'Yuzu', 'Water Notes', 'Peony', 'Raspberry', 'Lotus', 'Magnolia', 'Musk', 'Mahogany', 'Amber'], 345.0, 90, 'Eau de Parfum'),
    ('LL-064', 'Versace', 'Dylan Purple', ['dylan purple'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Floral'], ['Bitter Orange', 'Pear Juice', 'Bergamot', 'Purple Freesia', 'Pomarose', 'Mahonial', 'Iso E Super', 'Ambroxan', 'Belambre', 'Cedarwood'], 340.0, 100, 'Eau de Parfum'),
    ('LL-065', 'Elie Saab', 'Le Parfum', ['elie saab', 'le parfum'], ['90ml'], 'floral', ['Floral & Rose', 'Orange Blossom Floral'], ['African Orange Flower', 'Jasmine', 'Grandiflorum Jasmine', 'Patchouli', 'Virginia Cedar', 'Rose', 'White Honey'], 149.0, 90, 'Eau de Parfum'),
    ('LL-066', 'Elie Saab', 'Girl of Now Rose Petal', ['girl of now', 'rose petal'], ['90ml'], 'floral', ['Floral & Rose', 'Pastel Rose Floral'], ['Mandarin Orange', 'Pink Peach', 'Rose', 'Magnolia', 'Almond', 'Cedarwood'], 249.0, 90, 'Eau de Parfum'),
    ('LL-067', 'Guerlain', 'Idylle', ['idylle'], ['75ml'], 'floral', ['Floral & Rose', 'Romantic Floral'], ['Lily-of-the-Valley', 'Peony', 'Freesia', 'Lilac', 'Bulgarian Rose', 'Jasmine', 'Patchouli', 'White Musk'], 340.0, 75, 'Eau de Parfum'),
    ('LL-068', 'Guerlain', 'Insolence', ['insolence'], ['75ml'], 'floral', ['Floral & Rose', 'Powdery Violet'], ['Violet', 'Red Berries', 'Iris', 'Orange Blossom', 'Tonka Bean', 'Sandalwood', 'Woody Notes'], 360.0, 75, 'Eau de Parfum'),
    ('LL-069', 'Bvlgari', 'Rose Goldea', ['goldea', 'rose'], ['90ml'], 'floral', ['Floral & Rose', 'Rose Musky'], ['Pomegranate', 'Rose Petals', 'Musk', 'Damask Rose', 'Grandiflorum Jasmine', 'Sandalwood', 'White Incense'], 410.0, 90, 'Eau de Parfum'),

    # --- AMBER & ORIENTAL (18 items) ---
    ('LL-070', 'Yves Saint Laurent', 'Libre', ['libre', 'edp'], ['90ml'], 'oriental', ['Amber & Oriental', 'Amber Floral'], ['Lavender', 'Mandarin Orange', 'Blackcurrant', 'Petitgrain', 'Orange Blossom', 'Jasmine', 'Madagascar Vanilla', 'Musk', 'Cedar', 'Ambergris'], 395.0, 90, 'Eau de Parfum'),
    ('LL-071', 'Yves Saint Laurent', 'Libre Le Parfum', ['libre', 'parfum'], ['90ml'], 'oriental', ['Amber & Oriental', 'Warm Amber Floral'], ['Saffron', 'Ginger', 'Mandarin Orange', 'Bergamot', 'Orange Blossom', 'Lavender', 'Bourbon Vanilla', 'Honey', 'Tonka Bean', 'Vetiver'], 449.0, 90, 'Parfum'),
    ('LL-072', 'Yves Saint Laurent', 'Black Opium', ['black opium'], ['90ml'], 'oriental', ['Amber & Oriental', 'Gourmand Coffee Amber'], ['Pear', 'Pink Pepper', 'Orange Blossom', 'Coffee', 'Jasmine', 'Bitter Almond', 'Licorice', 'Vanilla', 'Patchouli', 'Cashmere Wood', 'Cedar'], 420.0, 90, 'Eau de Parfum'),
    ('LL-073', 'Carolina Herrera', 'Good Girl', ['good girl'], ['80ml'], 'oriental', ['Amber & Oriental', 'Amber Floral Gourmand'], ['Almond', 'Coffee', 'Bergamot', 'Lemon', 'Tuberose', 'Jasmine Sambac', 'Orange Blossom', 'Orris', 'Bulgarian Rose', 'Tonka Bean', 'Cacao', 'Vanilla', 'Praline', 'Sandalwood', 'Musk', 'Amber', 'Cashmere Wood', 'Cinnamon', 'Patchouli', 'Cedar'], 440.0, 80, 'Eau de Parfum'),
    ('LL-074', 'Carolina Herrera', 'Good Girl Blush', ['good girl blush'], ['80ml'], 'oriental', ['Amber & Oriental', 'Powdery Amber Floral'], ['Bergamot', 'Bitter Almond', 'Peony', 'Ylang-Ylang', 'Vanilla', 'Tonka Bean'], 469.0, 80, 'Eau de Parfum'),
    ('LL-075', 'Dior', 'Pure Poison', ['pure poison'], ['100ml'], 'oriental', ['Amber & Oriental', 'Luminous White Amber'], ['Jasmine', 'Orange', 'Bergamot', 'Sicilian Mandarin', 'Gardenia', 'Orange Blossom', 'Sandalwood', 'White Amber', 'Cedar', 'White Musk'], 490.0, 100, 'Eau de Parfum'),
    ('LL-076', 'Lancôme', 'La Vie Est Belle', ['la vie est belle'], ['100ml'], 'oriental', ['Amber & Oriental', 'Gourmand Iris'], ['Blackcurrant', 'Pear', 'Iris', 'Jasmine', 'Orange Blossom', 'Praline', 'Vanilla', 'Patchouli', 'Tonka Bean'], 420.0, 100, 'Eau de Parfum'),
    ('LL-077', 'Lancôme', 'La Vie Est Belle Elixir', ['la vie est belle', 'elixir'], ['100ml'], 'oriental', ['Amber & Oriental', 'Rich Fruity Amber'], ['Raspberry', 'Liquor Accord', 'Calabrian Bergamot', 'Violet Leaf', 'Rose', 'Leather', 'Cocoa Butter', 'Cedarwood'], 460.0, 100, 'Eau de Parfum'),
    ('LL-078', 'Jean Paul Gaultier', 'Scandal', ['scandal'], ['80ml'], 'oriental', ['Amber & Oriental', 'Honey Floral'], ['Blood Orange', 'Mandarin Orange', 'Honey', 'Gardenia', 'Orange Blossom', 'Jasmine', 'Peach', 'Beeswax', 'Caramel', 'Patchouli', 'Licorice'], 425.0, 80, 'Eau de Parfum'),
    ('LL-079', 'Jean Paul Gaultier', 'La Belle', ['la belle'], ['100ml'], 'oriental', ['Amber & Oriental', 'Amber Vanilla'], ['Green Pear', 'Bergamot', 'Vanilla Pod', 'Leather', 'Amber', 'Vetiver', 'Musk'], 415.0, 100, 'Eau de Parfum'),
    ('LL-080', 'Viktor & Rolf', 'Flowerbomb', ['flowerbomb'], ['100ml'], 'oriental', ['Amber & Oriental', 'Amber Floral Gourmand'], ['Tea', 'Bergamot', 'Osmanthus', 'Orchid', 'Jasmine', 'Rose', 'Freesia', 'African Orange Flower', 'Patchouli', 'Musk', 'Vanilla'], 440.0, 100, 'Eau de Parfum'),
    ('LL-081', 'Elie Saab', 'Girl of Now', ['girl of now'], ['90ml'], 'oriental', ['Amber & Oriental', 'Gourmand Almond Amber'], ['Pistachio', 'Pear', 'Mandarin Orange', 'Almond', 'Orange Blossom', 'Magnolia', 'Almond Milk', 'Tonka Bean', 'Patchouli', 'Cashmeran'], 330.0, 90, 'Eau de Parfum'),
    ('LL-082', 'Prada', 'Paradoxe', ['paradoxe'], ['90ml'], 'oriental', ['Amber & Oriental', 'Amber Floral'], ['Pear', 'Tangerine', 'Calabrian Bergamot', 'Orange Blossom', 'Neroli Essence', 'Jasmine Sambac', 'Bourbon Vanilla', 'White Musk', 'Amber', 'Benzoin'], 460.0, 90, 'Eau de Parfum'),
    ('LL-083', 'Prada', 'Paradoxe Intense', ['paradoxe intense'], ['90ml'], 'oriental', ['Amber & Oriental', 'Warm Amber Floral'], ['Pear', 'Neroli', 'Bergamot', 'Moss', 'Jasmine', 'Bourbon Vanilla', 'Ambrofix', 'Amber', 'Serenolide'], 499.0, 90, 'Eau de Parfum'),
    ('LL-084', 'Burberry', 'Burberry Goddess', ['burberry goddess'], ['5ml', '100ml'], 'oriental', ['Amber & Oriental', 'Aromatic Gourmand Vanilla'], ['Vanilla Infusion', 'Lavender', 'Vanilla Caviar', 'Vanilla Absolute'], 440.0, 100, 'Eau de Parfum'),
    ('LL-085', 'Paco Rabanne', 'Olympéa', ['olympea'], ['80ml'], 'oriental', ['Amber & Oriental', 'Salty Vanilla Amber'], ['Water Jasmine', 'Green Mandarin', 'Ginger Lily', 'Salted Vanilla', 'Cashmere Wood', 'Ambergris', 'Sandalwood'], 340.0, 80, 'Eau de Parfum'),
    ('LL-086', 'Ariana Grande', 'Mod Vanilla', ['mod vanilla'], ['100ml'], 'oriental', ['Amber & Oriental', 'Gourmand Vanilla Musky'], ['Pink Freesia', 'Juicy Plum', 'Musk', 'Orris', 'Praline', 'Vanilla Absolute', 'Cocoa Butter'], 239.0, 100, 'Eau de Parfum'),
    ('LL-087', 'Lattafa', 'Yara', ['yara'], ['100ml'], 'oriental', ['Amber & Oriental', 'Tropical Gourmand'], ['Heliotrope', 'Orchid', 'Tangerine', 'Gourmand Accord', 'Tropical Fruits', 'Vanilla', 'Sandalwood', 'Musk'], 69.0, 100, 'Eau de Parfum'),

    # --- WOODY & EARTHY (13 items) ---
    ('LL-088', 'Narciso Rodriguez', 'For Her', ['for her', 'edp'], ['100ml'], 'woody', ['Woody & Earthy', 'Floral Woody Musk'], ['Rose', 'Peach', 'Musk', 'Amber', 'Patchouli', 'Sandalwood'], 345.0, 100, 'Eau de Parfum'),
    ('LL-089', 'Narciso Rodriguez', 'Pure Musc', ['pure musc', 'her'], ['100ml'], 'woody', ['Woody & Earthy', 'Musky Floral Woody'], ['Jasmine', 'Orange Blossom', 'Musk Heart', 'Cashmeran', 'Amber', 'Patchouli'], 360.0, 100, 'Eau de Parfum'),
    ('LL-090', 'Tom Ford', 'Black Orchid', ['black orchid'], ['100ml'], 'woody', ['Woody & Earthy', 'Dark Woody Amber'], ['Truffle', 'Gardenia', 'Blackcurrant', 'Ylang-Ylang', 'Jasmine', 'Bergamot', 'Mandarin', 'Orchid', 'Spices', 'Patchouli', 'Sandalwood', 'Incense', 'Amber', 'Vetiver', 'Vanilla', 'Dark Chocolate'], 650.0, 100, 'Eau de Parfum'),
    ('LL-091', 'Versace', 'Crystal Noir', ['crystal noir'], ['90ml'], 'woody', ['Woody & Earthy', 'Amber Woody Spiced'], ['Pepper', 'Ginger', 'Cardamom', 'Coconut', 'Gardenia', 'Orange Blossom', 'Peony', 'Sandalwood', 'Musk', 'Amber'], 340.0, 90, 'Eau de Parfum'),
    ('LL-092', 'Hermès', 'Eau des Merveilles', ['merveilles'], ['100ml'], 'woody', ['Woody & Earthy', 'Woody Amber Mineral'], ['Orange', 'Elemi Resin', 'Lemon', 'Amber', 'Pepper', 'Pink Pepper', 'Violet', 'Fir', 'Cedar', 'Madagascar Vetiver', 'Oakmoss'], 460.0, 100, 'Eau de Toilette'),
    ('LL-093', 'Hermès', 'Kelly Calèche', ['kelly caleche'], ['100ml'], 'woody', ['Woody & Earthy', 'Floral Leather Woody'], ['Grapefruit', 'Narcissus', 'Lily-of-the-Valley', 'Iris', 'Rose', 'Mimosa', 'Tuberose', 'Tuscan Leather'], 480.0, 100, 'Eau de Parfum'),
    ('LL-094', 'Givenchy', 'L’Interdit Rouge', ['interdit', 'rouge'], ['80ml'], 'woody', ['Woody & Earthy', 'Spicy Woody Floral'], ['Blood Orange', 'Ginger', 'Pimento Leaf', 'Tuberose', 'Jasmine', 'Sandalwood', 'Patchouli', 'Vetiver'], 425.0, 80, 'Eau de Parfum'),
    ('LL-095', 'Gucci', 'Gucci Guilty Pour Femme', ['gucci guilty', 'femme'], ['90ml'], 'woody', ['Woody & Earthy', 'Amber Floral Woody'], ['Pink Pepper', 'Mandora', 'Bergamot', 'Lilac', 'Violet', 'Geranium', 'Rose', 'Patchouli', 'Amber'], 390.0, 90, 'Eau de Parfum'),
    ('LL-096', 'Calvin Klein', 'Euphoria', ['euphoria'], ['100ml'], 'woody', ['Woody & Earthy', 'Woody Amber Fruity'], ['Pomegranate', 'Persimmon', 'Green Accord', 'Black Orchid', 'Lotus', 'Champaca', 'Mahogany Wood', 'Amber', 'Black Violet', 'Whipped Cream'], 240.0, 100, 'Eau de Parfum'),
    ('LL-097', 'Cartier', 'La Panthère', ['panthere'], ['75ml'], 'woody', ['Woody & Earthy', 'Chypre Floral Mossy'], ['Dried Fruits', 'Rhubarb', 'Strawberries', 'Bergamot', 'Gardenia', 'Rose', 'Ylang-Ylang', 'Orange Blossom', 'Pear', 'Oakmoss', 'Musk', 'Leather', 'Patchouli'], 420.0, 75, 'Eau de Parfum'),
    ('LL-098', 'Lalique', 'Perles de Lalique', ['perles de lalique'], ['100ml'], 'woody', ['Woody & Earthy', 'Chypre Woody Rose'], ['Bulgarian Rose', 'Pepper', 'Bourbon Iris', 'Patchouli', 'Oakmoss', 'Vetiver', 'Cashmere Wood'], 169.0, 100, 'Eau de Parfum'),
    ('LL-099', 'Burberry', 'Her Elixir', ['her', 'elixir'], ['100ml'], 'woody', ['Woody & Earthy', 'Woody Gourmand Fruity'], ['Strawberry', 'Blackberry', 'Jasmine', 'Vanilla', 'Amber', 'Sandalwood'], 430.0, 100, 'Eau de Parfum Intense'),
    ('LL-100', 'Guerlain', 'Mon Guerlain', ['guerlain', 'mon'], ['eau', 'women'], 'woody', ['Woody & Earthy', 'Aromatic Woody Amber'], ['Carla Lavender', 'Bergamot', 'Sambac Jasmine', 'Iris', 'Rose', 'Tahitensis Vanilla', 'Australian Sandalwood', 'Coumarin', 'Benzoin', 'Licorice', 'Patchouli'], 460.0, 100, 'Eau de Parfum')
]

def slugify(text):
    text = text.lower().replace('&', 'and')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

new_products_list = []
row_idx = 28
used_slugs = set(p['slug'] for p in original_25)

for (sku, brand, name, req_tok, pref_tok, category, families, notes, def_price, def_size, def_conc) in NEW_75_WOMENS:
    best_lp = find_leperfume_product(req_tok, pref_tok)
    
    if best_lp:
        lp_title = best_lp['title']
        lp_price = float(best_lp['variants'][0]['price']) if best_lp.get('variants') else def_price
        img_src = best_lp['images'][0]['src'] if best_lp.get('images') else None
    else:
        print(f"Notice: No lp match for {sku} ({brand} {name}), using defaults")
        lp_title = f"{brand} {name} {def_size}ml"
        lp_price = def_price
        img_src = None

    base_slug = slugify(f"{brand} {name}")
    slug = base_slug
    if slug in used_slugs:
        slug = f"{base_slug}-{slugify(def_conc)}"
    if slug in used_slugs:
        slug = f"{slug}-{def_size}ml"
    used_slugs.add(slug)

    local_img_file = os.path.join(PUBLIC_PRODUCTS_DIR, f"{slug}.webp")
    web_img_path = f"/assets/products/{slug}.webp"

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
            print(f"[{sku}] Downloaded image: {slug}.webp")
        except Exception as e:
            print(f"[{sku}] Image fetch error for {img_src}: {e}")
    elif os.path.exists(local_img_file):
        # Image exists
        pass
    else:
        print(f"[{sku}] Warning: No image found for {slug}")

    price = lp_price if lp_price and lp_price > 0 else def_price
    price_minor = int(price * 100)
    price_display = f"{int(price)} QAR"

    short_notes_preview = ", ".join(notes[:4])
    description = (
        f"An iconic fragrance masterpiece by {brand}. {name} unfolds with exquisite accords of "
        f"{short_notes_preview}, embodying timeless luxury, elegance, and distinction."
    )

    product_obj = {
        "id": f"lum_{str(row_idx).zfill(3)}",
        "row": row_idx,
        "sku": sku,
        "slug": slug,
        "brand": brand,
        "name": name,
        "fullName": f"{brand} {name}",
        "sizeMl": def_size,
        "sizeDisplay": f"{def_size}ml",
        "concentration": def_conc,
        "currency": "QAR",
        "priceMinor": price_minor,
        "priceDisplay": price_display,
        "stickerPriceMinor": None,
        "image": web_img_path,
        "category": category,
        "scentFamilies": families,
        "keyNotes": notes,
        "rawNotes": ", ".join(notes),
        "description": description,
        "isDraft": False,
        "draftReason": [],
        "featured": sku in ['LL-026', 'LL-044', 'LL-045', 'LL-048', 'LL-055', 'LL-070', 'LL-073', 'LL-084', 'LL-090']
    }
    new_products_list.append(product_obj)
    row_idx += 1

print(f"\nGenerated {len(new_products_list)} new women's products!")

# Combine original 25 + new 75 = 100
final_100 = original_25 + new_products_list
print(f"Total unified catalog count: {len(final_100)}")

# Verify category distribution
from collections import Counter
cat_counts = Counter(p['category'] for p in final_100)
print(f"Category breakdown: {dict(cat_counts)}")

with open(EXISTING_PRODUCTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(final_100, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {len(final_100)} products to {EXISTING_PRODUCTS_JSON}!")
