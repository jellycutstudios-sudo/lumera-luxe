import json
import os
import re
import urllib.request
from PIL import Image
import io

LEPERFUME_CATALOG = '/Users/LUMÈRA_LUXE/private-source/leperfumeqa_catalog.json'
PRODUCTS_JSON = '/Users/LUMÈRA_LUXE/src/data/products.json'
PUBLIC_PRODUCTS_DIR = '/Users/LUMÈRA_LUXE/public/assets/products'

os.makedirs(PUBLIC_PRODUCTS_DIR, exist_ok=True)

with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
    existing_100 = json.load(f)

print(f"Loaded existing products: {len(existing_100)}")

with open(LEPERFUME_CATALOG, 'r', encoding='utf-8') as f:
    lp_products = json.load(f)

print(f"Loaded LePerfume catalog: {len(lp_products)}")

def is_men_title(t):
    t_clean = re.sub(r'women|femme|donna|pour elle', '', t.lower())
    if re.search(r'\b(men|homme|uomo|boy|male)\b', t_clean):
        return True
    if '(m)' in t.lower() or ' (m)' in t.lower() or '(m) ' in t.lower():
        return True
    return False

def find_lp(req_tokens, pref_tokens=[]):
    candidates = []
    for item in lp_products:
        t = item['title'].lower()
        if not item.get('images'): continue
        if is_men_title(t): continue
        if all(r in t for r in req_tokens):
            score = sum(3 for pr in pref_tokens if pr in t)
            candidates.append((score, item))
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    return None

def slugify(text):
    text = text.lower().replace('&', 'and')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

# 100 NEW CURATED LUXURY WOMEN'S PERFUMES (LL-101 to LL-200)
# (sku, brand, name, req_tokens, pref_tokens, category, scent_families, key_notes, default_price, size_ml, concentration)
NEW_100_ITEMS = [
    # --- FRESH & CITRUS (24 items) ---
    ('LL-101', 'Lanvin', 'Éclat d’Arpège', ['lanvin', 'eclat'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Fresh Green Floral'], ['Green Lilac', 'Tea Leaf', 'Peach Blossom', 'Peony', 'Petitgrain', 'Osmanthus', 'Cedar', 'Musk', 'Amber'], 149.0, 100, 'Eau de Parfum'),
    ('LL-102', 'Versace', 'Versense', ['versense'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Woody Citrus'], ['Bergamot', 'Green Mandarin', 'Fig', 'Sea Lily', 'Jasmine', 'Cardamom', 'Cedar', 'Sandalwood', 'Olive Tree', 'Musk'], 210.0, 100, 'Eau de Toilette'),
    ('LL-103', 'Dolce & Gabbana', 'Dolce Lily', ['dolce', 'lily'], ['75ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral Fresh'], ['Passionfruit', 'Bergamot', 'Lemon', 'Lily', 'Rose', 'Musk', 'Sandalwood', 'Vanilla'], 179.0, 75, 'Eau de Toilette'),
    ('LL-104', 'Salvatore Ferragamo', 'Incanto Charms', ['incanto', 'charms'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Floral Fruity Fresh'], ['Honeysuckle', 'Passionfruit', 'Rose', 'Jasmine', 'Woody Notes', 'Musk'], 99.0, 100, 'Eau de Toilette'),
    ('LL-105', 'Salvatore Ferragamo', 'Incanto Shine', ['incanto', 'shine'], ['50ml', '100ml'], 'fresh', ['Fresh & Citrus', 'Fruity Fresh'], ['Pineapple', 'Passionfruit', 'Bergamot', 'Peach', 'Pink Peony', 'Freesia', 'Cedar', 'Amber', 'Musk'], 69.0, 50, 'Eau de Toilette'),
    ('LL-106', 'Elizabeth Arden', 'Green Tea Summer', ['green tea', 'summer'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Citrus Aromatic'], ['Bergamot', 'Tangerine', 'Blackcurrant', 'Lemon', 'Watermelon', 'Green Tea', 'Lotus', 'Cyclamen', 'Oakmoss', 'Musk', 'Amber'], 59.0, 100, 'Eau de Toilette'),
    ('LL-107', 'Elizabeth Arden', 'White Tea', ['white tea', 'w'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Woody Floral Fresh'], ['Sea Notes', 'Fern', 'Mandarin Orange', 'Clary Sage', 'White Tea', 'White Iris', 'Mate', 'Exotic Woods', 'Ambrette', 'Tonka Bean', 'Amber'], 140.0, 100, 'Eau de Toilette'),
    ('LL-108', 'Escada', 'Brisa Cubana', ['brisa cubana'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Tropical Citrus'], ['Lime Accord', 'Mojito Accord', 'Mariposa Lily', 'Mint', 'Solar Notes'], 145.0, 100, 'Eau de Toilette'),
    ('LL-109', 'Escada', 'Santorini Sunrise', ['santorini'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Citrus Fruity'], ['Mandarin Sorbet', 'Bergamot', 'Jasmine Petals', 'Pink Pepper', 'Solar Accord'], 155.0, 100, 'Eau de Toilette'),
    ('LL-110', 'Moschino', 'I Love Love', ['love love'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Citrus Floral'], ['Grapefruit', 'Orange', 'Lemon', 'Red Currant', 'Sugar Cane', 'Bulrush', 'Lily-of-the-Valley', 'Tea Rose', 'Cinnamon', 'Cedar', 'Musk', 'Tanaka Wood'], 169.0, 100, 'Eau de Toilette'),
    ('LL-111', 'Moschino', 'Fresh Couture', ['fresh couture'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Floral Fruity Fresh'], ['Bergamot', 'Mandarin Orange', 'Ylang-Ylang', 'Peony', 'Raspberry', 'Osmanthus', 'Woody Notes', 'White Patchouli', 'Ambroxan'], 180.0, 100, 'Eau de Toilette'),
    ('LL-112', 'Roberto Cavalli', 'Paradiso', ['paradiso', 'rosa'], ['75ml'], 'fresh', ['Fresh & Citrus', 'Citrus Floral Woody'], ['Citrus', 'Mandarin Orange', 'Bergamot', 'Jasmine', 'Pine Tree', 'Cypress', 'Laurel'], 129.0, 75, 'Eau de Parfum'),
    ('LL-113', 'Coach', 'Coach Dreams', ['coach dreams'], ['90ml', 'set'], 'fresh', ['Fresh & Citrus', 'Fruity Floral Fresh'], ['Bitter Orange', 'Pear', 'Gardenia', 'Cactus Flower', 'Joshua Tree', 'Ambroxan'], 270.0, 90, 'Eau de Parfum'),
    ('LL-114', 'Guess', 'Bella Vita Paradiso', ['bella vita', 'paradiso'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Floral Amber Fresh'], ['Italian Mandarin', 'Pear Blossom', 'Red Berries', 'Jasmine', 'Gardenia', 'Tuberose', 'Patchouli', 'Amber', 'Musk'], 149.0, 100, 'Eau de Parfum'),
    ('LL-115', 'Issey Miyake', 'L’Eau d’Issey Pure', ['issey miyake', 'pure'], ['90ml'], 'fresh', ['Fresh & Citrus', 'Aquatic Floral'], ['Sea Notes', 'Orange Blossom', 'Damask Rose', 'Jasmine', 'Lily', 'Ambergris', 'Cashmeran'], 240.0, 90, 'Eau de Parfum'),
    ('LL-116', 'Calvin Klein', 'CK IN2U for Her', ['in2u', 'her'], ['100ml', '150ml'], 'fresh', ['Fresh & Citrus', 'Citrus Fresh'], ['Pink Grapefruit', 'Sicilian Bergamot', 'Red Currant Leaf', 'Cactus', 'Orchid', 'Vanilla', 'Red Cedar', 'Amber'], 110.0, 100, 'Eau de Toilette'),
    ('LL-117', 'Marc Jacobs', 'Daisy Eau So Fresh', ['daisy', 'fresh'], ['125ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral Fresh'], ['Raspberry', 'Pear', 'Grapefruit', 'Green Notes', 'Violet', 'Litchi', 'Apple Blossom', 'Rose', 'Jasmine', 'Musk', 'Plum', 'Virginia Cedar'], 360.0, 125, 'Eau de Toilette'),
    ('LL-118', 'Burberry', 'Brit Sheer', ['brit sheer'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral Fresh'], ['Litchi', 'Yuzu', 'Pineapple Leaf', 'Mandarin Orange', 'Peony', 'Peach Blossom', 'Pear', 'White Musk', 'White Wood'], 215.0, 100, 'Eau de Toilette'),
    ('LL-119', 'Guerlain', 'Aqua Allegoria Mandarine Basilic', ['mandarine basilic'], ['125ml', '75ml'], 'fresh', ['Fresh & Citrus', 'Citrus Aromatic'], ['Clementine', 'Bitter Orange', 'Orange Blossom', 'Green Tea', 'Ivy', 'Mandarin Orange', 'Basil', 'Chamomile', 'Peony', 'Sandalwood', 'Amber'], 320.0, 125, 'Eau de Toilette'),
    ('LL-120', 'Hermès', 'Un Jardin Sur Le Nil', ['jardin sur le nil'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Fruity Green Fresh'], ['Green Mango', 'Grapefruit', 'Tomato', 'Carrot', 'Lotus', 'Cattail', 'Orange', 'Peony', 'Hyacinth', 'Musk', 'Iris', 'Incense', 'Labdanum', 'Cinnamon'], 430.0, 100, 'Eau de Toilette'),
    ('LL-121', 'Kenzo', 'L’Eau Kenzo Pour Femme', ['eau kenzo', 'femme'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Aquatic Floral'], ['Reed', 'Mint', 'Green Lilac', 'Mandarin Orange', 'Pink Pepper', 'Water Lily', 'Pepper', 'White Peach', 'Amaryllis', 'Rose', 'Cedar', 'White Musk', 'Vanilla'], 195.0, 100, 'Eau de Toilette'),
    ('LL-122', 'Chanel', 'Chance Eau Fraîche', ['chance', 'fraiche'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Chypre Floral Fresh'], ['Lemon', 'Cedar', 'Citron', 'Water Hyacinth', 'Pink Pepper', 'Jasmine', 'White Musk', 'Patchouli', 'Vetiver', 'Teak Wood', 'Iris', 'Amber'], 590.0, 100, 'Eau de Toilette'),
    ('LL-123', 'Afnan', 'Souvenir Blooming Bliss', ['souvenir', 'blooming'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral'], ['Bergamot', 'Litchi', 'Red Fruits', 'Rose', 'Vanilla', 'Cedarwood', 'Musk'], 140.0, 100, 'Eau de Parfum'),
    ('LL-124', 'Guess', '1981 Los Angeles', ['guess 1981', 'angeles', 'w'], ['100ml'], 'fresh', ['Fresh & Citrus', 'Fruity Floral Fresh'], ['Red Currant', 'Mandarin Orange', 'Pear', 'Jasmine', 'Peony', 'Orange Blossom', 'Lily-of-the-Valley', 'Ambroxan', 'Praline', 'Musk', 'Cedar'], 89.0, 100, 'Eau de Toilette'),

    # --- FLORAL & ROSE (35 items) ---
    ('LL-125', 'Lanvin', 'Marry Me', ['lanvin', 'marry me'], ['75ml'], 'floral', ['Floral & Rose', 'Romantic Floral'], ['Bitter Orange', 'Peach', 'Freesia', 'Jasmine', 'Magnolia', 'Rose', 'Musk', 'Virginia Cedar', 'Amber'], 139.0, 75, 'Eau de Parfum'),
    ('LL-126', 'Dolce & Gabbana', 'Dolce Violet', ['dolce', 'violet'], ['75ml'], 'floral', ['Floral & Rose', 'Floral Fruity Violet'], ['Cassis', 'Cyclamen', 'Mandarin Orange', 'Violet', 'Blackberry', 'Pear', 'Musk', 'Madagascar Vanilla', 'Sandalwood'], 199.0, 75, 'Eau de Toilette'),
    ('LL-127', 'Dolce & Gabbana', 'Dolce Blue Jasmine', ['blue jasmine'], ['75ml'], 'floral', ['Floral & Rose', 'Solar Floral'], ['Sicilian Fig', 'Blue Jasmine Sambac', 'Cedarwood'], 215.0, 75, 'Eau de Parfum'),
    ('LL-128', 'Paco Rabanne', 'Olympéa Flora', ['olympea', 'flora'], ['80ml'], 'floral', ['Floral & Rose', 'Rose Floral'], ['Blackcurrant', 'Pink Pepper', 'Sorbet', 'Rose', 'Peony', 'Vanilla', 'Patchouli', 'Cashmere Wood', 'Salt'], 249.0, 80, 'Eau de Parfum Intense'),
    ('LL-129', 'Guess', 'Girl Belle', ['guess girl belle'], ['100ml'], 'floral', ['Floral & Rose', 'Floral Fruity'], ['Wild Berries', 'Champagne', 'Peony', 'Jasmine', 'Violet', 'Australian Sandalwood', 'Musk', 'Vanilla'], 69.0, 100, 'Eau de Toilette'),
    ('LL-130', 'Guess', 'Girl', ['guess girl', 'edt'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Floral'], ['Raspberry', 'Melon', 'Bergamot', 'Orchid', 'Lily', 'Robinia', 'Australian Sandalwood', 'Madagascar Vanilla'], 69.0, 100, 'Eau de Toilette'),
    ('LL-131', 'Coach', 'Coach Floral Blush', ['coach floral blush'], ['90ml'], 'floral', ['Floral & Rose', 'Airy Rose Floral'], ['Goji Berries', 'Grapefruit', 'Peony', 'Peach', 'Crystal Musk', 'White Wood'], 189.0, 90, 'Eau de Parfum'),
    ('LL-132', 'Coach', 'Coach Wild Rose', ['wild rose'], ['90ml'], 'floral', ['Floral & Rose', 'Gourmand Rose'], ['Red Currant', 'Bergamot', 'Rose', 'Jasmine Sambac', 'Ambroxan', 'Tonka Bean', 'Moss'], 220.0, 90, 'Eau de Parfum'),
    ('LL-133', 'Elizabeth Arden', '5th Avenue', ['5th avenue', 'after five'], ['125ml'], 'floral', ['Floral & Rose', 'Classic Floral'], ['Plum', 'Bergamot', 'Coriander', 'Lily-of-the-Valley', 'Lotus', 'Jasmine', 'Saffron', 'Birch', 'Tonka Bean', 'Musk'], 99.0, 125, 'Eau de Parfum'),
    ('LL-134', 'Kenzo', 'Flower by Kenzo', ['kenzo', 'flower'], ['100ml'], 'floral', ['Floral & Rose', 'Powdery Floral'], ['Bulgarian Rose', 'Hawthorn', 'Blackcurrant', 'Mandarin Orange', 'Parma Violet', 'Rose', 'Opoponax', 'Jasmine', 'Vanilla', 'White Musk', 'Incense'], 225.0, 100, 'Eau de Parfum'),
    ('LL-135', 'Issey Miyake', 'L’Eau d’Issey Rose & Rose', ['rose&rose'], ['90ml'], 'floral', ['Floral & Rose', 'Intense Rose Floral'], ['Raspberry', 'Pear', 'Pink Pepper', 'Bulgarian Rose', 'Rose', 'Osmanthus', 'Cashmeran', 'Amber', 'Patchouli'], 219.0, 90, 'Eau de Parfum Intense'),
    ('LL-136', 'Nina Ricci', 'L’Air du Temps', ['air du temps'], ['100ml'], 'floral', ['Floral & Rose', 'Spicy Carnation Floral'], ['Carnation', 'Aldehydes', 'Rose', 'Neroli', 'Brazilian Rosewood', 'Peach', 'Bergamot', 'Cloves', 'Orris Root', 'Ylang-Ylang', 'Oakmoss', 'Spices', 'Sandalwood', 'Benzoin', 'Amber', 'Cedar', 'Musk'], 189.0, 100, 'Eau de Parfum'),
    ('LL-137', 'Gucci', 'Flora Gorgeous Magnolia', ['gorgeous magnolia'], ['100ml'], 'floral', ['Floral & Rose', 'Chypre Floral'], ['Dewberry', 'Sweet Orange', 'Magnolia', 'Jasmine Sambac', 'Clary Sage', 'Patchouli', 'Musk', 'Blonde Woods'], 415.0, 100, 'Eau de Parfum'),
    ('LL-138', 'Armaf', 'Club de Nuit Woman', ['club de nuit', 'woman'], ['105ml'], 'floral', ['Floral & Rose', 'Fruity Floral Chypre'], ['Orange', 'Bergamot', 'Grapefruit', 'Peach', 'Rose', 'Jasmine', 'Geranium', 'Litchi', 'Patchouli', 'Vanilla', 'Musk', 'Vetiver'], 95.0, 105, 'Eau de Parfum'),
    ('LL-139', 'Narciso Rodriguez', 'Fleur Musc', ['fleur musc'], ['100ml'], 'floral', ['Floral & Rose', 'Rose Floral Musky'], ['Pink Pepper', 'Rose', 'Peony', 'Musk', 'Patchouli', 'Amber', 'Violet'], 349.0, 100, 'Eau de Parfum'),
    ('LL-140', 'Narciso Rodriguez', 'Narciso Ambrée', ['narciso ambree'], ['90ml'], 'floral', ['Floral & Rose', 'Warm Solar Floral'], ['Frangipani', 'Ylang-Ylang', 'White Flowers', 'Musk', 'Amber', 'Cashmeran', 'Vanilla', 'Cedar'], 329.0, 90, 'Eau de Parfum'),
    ('LL-141', 'Burberry', 'Her Blossom', ['her', 'blossom'], ['100ml'], 'floral', ['Floral & Rose', 'Airy Fruity Floral'], ['Mandarin Orange', 'Pink Pepper', 'Plum Blossom', 'Peony', 'Musk', 'Sandalwood'], 295.0, 100, 'Eau de Toilette'),
    ('LL-142', 'Chanel', 'Gabrielle', ['gabrielle'], ['100ml'], 'floral', ['Floral & Rose', 'Solar White Floral'], ['Grapefruit', 'Mandarin Orange', 'Blackcurrant', 'Orange Blossom', 'Jasmine', 'Ylang-Ylang', 'Tuberose', 'Lily-of-the-Valley', 'Pear', 'Pink Pepper', 'Musk', 'Sandalwood', 'Cashmeran', 'Orris'], 650.0, 100, 'Eau de Parfum'),
    ('LL-143', 'Dior', 'Miss Dior Blooming Bouquet', ['blooming bouquet'], ['100ml'], 'floral', ['Floral & Rose', 'Tender Rose Floral'], ['Sicilian Mandarin', 'Pink Peony', 'Damask Rose', 'Apricot', 'Peach', 'White Musk'], 490.0, 100, 'Eau de Toilette'),
    ('LL-144', 'Giorgio Armani', 'Sì Passione Éclat', ['passione', 'eclat'], ['100ml'], 'floral', ['Floral & Rose', 'Radiant Rose Floral'], ['Blackcurrant', 'Calabrian Bergamot', 'May Rose', 'Damask Rose', 'White Musk', 'Madagascar Vanilla'], 435.0, 100, 'Eau de Parfum'),
    ('LL-145', 'Givenchy', 'Irresistible Very Floral', ['irresistible', 'floral'], ['80ml'], 'floral', ['Floral & Rose', 'Solar Rose'], ['Coconut Water', 'Blackcurrant', 'Rose Essential', 'Centifolia Rose', 'Iris', 'White Flowers', 'Ylang-Ylang', 'Jasmine Sambac', 'Ambrette', 'Cedarwood'], 395.0, 80, 'Eau de Parfum'),
    ('LL-146', 'Elie Saab', 'Girl of Now Lovely', ['girl of now lovely'], ['90ml'], 'floral', ['Floral & Rose', 'Sparkling Green Floral'], ['Mint', 'Mandarin Orange', 'Pear', 'Rosemary', 'Blackcurrant Blossom', 'Almond', 'Orange Blossom', 'Frangipani', 'Anise', 'Patchouli', 'Tonka Bean', 'Ambroxan'], 235.0, 90, 'Eau de Parfum'),
    ('LL-147', 'Marc Jacobs', 'Daisy', ['marc jacobs', 'daisy'], ['100ml'], 'floral', ['Floral & Rose', 'Powdery Floral'], ['Violet Leaf', 'Blood Grapefruit', 'Wild Strawberry', 'Violet', 'Gardenia', 'Jasmine', 'Musk', 'White Woods', 'Vanilla'], 340.0, 100, 'Eau de Toilette'),
    ('LL-148', 'Marc Jacobs', 'Perfect', ['marc jacobs', 'perfect'], ['100ml'], 'floral', ['Floral & Rose', 'Comforting Floral'], ['Rhubarb', 'Narcissus', 'Almond Milk', 'Cashmeran', 'Cedar'], 395.0, 100, 'Eau de Parfum'),
    ('LL-149', 'Jimmy Choo', 'Blossom', ['jimmy choo', 'blossom'], ['100ml'], 'floral', ['Floral & Rose', 'Berry Floral'], ['Raspberry', 'Red Berries', 'Citrus', 'Sweet Pea', 'Rose', 'White Musk', 'Sandalwood'], 199.0, 100, 'Eau de Parfum'),
    ('LL-150', 'Jimmy Choo', 'Floral', ['jimmy choo', 'floral'], ['90ml'], 'floral', ['Floral & Rose', 'Radiant Floral'], ['Nectarine', 'Tangerine', 'Bergamot', 'Magnolia', 'Sweet Pea', 'Apricot Blossom', 'Musk', 'Ambroxan', 'Woody Notes'], 210.0, 90, 'Eau de Toilette'),
    ('LL-151', 'Lalique', 'Amethyst', ['lalique', 'amethyst'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Berry Floral'], ['Blackberry', 'Blackcurrant', 'Blueberry', 'Mulberry', 'Strawberry', 'Peony', 'Pepper', 'Rose', 'Ylang-Ylang', 'Musk', 'Woody Notes', 'Bourbon Vanilla'], 149.0, 100, 'Eau de Parfum'),
    ('LL-152', 'Ariana Grande', 'Ari', ['ariana', 'ari'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Floral Gourmand'], ['Raspberry', 'Pear', 'Grapefruit', 'Vanilla Orchid', 'Rose', 'Lily-of-the-Valley', 'Marshmallow', 'Musk', 'Woody Notes'], 195.0, 100, 'Eau de Parfum'),
    ('LL-153', 'Ariana Grande', 'Thank U Next', ['thank u next'], ['100ml'], 'floral', ['Floral & Rose', 'Floral Gourmand'], ['Raspberry', 'Pear', 'Coconut', 'Pink Rose', 'Macarons', 'Musk'], 215.0, 100, 'Eau de Parfum'),
    ('LL-154', 'Bvlgari', 'Omnia Amethyste', ['omnia amethyste'], ['65ml', '100ml'], 'floral', ['Floral & Rose', 'Powdery Floral'], ['Green Sap', 'Pink Grapefruit', 'Iris', 'Bulgarian Rose', 'Heliotrope', 'Solar Wood'], 295.0, 65, 'Eau de Toilette'),
    ('LL-155', 'Roberto Cavalli', 'Florence', ['roberto cavalli', 'florence'], ['75ml'], 'floral', ['Floral & Rose', 'Chypre Amber Floral'], ['Mandarin Orange', 'Blackcurrant', 'Orange Blossom', 'Grapefruit Blossom', 'Hibiscus Seed', 'Patchouli', 'Amber', 'Musk'], 169.0, 75, 'Eau de Parfum'),
    ('LL-156', 'Paco Rabanne', 'Lady Million Fabulous', ['lady million', 'fabulous'], ['80ml'], 'floral', ['Floral & Rose', 'Solar Amber Floral'], ['Mandarin Orange', 'Pink Pepper', 'Solar Notes', 'Tuberose', 'Ylang-Ylang', 'Jasmine', 'Vanilla', 'Tonka Bean', 'Moss'], 345.0, 80, 'Eau de Parfum'),
    ('LL-157', 'Valentino', 'Donna Born in Roma Coral Fantasy', ['coral fantasy'], ['100ml'], 'floral', ['Floral & Rose', 'Fruity Floral'], ['Kiwi', 'Brazilian Orange', 'Indian Jasmine', 'Rose', 'Ambrette', 'White Musk', 'Texas Cedar'], 460.0, 100, 'Eau de Parfum'),
    ('LL-158', 'Valentino', 'Donna Born in Roma Yellow Dream', ['yellow dream'], ['100ml'], 'floral', ['Floral & Rose', 'Zesty Rose Floral'], ['Italian Lemon', 'Damask Rose', 'White Musk'], 440.0, 100, 'Eau de Parfum'),
    ('LL-159', 'Guerlain', 'La Petite Robe Noire', ['petite robe noire'], ['75ml'], 'floral', ['Floral & Rose', 'Fruity Floral Amber'], ['Sour Cherry', 'Almond', 'Red Berries', 'Bergamot', 'Licorice', 'Rose', 'Taif Rose', 'Tea', 'Vanilla', 'Anise', 'Tonka Bean', 'Patchouli', 'Iris'], 380.0, 75, 'Eau de Parfum'),

    # --- AMBER & ORIENTAL (26 items) ---
    ('LL-160', 'Jimmy Choo', 'I Want Choo Le Parfum', ['i want choo', 'le parfum'], ['100ml'], 'oriental', ['Amber & Oriental', 'Opulent Amber Gourmand'], ['Pear', 'Blackberry', 'Gardenia', 'Jasmine Sambac', 'Patchouli', 'Ambrette', 'Praline', 'Sandalwood', 'Benzoin'], 315.0, 100, 'Parfum'),
    ('LL-161', 'Jimmy Choo', 'I Want Choo', ['i want choo'], ['100ml', 'edp'], 'oriental', ['Amber & Oriental', 'Solar Floral Amber'], ['Mandarin Juice', 'Velvet Peach', 'Red Spider Lily', 'Jasmine Sambac', 'Vanilla', 'Benzoin'], 295.0, 100, 'Eau de Parfum'),
    ('LL-162', 'Dolce & Gabbana', 'Dolce Garden', ['dolce garden'], ['75ml'], 'oriental', ['Amber & Oriental', 'Gourmand Coconut Amber'], ['Mandarin Orange', 'Magnolia', 'Neroli', 'Coconut', 'Frangipani', 'Ylang-Ylang', 'Vanilla Absolute', 'Almond Milk', 'Sandalwood'], 229.0, 75, 'Eau de Parfum'),
    ('LL-163', 'Dolce & Gabbana', 'Devotion Intense', ['devotion', 'intense'], ['100ml'], 'oriental', ['Amber & Oriental', 'Rich Gourmand Amber'], ['Candied Hazelnut', 'Orange Blossom', 'Vanilla Caviar'], 410.0, 100, 'Eau de Parfum Intense'),
    ('LL-164', 'Paco Rabanne', 'Million Gold for Her', ['million gold', 'her'], ['90ml'], 'oriental', ['Amber & Oriental', 'Solar Metallic Floral'], ['Rose', 'White Flowers', 'Solar Mineral Musk'], 479.0, 90, 'Eau de Parfum'),
    ('LL-165', 'Paco Rabanne', 'Olympéa Absolu', ['olympea', 'absolu'], ['80ml'], 'oriental', ['Amber & Oriental', 'Warm Amber Vanilla'], ['Salty Vanilla', 'Orange Blossom', 'White Amber', 'Cashmere Wood'], 299.0, 80, 'Parfum Intense'),
    ('LL-166', 'Mugler', 'Alien Goddess', ['alien goddess'], ['90ml', '60ml'], 'oriental', ['Amber & Oriental', 'Solar Woody Amber'], ['Coconut Water', 'Bergamot', 'Jasmine', 'Heliotrope', 'Bourbon Vanilla', 'Cashmeran'], 379.0, 90, 'Eau de Parfum'),
    ('LL-167', 'Mugler', 'Angel Elixir', ['angel elixir'], ['100ml', '50ml'], 'oriental', ['Amber & Oriental', 'Woody Floral Gourmand'], ['Pink Pepper', 'Jasmine', 'Ylang-Ylang', 'Orange Blossom', 'Sandalwood', 'Bourbon Vanilla', 'Amber Xtreme'], 395.0, 100, 'Eau de Parfum'),
    ('LL-168', 'Ariana Grande', 'Cloud', ['ariana', 'cloud'], ['100ml'], 'oriental', ['Amber & Oriental', 'Gourmand Musk'], ['Lavender Blossom', 'Juicy Pear', 'Bergamot', 'Crème de Coconut', 'Praline', 'Vanilla Orchid', 'Sensual Musks', 'Creamy Blond Woods'], 289.0, 100, 'Eau de Parfum'),
    ('LL-169', 'Ariana Grande', 'Sweet Like Candy', ['sweet like candy'], ['100ml'], 'oriental', ['Amber & Oriental', 'Fruity Gourmand'], ['Blackberry', 'Pear', 'Bergamot', 'Whipped Cream', 'Marshmallow', 'Blackcurrant', 'Frangipani', 'Jasmine', 'Vanilla', 'Cashmere Wood'], 219.0, 100, 'Eau de Parfum'),
    ('LL-170', 'Lattafa', 'Yara Candy', ['yara candy'], ['100ml'], 'oriental', ['Amber & Oriental', 'Sweet Fruity Gourmand'], ['Green Tangerine', 'Blackcurrant', 'Strawberry Fizz Candy', 'Gardenia', 'Vanilla', 'Amber', 'Musk', 'Sandalwood'], 65.0, 100, 'Eau de Parfum'),
    ('LL-171', 'Lattafa', 'Angham Second Song', ['angham', 'second'], ['100ml'], 'oriental', ['Amber & Oriental', 'Amber Floral Vanilla'], ['Ginger', 'Mandarin', 'Pink Pepper', 'Praline', 'Jasmine', 'Lavender', 'Bourbon Vanilla', 'Amber', 'Musk'], 75.0, 100, 'Eau de Parfum'),
    ('LL-172', 'Montblanc', 'Signature Absolu', ['signature absolu'], ['90ml'], 'oriental', ['Amber & Oriental', 'Radiant Amber Floral'], ['Mandarin Orange', 'Pear', 'Pink Pepper', 'Tuberose', 'Ylang-Ylang', 'Frangipani', 'Tonka Bean', 'Cedar'], 225.0, 90, 'Eau de Parfum'),
    ('LL-173', 'Salvatore Ferragamo', 'Signorina', ['signorina', 'edp'], ['100ml'], 'oriental', ['Amber & Oriental', 'Fruity Gourmand Floral'], ['Red Currant', 'Pink Pepper', 'Rose', 'Peony', 'Jasmine', 'Panacotta', 'Patchouli', 'Musk'], 175.0, 100, 'Eau de Parfum'),
    ('LL-174', 'Salvatore Ferragamo', 'Signorina Misteriosa', ['misteriosa'], ['100ml'], 'oriental', ['Amber & Oriental', 'Dark Fruity Amber'], ['Blackberry', 'Neroli', 'Tuberose', 'Orange Blossom', 'Patchouli', 'Black Vanilla Mousse'], 199.0, 100, 'Eau de Parfum'),
    ('LL-175', 'Guess', 'Seductive Women', ['guess', 'seductive', 'w'], ['75ml'], 'oriental', ['Amber & Oriental', 'Floral Fruity Amber'], ['Bergamot', 'Blackcurrant', 'Pear', 'Jasmine', 'African Orange Flower', 'Orris Root', 'Vanille', 'Olibanum', 'Cashmere Wood'], 79.0, 75, 'Eau de Toilette'),
    ('LL-176', 'Guess', 'Seductive Noir Women', ['seductive noir', 'w'], ['75ml'], 'oriental', ['Amber & Oriental', 'Warm Amber Vanilla'], ['Bergamot', 'Peony', 'Sage', 'Jasmine Sambac', 'Iris', 'Lily-of-the-Valley', 'Vanilla', 'Haitian Vetiver', 'Velvet'], 89.0, 75, 'Eau de Toilette'),
    ('LL-177', 'Escada', 'Party Love', ['party love'], ['100ml'], 'oriental', ['Amber & Oriental', 'Gourmand Vanilla'], ['Dark Cherry', 'Whipped Cream', 'Vanilla Cupcake Accord'], 160.0, 100, 'Eau de Parfum'),
    ('LL-178', 'Jean Paul Gaultier', 'Scandal Le Parfum', ['scandal', 'le parfum'], ['80ml'], 'oriental', ['Amber & Oriental', 'Salted Caramel Amber'], ['Jasmine', 'Salted Caramel', 'Black Vanilla'], 439.0, 80, 'Eau de Parfum Intense'),
    ('LL-179', 'Jean Paul Gaultier', 'La Belle Le Parfum', ['la belle', 'le parfum'], ['100ml'], 'oriental', ['Amber & Oriental', 'Intense Vanilla Gourmand'], ['Pear', 'Tonka Bean', 'Vanilla'], 435.0, 100, 'Eau de Parfum Intense'),
    ('LL-180', 'Carolina Herrera', 'Very Good Girl Glam', ['good girl', 'glam'], ['80ml'], 'oriental', ['Amber & Oriental', 'Cherry Amber Floral'], ['Black Cherry', 'Bitter Almond', 'Rose', 'Lily', 'Bourbon Vanilla', 'Vetiver'], 479.0, 80, 'Eau de Parfum'),
    ('LL-181', 'Carolina Herrera', '212 VIP', ['212 vip', 'w'], ['80ml'], 'oriental', ['Amber & Oriental', 'Rum Passionfruit Amber'], ['Passionfruit', 'Rum', 'Musk', 'Gardenia', 'Tonka Bean', 'Vanilla'], 340.0, 80, 'Eau de Parfum'),
    ('LL-182', 'Guerlain', 'Samsara', ['samsara', 'women'], ['75ml'], 'oriental', ['Amber & Oriental', 'Woody Amber Floral'], ['Ylang-Ylang', 'Peach', 'Bergamot', 'Green Notes', 'Lemon', 'Iris', 'Jasmine', 'Orris Root', 'Narcissus', 'Violet', 'Rose', 'Sandalwood', 'Iris', 'Vanilla', 'Tonka Bean', 'Amber', 'Musk'], 390.0, 75, 'Eau de Parfum'),
    ('LL-183', 'Prada', 'Candy', ['prada candy'], ['80ml'], 'oriental', ['Amber & Oriental', 'Caramel Amber Gourmand'], ['Caramel', 'Powdery Notes', 'Musk', 'Vanilla', 'Benzoin'], 380.0, 80, 'Eau de Parfum'),
    ('LL-184', 'Yves Saint Laurent', 'Libre Flowers & Flames', ['libre', 'flowers'], ['90ml'], 'oriental', ['Amber & Oriental', 'Spicy Floral Amber'], ['Lavender', 'Bergamot', 'Desert Lily', 'Palm Tree', 'Orange Blossom', 'Vanilla Caviar'], 449.0, 90, 'Eau de Parfum Florale'),
    ('LL-185', 'Lalique', 'Soleil', ['lalique soleil'], ['100ml'], 'oriental', ['Amber & Oriental', 'Gourmand Solar Amber'], ['Mandarin Orange', 'Bitter Almond', 'Cardamom', 'Pear', 'Milk', 'Caffè Latte', 'Caramel', 'Jasmine', 'Praline', 'White Musk', 'Sandalwood'], 189.0, 100, 'Eau de Parfum'),

    # --- WOODY & EARTHY (15 items) ---
    ('LL-186', 'Narciso Rodriguez', 'Narciso Poudrée', ['narciso poudree'], ['90ml'], 'woody', ['Woody & Earthy', 'Powdery Woody Floral'], ['Jasmine', 'Bulgarian Rose', 'Orange Blossom', 'Musk', 'Coumarin', 'Cedar', 'Vetiver', 'Patchouli'], 315.0, 90, 'Eau de Parfum'),
    ('LL-187', 'Narciso Rodriguez', 'Musc Nude', ['musc nude'], ['100ml'], 'woody', ['Woody & Earthy', 'Solar Woody Musk'], ['White Flowers', 'Jasmine', 'Pink Pepper', 'Musk', 'Damask Rose', 'Tonka Bean', 'Patchouli', 'Cedarwood'], 345.0, 100, 'Eau de Parfum'),
    ('LL-188', 'Guerlain', 'L’Instant Magic', ['instant magic'], ['75ml'], 'woody', ['Woody & Earthy', 'Woody Floral Musk'], ['Anise', 'Bergamot', 'Lemon', 'Violet', 'Mimosa', 'Rose', 'Freesia', 'Carnation', 'White Musk', 'Almond', 'Iris', 'Vanilla', 'Sandalwood', 'Cedar'], 390.0, 75, 'Eau de Parfum'),
    ('LL-189', 'Tom Ford', 'Velvet Orchid', ['velvet orchid'], ['100ml'], 'woody', ['Woody & Earthy', 'Dark Floral Woody'], ['Rum', 'Honey', 'Mandarin Orange', 'Bergamot', 'Black Orchid', 'Orchid', 'Jasmine', 'Heliotrope', 'Hyacinth', 'Rose Oil', 'Narcissus', 'Magnolia', 'Orange Blossom', 'Vanilla', 'Myrrh', 'Suede', 'Sandalwood', 'Peru Balsam', 'Labdanum'], 580.0, 100, 'Eau de Parfum'),
    ('LL-190', 'Cartier', 'La Panthère Parfum', ['panthere', 'parfum'], ['75ml'], 'woody', ['Woody & Earthy', 'Chypre Floral Leather'], ['Apricot', 'Osmanthus', 'Gardenia', 'Patchouli', 'Moss', 'Musk'], 440.0, 75, 'Parfum'),
    ('LL-191', 'Chloé', 'Nomade Jasmin Naturel', ['nomade', 'naturel'], ['75ml'], 'woody', ['Woody & Earthy', 'Gourmand Woody Chypre'], ['Mirabelle', 'Pear', 'Egyptian Jasmine', 'Dates', 'Vanilla', 'Sandalwood', 'Oakmoss', 'Patchouli'], 375.0, 75, 'Eau de Parfum'),
    ('LL-192', 'Givenchy', 'L’Interdit Eau de Parfum Intense', ['interdit', 'intense'], ['80ml'], 'woody', ['Woody & Earthy', 'Dark Woody Floral'], ['Black Pepper', 'Tuberose', 'Orange Blossom', 'Roasted Black Sesame', 'Madagascar Vanilla', 'Patchouli', 'Vetiver'], 435.0, 80, 'Eau de Parfum Intense'),
    ('LL-193', 'Hermès', 'Elixir des Merveilles', ['elixir des merveilles'], ['100ml'], 'woody', ['Woody & Earthy', 'Amber Woody Balsamic'], ['Candied Orange Peel', 'Amber', 'Caramel', 'Peru Balsam', 'Siam Resin', 'Tonka Bean', 'Patchouli', 'Oakmoss', 'Incense', 'Sandalwood', 'Cedar'], 480.0, 100, 'Eau de Parfum'),
    ('LL-194', 'Burberry', 'My Burberry Black', ['my burberry black'], ['90ml'], 'woody', ['Woody & Earthy', 'Amber Floral Woody'], ['Jasmine', 'Peach Nectar', 'Candied Rose', 'Amber', 'Patchouli'], 360.0, 90, 'Eau de Parfum'),
    ('LL-195', 'Guerlain', 'Patchouli Ardent', ['patchouli ardent'], ['125ml'], 'woody', ['Woody & Earthy', 'Woody Floral Musk'], ['Fig', 'Pink Pepper', 'Black Pepper', 'Turkish Rose', 'Patchouli', 'Cedar', 'Leather', 'Musk'], 590.0, 125, 'Eau de Parfum'),
    ('LL-196', 'Guerlain', 'Musc Noble', ['musc noble'], ['125ml'], 'woody', ['Woody & Earthy', 'Woody Floral Musk'], ['Saffron', 'Pink Pepper', 'Aldehydes', 'Rose', 'Musk', 'Geranium', 'White Amber', 'Cedar', 'Leather', 'Labdanum', 'Orris Root'], 590.0, 125, 'Eau de Parfum'),
    ('LL-197', 'Bvlgari', 'Splendida Jasmin Noir', ['jasmin noir'], ['100ml'], 'woody', ['Woody & Earthy', 'Woody White Floral'], ['Gardenia', 'Green Notes', 'Jasmine Sambac', 'Satin Almond', 'Heart of Patchouli', 'Cashmeran', 'Tonka Bean'], 380.0, 100, 'Eau de Parfum'),
    ('LL-198', 'Elie Saab', 'Le Parfum Royal', ['le parfum royal'], ['90ml'], 'woody', ['Woody & Earthy', 'Chypre Floral Royal'], ['Mandarin Orange', 'Turkish Rose', 'Bulgarian Rose', 'Lebanese Neroli', 'Indonesian Patchouli', 'Indian Sandalwood', 'Amber', 'Vanilla'], 220.0, 90, 'Eau de Parfum'),
    ('LL-199', 'Lancôme', 'Magie Noire', ['magie noire'], ['75ml'], 'woody', ['Woody & Earthy', 'Chypre Earthy Mossy'], ['Galbanum', 'Cassis', 'Cassia', 'Hyacinth', 'Bulgarian Rose', 'Raspberry', 'Bergamot', 'Honey', 'Narcissus', 'Cedar', 'Orris Root', 'Ylang-Ylang', 'Jasmine', 'Lily-of-the-Valley', 'Tuberose', 'Oakmoss', 'Spices', 'Civet', 'Incense', 'Patchouli', 'Amber', 'Sandalwood', 'Vetiver', 'Musk'], 320.0, 75, 'Eau de Toilette'),
    ('LL-200', 'Roberto Cavalli', 'Gemma di Paradiso', ['gemma di paradiso'], ['75ml'], 'woody', ['Woody & Earthy', 'Amber Woody Floral'], ['Pear', 'Mandarin Orange', 'Floral Notes', 'Jasmine', 'Precious Woods', 'Vanilla', 'Amber'], 140.0, 75, 'Eau de Parfum')
]

used_slugs = set(p['slug'] for p in existing_100)
row_idx = len(existing_100) + 1
new_items_list = []

for (sku, brand, name, req_tok, pref_tok, category, families, notes, def_price, def_size, def_conc) in NEW_100_ITEMS:
    best_lp = find_lp(req_tok, pref_tok)
    
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
            print(f"[{sku}] Image error for {img_src}: {e}")
    elif os.path.exists(local_img_file):
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
        "featured": sku in ['LL-101', 'LL-128', 'LL-142', 'LL-143', 'LL-160', 'LL-168', 'LL-189']
    }
    new_items_list.append(product_obj)
    row_idx += 1

print(f"\nGenerated {len(new_items_list)} new women's products!")

# Combine 100 existing + 100 new = 200 total
final_200 = existing_100 + new_items_list
print(f"Total unified catalog count: {len(final_200)}")

from collections import Counter
cat_counts = Counter(p['category'] for p in final_200)
print(f"Final 200 Category breakdown: {dict(cat_counts)}")

with open(PRODUCTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(final_200, f, indent=2, ensure_ascii=False)

print(f"Successfully updated {PRODUCTS_JSON} to {len(final_200)} products!")
