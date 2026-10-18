import zipfile
import xml.etree.ElementTree as ET
import json
import os
import shutil
import re

workspace_dir = '/Users/LUMÈRA_LUXE'
xlsx_path = os.path.join(workspace_dir, 'LumeraLuxePerfumesandPricing.xlsx')
extracted_dir = os.path.join(workspace_dir, 'extracted_images')
public_prod_dir = os.path.join(workspace_dir, 'public', 'assets', 'products')
private_source_dir = os.path.join(workspace_dir, 'private-source')
src_data_dir = os.path.join(workspace_dir, 'src', 'data')

os.makedirs(public_prod_dir, exist_ok=True)
os.makedirs(private_source_dir, exist_ok=True)
os.makedirs(src_data_dir, exist_ok=True)

with zipfile.ZipFile(xlsx_path, 'r') as z:
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        ss_tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
        ns_ss = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        for si in ss_tree.findall('s:si', ns_ss):
            shared_strings.append(''.join(t.text for t in si.findall('.//s:t', ns_ss) if t.text))

    def get_sheet_rows(target):
        tree = ET.fromstring(z.read(target))
        ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        rows = {}
        for row in tree.findall('m:sheetData/m:row', ns):
            r_idx = int(row.attrib['r'])
            cells = {}
            for c in row.findall('m:c', ns):
                col = ''.join([ch for ch in c.attrib['r'] if ch.isalpha()])
                t = c.attrib.get('t')
                v = c.find('m:v', ns)
                val = v.text if v is not None else ''
                if t == 's' and val.isdigit():
                    val = shared_strings[int(val)]
                cells[col] = val
            rows[r_idx] = cells
        return rows

    s1 = get_sheet_rows('xl/worksheets/sheet1.xml')
    s2 = get_sheet_rows('xl/worksheets/sheet2.xml')

# Brand extraction heuristics
KNOWN_BRANDS = [
    'Aigner', 'Boucheron', 'Burberry', 'Carolina Herrera', 'Chanel',
    'Chloé', 'Coach', 'Dolce & Gabbana', 'Dolce & Gababana', 'Giorgio Armani',
    'Givenchy', 'Jimmy Choo', 'Juicy Couture', 'Lancome', 'Lanvin',
    'Lalique', 'Narciso Rodriguez', 'Paco Rabanne', 'Roberto Cavalli'
]

products = []
discrepancies = []

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text

for r in range(3, 28):
    row1 = s1.get(r, {})
    row2 = s2.get(r, {})
    raw_name_1 = row1.get('A', '').strip()
    raw_name_2 = row2.get('A', '').strip()
    size_1 = row1.get('B', '').strip()
    size_2 = row2.get('B', '').strip()
    sticker = row1.get('C', '').strip()
    price = row1.get('D', '').strip()
    family_1 = row1.get('F', '').strip()
    family_2 = row2.get('D', '').strip()
    notes_1 = row1.get('G', '').strip()
    notes_2 = row2.get('E', '').strip()
    
    img_idx = r - 2
    src_img = f'image{img_idx}.png'
    
    # Identify Brand
    brand = 'Unknown'
    clean_name = raw_name_1
    for b in KNOWN_BRANDS:
        if raw_name_1.lower().startswith(b.lower()):
            brand = b
            clean_name = raw_name_1[len(b):].strip()
            break
            
    # Fix known typos
    if brand == 'Dolce & Gababana':
        brand = 'Dolce & Gabbana'
    if brand == 'Lancome':
        brand = 'Lancôme'
        
    # Detect concentration
    concentration = 'Eau de Parfum'
    if 'EDT' in raw_name_1 or 'EDT' in raw_name_2:
        concentration = 'Eau de Toilette'
    elif 'EDP intense' in raw_name_1 or 'EDP intense' in raw_name_2:
        concentration = 'Eau de Parfum Intense'
    elif 'EDP' in raw_name_1 or 'EDP' in raw_name_2:
        concentration = 'Eau de Parfum'
    elif 'EDU' in raw_name_1 or 'EDU' in raw_name_2:
        concentration = 'EDU (Pending Owner Confirmation)'

    # Clean name of concentration suffixes for display
    display_name = clean_name
    for token in ['EDP intense', 'EDP Intense', 'EDP', 'EDT', 'EDU']:
        display_name = display_name.replace(token, '').strip()
    if display_name.startswith('CH CH'):
        display_name = 'CH'
        
    # Check for discrepancies
    diffs = []
    if raw_name_1 != raw_name_2:
        diffs.append(f"Name mismatch: Brands='{raw_name_1}' vs ImageNotes='{raw_name_2}'")
    if size_1 != size_2:
        diffs.append(f"Size mismatch: Brands='{size_1}' vs ImageNotes='{size_2}'")
    if 'EDU' in raw_name_1 or 'EDU' in raw_name_2:
        diffs.append("EDU concentration requires owner confirmation (EDP/EDT)")
    if 'Gababana' in raw_name_1:
        diffs.append("Brand typo 'Dolce & Gababana' corrected to 'Dolce & Gabbana'")
    if 'Jenne' in raw_name_1:
        diffs.append("Perfume name typo 'Jenne' (Jeanne Blossom)")
        
    is_draft = len(diffs) > 0
    if is_draft:
        discrepancies.append({
            'row': r,
            'brand': brand,
            'name': raw_name_1,
            'issues': diffs
        })
        
    # Normalize size in ml
    size_ml = 100
    m_size = re.search(r'(\d+)', size_1)
    if m_size:
        size_ml = int(m_size.group(1))

    # Notes normalization
    notes_text = notes_1 or notes_2
    notes_clean = re.sub(r'^(Main NotesL|Notes:)\s*', '', notes_text, flags=re.I).strip()
    key_notes = [n.strip() for n in re.split(r'[,/]', notes_clean) if n.strip()]

    # Families
    fam_text = family_1 or family_2
    families = [f.strip() for f in fam_text.split('/') if f.strip()]

    # Copy image to public assets with SEO-friendly slug
    slug = slugify(f"{brand} {display_name}")
    asset_img_filename = f"{slug}.png"
    src_file_path = os.path.join(extracted_dir, src_img)
    dest_file_path = os.path.join(public_prod_dir, asset_img_filename)
    if os.path.exists(src_file_path):
        shutil.copy2(src_file_path, dest_file_path)

    selling_price_num = int(price) if price.isdigit() else 0
    sticker_price_num = int(sticker) if sticker.isdigit() else 0

    product_entry = {
        'id': f"lum_{r:03d}",
        'row': r,
        'slug': slug,
        'brand': brand,
        'name': display_name,
        'fullName': f"{brand} {display_name}",
        'sizeMl': size_ml,
        'sizeDisplay': size_1,
        'concentration': concentration,
        'currency': 'QAR',
        'priceMinor': selling_price_num * 100,
        'priceDisplay': f"{selling_price_num} QAR",
        'stickerPriceMinor': sticker_price_num * 100, # private reference only
        'image': f"/assets/products/{asset_img_filename}",
        'scentFamilies': families,
        'keyNotes': key_notes[:8],
        'rawNotes': notes_clean,
        'description': f"A luxurious fragrance by {brand}, blending {' and '.join(families)} accords with prominent notes of {', '.join(key_notes[:4])}.",
        'isDraft': is_draft,
        'draftReason': diffs if is_draft else [],
        'featured': r in [3, 4, 8, 12] # Initial 4 selected products for hero showcase
    }
    products.append(product_entry)

# Write src/data/products.json
with open(os.path.join(src_data_dir, 'products.json'), 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

# Write private-source/discrepancy_report.md
report_content = f"""# LUMÈRA LUXE — Source Audit & Discrepancy Report
Generated from `LumeraLuxePerfumesandPricing.xlsx`

Total records parsed: {len(products)}
Total flagged with discrepancies (marked draft pending owner approval): {len(discrepancies)}
Total ready for immediate preview: {len(products) - len(discrepancies)}

## Identified Discrepancies & Blockers

| Row | Brand | Sheet 1 Name | Issues Detected |
|---|---|---|---|
"""
for d in discrepancies:
    issues_str = '<br>'.join(d['issues'])
    report_content += f"| {d['row']} | {d['brand']} | {d['name']} | {issues_str} |\n"

report_content += """
## Commercial Notes
1. **Currency**: Provisionally set to **QAR** (Qatar Riyals) as requested in implementation plan.
2. **Change Sticker Column**: Kept strictly as internal private data (`stickerPriceMinor`). Never exposed in customer-facing UI as a discount or strike-through price.
3. **EDU Concentrations**: Confirmed need for owner input on Chanel N°5 and Lalique Amethyst Éclat.
4. **Volume Conflicts**: Givenchy Dahlia Divin and Lancôme Idôle show 100ml in Brands vs 75ml in Image and notes.
"""

with open(os.path.join(private_source_dir, 'discrepancy_report.md'), 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"Catalogue processing complete: {len(products)} products, {len(discrepancies)} discrepancies recorded.")
