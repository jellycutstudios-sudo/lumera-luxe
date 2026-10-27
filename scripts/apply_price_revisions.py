import openpyxl
import json
import re
import os

EXCEL_PATH = '/Users/LUMÈRA_LUXE/Lumera_Luxe_Qatar_Perfume_Price_Comparison.xlsx'
PRODUCTS_JSON_PATH = '/Users/LUMÈRA_LUXE/src/data/products.json'
PUBLIC_PRODUCTS_DIR = '/Users/LUMÈRA_LUXE/public/assets/products'

wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
ws = wb['Sheet1']

with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
    existing_products = json.load(f)

def clean(s):
    s = s.lower()
    s = re.sub(r'delete', '', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

prod_map = {clean(p['fullName']): p for p in existing_products}

# Metadata for the 11 new additions
NEW_PRODUCTS_METADATA = {
    'dolce & gabbana velevet desert oud': {
        'brand': 'Dolce & Gabbana',
        'name': 'Velvet Desert Oud',
        'fullName': 'Dolce & Gabbana Velvet Desert Oud',
        'slug': 'dolce-and-gabbana-velvet-desert-oud',
        'sizeMl': 100,
        'sizeDisplay': '100ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Woody Amber Oud'],
        'keyNotes': ['Incense', 'Amber', 'Agarwood (Oud)', 'Musk', 'Woody Notes'],
        'rawNotes': 'Incense, Amber, Agarwood (Oud), Musk, Woody Notes',
        'description': 'A precious royal oud composition from Dolce & Gabbana’s Velvet Collection. Velvet Desert Oud weaves deep smoky incense, luscious amber, and authentic dark oud into an opulent desert sunset ritual.',
        'image': '/assets/products/dolce-and-gabbana-velvet-desert-oud.webp',
        'featured': True,
    },
    'guerlain cuir intense': {
        'brand': 'Guerlain',
        'name': 'Cuir Intense',
        'fullName': 'Guerlain Cuir Intense',
        'slug': 'guerlain-cuir-intense',
        'sizeMl': 125,
        'sizeDisplay': '125ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Deep Leather Woody'],
        'keyNotes': ['Osmanthus', 'Ylang-Ylang', 'Leather', 'Musk', 'Tobacco', 'Sandalwood', 'Virginia Cedar'],
        'rawNotes': 'Osmanthus, Ylang-Ylang, Leather, Musk, Tobacco, Sandalwood, Virginia Cedar',
        'description': 'An intense, hypnotic leather symphony from Guerlain’s Les Absolus d’Orient. Cuir Intense pairs bold dark leather and aromatic woods with delicate floral facets of apricot osmanthus and golden ylang-ylang.',
        'image': '/assets/products/guerlain-cuir-intense.webp',
        'featured': True,
    },
    'tom ford noir extreme': {
        'brand': 'Tom Ford',
        'name': 'Noir Extreme',
        'fullName': 'Tom Ford Noir Extreme',
        'slug': 'tom-ford-noir-extreme',
        'sizeMl': 100,
        'sizeDisplay': '100ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Warm Amber Woody'],
        'keyNotes': ['Cardamom', 'Nutmeg', 'Saffron', 'Kulfi', 'Rose', 'Mastic', 'Jasmine', 'Vanilla', 'Amber', 'Sandalwood'],
        'rawNotes': 'Cardamom, Nutmeg, Saffron, Mandarin Orange, Neroli, Kulfi Accords, Rose, Mastic, Jasmine, Orange Blossom, Vanilla, Amber, Woody Notes, Sandalwood',
        'description': 'An amber-drenched, woody oriental fragrance with a tantalizing heart of Indian Kulfi. Tom Ford Noir Extreme captures an intoxicating tension between refined amber warmth and decadent spiced sophistication.',
        'image': '/assets/products/tom-ford-noir-extreme.webp',
        'featured': True,
    },
    'chopard oud malaki': {
        'brand': 'Chopard',
        'name': 'Oud Malaki',
        'fullName': 'Chopard Oud Malaki',
        'slug': 'chopard-oud-malaki',
        'sizeMl': 80,
        'sizeDisplay': '80ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Warm Spicy Oud'],
        'keyNotes': ['Grapefruit', 'Lavender', 'Artemisia', 'Tobacco', 'Spices', 'Leather', 'Agarwood (Oud)', 'Dark Woods', 'Ambergris'],
        'rawNotes': 'Grapefruit, Lavender, Artemisia, Tobacco, Spices, Leather, Agarwood (Oud), Dark Woods, Ambergris',
        'description': 'A luminous benchmark in modern Middle Eastern perfumery. Chopard Oud Malaki balances glowing amber and aromatic tobacco leaves with smoky oud and refined leather for regal, enduring presence.',
        'image': '/assets/products/chopard-oud-malaki.webp',
        'featured': True,
    },
    'chopard leather malaki': {
        'brand': 'Chopard',
        'name': 'Leather Malaki',
        'fullName': 'Chopard Leather Malaki',
        'slug': 'chopard-leather-malaki',
        'sizeMl': 80,
        'sizeDisplay': '80ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Smoky Leather'],
        'keyNotes': ['Bergamot', 'Smoke Accords', 'Black Pepper', 'Leather', 'Cedar', 'Amber', 'Mineral Notes'],
        'rawNotes': 'Bergamot, Smoke Accords, Black Pepper, Leather, Cedar, Amber, Mineral Notes',
        'description': 'A tribute to the noble tradition of fine leathercraft. Chopard Leather Malaki unfolds with crisp Italian bergamot, smoky accents, velvety hide, and resplendent ambery cedar.',
        'image': '/assets/products/chopard-leather-malaki.webp',
        'featured': False,
    },
    'chopard black incense malaki': {
        'brand': 'Chopard',
        'name': 'Black Incense Malaki',
        'fullName': 'Chopard Black Incense Malaki',
        'slug': 'chopard-black-incense-malaki',
        'sizeMl': 80,
        'sizeDisplay': '80ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Resinous Woody Incense'],
        'keyNotes': ['Incense (Olibanum)', 'Resins', 'Leather', 'Agarwood (Oud)', 'Spices', 'Patchouli', 'Cedar'],
        'rawNotes': 'Incense (Olibanum), Resins, Leather, Agarwood (Oud), Spices, Patchouli, Cedar',
        'description': 'A dark, magnetic incense elixir centered around royal Somalian Frankincense. Black Incense Malaki creates an aura of enigmatic luxury layered with pure resins, oud, and spiced leather.',
        'image': '/assets/products/chopard-black-incense-malaki.webp',
        'featured': True,
    },
    "boucheron ambre d'alexandrie": {
        'brand': 'Boucheron',
        'name': "Ambre d'Alexandrie",
        'fullName': "Boucheron Ambre d'Alexandrie",
        'slug': 'boucheron-ambre-d-alexandrie',
        'sizeMl': 125,
        'sizeDisplay': '125ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Amber Vanilla Resin'],
        'keyNotes': ['Vanilla', 'Benzoin', 'Tobacco', 'Amber', 'Cistus Labdanum', 'Ambergris', 'Musk'],
        'rawNotes': 'Vanilla, Benzoin, Tobacco, Amber, Cistus Labdanum, Ambergris, Musk',
        'description': 'Inspired by the ancient jewel and spice routes of Alexandria. This Boucheron masterpiece envelops the wearer in warm, honeyed amber, smoky tobacco nectar, creamy Madagascar vanilla, and benzoin.',
        'image': '/assets/products/boucheron-ambre-d-alexandrie.webp',
        'featured': True,
    },
    'boucheron patchouli': {
        'brand': 'Boucheron',
        'name': "Patchouli d'Angkor",
        'fullName': "Boucheron Patchouli d'Angkor",
        'slug': 'boucheron-patchouli-d-angkor',
        'sizeMl': 125,
        'sizeDisplay': '125ml',
        'concentration': 'Eau de Parfum',
        'category': 'woody',
        'scentFamilies': ['Woody & Earthy', 'Floral Chypre Patchouli'],
        'keyNotes': ['Damask Rose', 'Pear', 'Bourbon Pepper', 'Jasmine', 'Patchouli', 'Guaiac Wood', 'White Musk'],
        'rawNotes': 'Damask Rose, Pear, Bourbon Pepper, Jasmine, Patchouli, Guaiac Wood, White Musk',
        'description': 'An olfactory voyage to the sacred stone temples of Angkor. Earthy, noble Indonesian patchouli is illuminated by crystalline Damask rose, juicy pear, and sacred guaiac wood.',
        'image': '/assets/products/boucheron-patchouli-d-angkor.webp',
        'featured': False,
    },
    'boucheron orange': {
        'brand': 'Boucheron',
        'name': 'Orange de Bahia',
        'fullName': 'Boucheron Orange de Bahia',
        'slug': 'boucheron-orange-de-bahia',
        'sizeMl': 125,
        'sizeDisplay': '125ml',
        'concentration': 'Eau de Parfum',
        'category': 'fresh',
        'scentFamilies': ['Fresh & Citrus', 'Sparkling Citrus Green'],
        'keyNotes': ['Orange', 'Green Mandarin', 'Fig Leaf', 'Rose', 'Coconut Milk', 'White Cedar', 'Amberwood'],
        'rawNotes': 'Orange, Green Mandarin, Fig Leaf, Rose, Coconut Milk, White Cedar, Amberwood',
        'description': 'A vibrant sparkling citrus creation inspired by the lively rhythms of Bahia. Sunny Brazilian orange and green mandarin blend with lush fig leaf, delicate rose, and warm cedarwood.',
        'image': '/assets/products/boucheron-orange-de-bahia.webp',
        'featured': False,
    },
    'boucheron oud de carthage': {
        'brand': 'Boucheron',
        'name': 'Oud de Carthage',
        'fullName': 'Boucheron Oud de Carthage',
        'slug': 'boucheron-oud-de-carthage',
        'sizeMl': 125,
        'sizeDisplay': '125ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Smoky Leather Oud'],
        'keyNotes': ['Incense', 'Honey', 'Tonka Bean', 'Labdanum', 'Agarwood (Oud)', 'Leather'],
        'rawNotes': 'Incense, Honey, Tonka Bean, Labdanum, Agarwood (Oud), Leather',
        'description': 'An ode to the maritime treasures and rich trading history of Carthage. Mystical incense and wild honey melt into smoky leather and majestic oud wood.',
        'image': '/assets/products/boucheron-oud-de-carthage.webp',
        'featured': True,
    },
    'boucheron feve tonka': {
        'brand': 'Boucheron',
        'name': 'Fève Tonka de Canaima',
        'fullName': 'Boucheron Fève Tonka de Canaima',
        'slug': 'boucheron-feve-tonka-de-canaima',
        'sizeMl': 125,
        'sizeDisplay': '125ml',
        'concentration': 'Eau de Parfum',
        'category': 'oriental',
        'scentFamilies': ['Amber & Oriental', 'Warm Gourmand Tonka'],
        'keyNotes': ['Bitter Almond', 'Violet', 'Tonka Bean', 'Patchouli', 'Rose', 'Vanilla', 'Sandalwood'],
        'rawNotes': 'Bitter Almond, Violet, Tonka Bean, Patchouli, Rose, Vanilla, Sandalwood',
        'description': 'A warm, hypnotic oriental confection inspired by the untouched Venezuelan wilderness. Roasted tonka bean and bitter almond are wrapped in creamy vanilla orchid and rich sandalwood.',
        'image': '/assets/products/boucheron-feve-tonka-de-canaima.webp',
        'featured': False,
    },
    'hermès eau des merveilles l': {
        'brand': 'Hermès',
        'name': 'Eau des Merveilles L',
        'fullName': 'Hermès Eau des Merveilles L',
        'slug': 'hermes-eau-des-merveilles-l',
        'sizeMl': 100,
        'sizeDisplay': '100ml',
        'concentration': 'Eau de Toilette',
        'category': 'woody',
        'scentFamilies': ['Woody & Earthy', 'Woody Amber Mineral'],
        'keyNotes': ['Orange', 'Elemi Resin', 'Lemon', 'Amber', 'Pepper', 'Pink Pepper', 'Violet', 'Fir', 'Cedar', 'Madagascar Vetiver', 'Oakmoss'],
        'rawNotes': 'Orange, Elemi Resin, Lemon, Amber, Pepper, Pink Pepper, Violet, Fir, Cedar, Madagascar Vetiver, Oakmoss',
        'description': 'An enchanting, radiant Hermès creation with no noticeable flower notes. A magical sparkling amber woody aura evoking the poetry of constellations and warm amber sands.',
        'image': '/assets/products/hermes-eau-des-merveilles-l-edt-100ml.webp',
        'featured': False,
    }
}

new_catalog = []

for r in range(2, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    if not any(vals):
        continue
    name_val = str(vals[1]).strip() if vals[1] else ''
    price_val = vals[2]   # Column C: Sticker / Original Price
    disc_val = vals[3]    # Column D: Lumera Selling Price
    
    # Check if yellow (delete)
    f = ws.cell(r, 2).fill
    c = f.fgColor if f else None
    if c and c.type == 'rgb' and c.rgb == 'FFFFFF00':
        print(f"Skipping yellow (deleted): Row {r} - {name_val}")
        continue

    # Identify if item exists or is new
    cn = clean(name_val)
    existing_p = None
    if not name_val.endswith(' L'):
        existing_p = prod_map.get(cn)
        if not existing_p:
            candidates = [p for k, p in prod_map.items() if cn in k or k in cn]
            if len(candidates) == 1:
                existing_p = candidates[0]

    # Calculate prices
    # disc_val = Selling Price (customer pays)
    # price_val = Sticker / Original Price
    if disc_val is not None and str(disc_val).strip() != '':
        selling_price = float(disc_val)
    elif existing_p and existing_p.get('priceMinor'):
        selling_price = float(existing_p['priceMinor']) / 100.0
    else:
        selling_price = 250.0

    if price_val is not None and str(price_val).strip() != '':
        sticker_price = float(price_val)
    elif existing_p and existing_p.get('stickerPriceMinor'):
        sticker_price = float(existing_p['stickerPriceMinor']) / 100.0
    else:
        sticker_price = None

    price_minor = int(round(selling_price * 100))
    price_display = f"{int(round(selling_price))} QAR"
    sticker_minor = int(round(sticker_price * 100)) if (sticker_price and sticker_price > selling_price) else (int(round(sticker_price * 100)) if sticker_price else None)

    if existing_p:
        item = dict(existing_p)
        item['priceMinor'] = price_minor
        item['priceDisplay'] = price_display
        item['stickerPriceMinor'] = sticker_minor
        # Special check: Hermès Eau des Merveilles L -> keep name Hermès Eau des Merveilles
        new_catalog.append(item)
    else:
        # Match against NEW_PRODUCTS_METADATA
        meta = None
        for mk, mv in NEW_PRODUCTS_METADATA.items():
            if clean(mk) in cn or cn in clean(mk):
                meta = mv
                break
        if not meta:
            print(f"ERROR: No metadata found for brand new item: {name_val}")
            continue

        item = {
            'id': '',
            'row': 0,
            'sku': '',
            'slug': meta['slug'],
            'brand': meta['brand'],
            'name': meta['name'],
            'fullName': meta['fullName'],
            'sizeMl': meta['sizeMl'],
            'sizeDisplay': meta['sizeDisplay'],
            'concentration': meta['concentration'],
            'currency': 'QAR',
            'priceMinor': price_minor,
            'priceDisplay': price_display,
            'stickerPriceMinor': sticker_minor,
            'image': meta['image'],
            'category': meta['category'],
            'scentFamilies': meta['scentFamilies'],
            'keyNotes': meta['keyNotes'],
            'rawNotes': meta['rawNotes'],
            'description': meta['description'],
            'isDraft': False,
            'draftReason': [],
            'featured': meta.get('featured', False)
        }
        new_catalog.append(item)

# Re-index cleanly 1..175
for idx, p in enumerate(new_catalog, 1):
    p['id'] = f"lum_{idx:03d}"
    p['row'] = idx
    p['sku'] = f"LL-{idx:03d}"

print(f"\nFinal catalog product count: {len(new_catalog)}")

# Backup old products.json
with open(PRODUCTS_JSON_PATH + '.bak', 'w', encoding='utf-8') as f:
    json.dump(existing_products, f, indent=2, ensure_ascii=False)

# Write updated products.json
with open(PRODUCTS_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(new_catalog, f, indent=2, ensure_ascii=False)

print("Saved updated src/data/products.json successfully!")
