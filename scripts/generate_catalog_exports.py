import json
import csv
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Paths
ROOT_DIR = '/Users/LUMÈRA_LUXE'
PRODUCTS_JSON_PATH = os.path.join(ROOT_DIR, 'src/data/products.json')
CSV_OUTPUT_PATH = os.path.join(ROOT_DIR, 'Lumera_Luxe_Catalog_200_Products.csv')
XLSX_OUTPUT_PATH = os.path.join(ROOT_DIR, 'Lumera_Luxe_Catalog_200_Products.xlsx')
PUBLIC_DOWNLOADS_DIR = os.path.join(ROOT_DIR, 'public/downloads')
os.makedirs(PUBLIC_DOWNLOADS_DIR, exist_ok=True)
PUBLIC_CSV_PATH = os.path.join(PUBLIC_DOWNLOADS_DIR, 'Lumera_Luxe_Catalog_200_Products.csv')
PUBLIC_XLSX_PATH = os.path.join(PUBLIC_DOWNLOADS_DIR, 'Lumera_Luxe_Catalog_200_Products.xlsx')

with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Loaded {len(products)} products from products.json")

# Prepare processed rows
processed_rows = []
for index, p in enumerate(products, 1):
    # Ensure uniform SKU LL-001 to LL-200
    sku = p.get('sku')
    if not sku:
        sku = f"LL-{index:03d}"
    
    internal_id = p.get('id', f"lum_{index:03d}")
    brand = p.get('brand', '').strip()
    name = p.get('name', '').strip()
    full_name = p.get('fullName', f"{brand} {name}").strip()
    category = p.get('category', '').strip().capitalize()
    
    # Scent families
    scent_families = p.get('scentFamilies', [])
    if isinstance(scent_families, list):
        scent_families_str = ', '.join(scent_families)
    else:
        scent_families_str = str(scent_families)
        
    size_ml = p.get('sizeMl') or 100
    size_display = p.get('sizeDisplay') or f"{size_ml}ml"
    concentration = p.get('concentration', 'Eau de Parfum').strip()
    currency = p.get('currency', 'QAR')
    
    price_qar = round(p.get('priceMinor', 0) / 100.0, 2)
    
    sticker_minor = p.get('stickerPriceMinor')
    if sticker_minor is not None and sticker_minor > 0:
        sticker_qar = round(sticker_minor / 100.0, 2)
        discount_qar = round(sticker_qar - price_qar, 2)
    else:
        sticker_qar = None
        discount_qar = None
        
    key_notes = p.get('keyNotes', [])
    if isinstance(key_notes, list):
        key_notes_str = ', '.join(key_notes)
    else:
        key_notes_str = str(key_notes)
        
    raw_notes = p.get('rawNotes', key_notes_str)
    description = p.get('description', '')
    slug = p.get('slug', '')
    store_url = f"https://lumeraluxe.qa/perfumes/{slug}"
    image_path = p.get('image', '')
    featured = "Yes" if p.get('featured') else "No"
    status = "Active"

    processed_rows.append({
        'sku': sku,
        'internal_id': internal_id,
        'brand': brand,
        'name': name,
        'full_name': full_name,
        'category': category,
        'scent_families': scent_families_str,
        'size_ml': size_ml,
        'size_display': size_display,
        'concentration': concentration,
        'currency': currency,
        'price_qar': price_qar,
        'sticker_qar': sticker_qar if sticker_qar is not None else "",
        'discount_qar': discount_qar if discount_qar is not None else "",
        'key_notes': key_notes_str,
        'raw_notes': raw_notes,
        'description': description,
        'slug': slug,
        'store_url': store_url,
        'image_path': image_path,
        'featured': featured,
        'status': status
    })

# Define CSV columns
headers = [
    ("SKU", 'sku'),
    ("Internal ID", 'internal_id'),
    ("Brand", 'brand'),
    ("Product Name", 'name'),
    ("Full Name", 'full_name'),
    ("Category", 'category'),
    ("Scent Families", 'scent_families'),
    ("Bottle Size (ml)", 'size_ml'),
    ("Size Display", 'size_display'),
    ("Concentration", 'concentration'),
    ("Currency", 'currency'),
    ("Price (QAR)", 'price_qar'),
    ("Original / Sticker Price (QAR)", 'sticker_qar'),
    ("Discount (QAR)", 'discount_qar'),
    ("Key Notes", 'key_notes'),
    ("Full Olfactory Notes", 'raw_notes'),
    ("Description", 'description'),
    ("Website Slug", 'slug'),
    ("Store URL", 'store_url'),
    ("Image Asset", 'image_path'),
    ("Featured", 'featured'),
    ("Status", 'status')
]

# Write CSV with UTF-8-SIG (BOM) so Excel opens UTF-8 characters like Nᵒ5 & French accents perfectly
for target_csv in [CSV_OUTPUT_PATH, PUBLIC_CSV_PATH]:
    with open(target_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([h[0] for h in headers])
        for row in processed_rows:
            writer.writerow([row[h[1]] for h in headers])
    print(f"Generated CSV: {target_csv}")

# Generate Excel Workbook
wb = Workbook()

# Colors (LUMÈRA LUXE luxury palette)
HEADER_BG = "2A2421"  # Deep luxury espresso
HEADER_FG = "FFFFFF"  # Crisp white
ACCENT_BG = "D4AF37"  # Warm Champagne Gold
ZEBRA_BG = "FBF9F7"   # Subtle warm cream
BORDER_COLOR = "E2DCD5"

header_font = Font(name="Segoe UI", size=11, bold=True, color=HEADER_FG)
header_fill = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type="solid")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

regular_font = Font(name="Segoe UI", size=10)
bold_font = Font(name="Segoe UI", size=10, bold=True)
zebra_fill = PatternFill(start_color=ZEBRA_BG, end_color=ZEBRA_BG, fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color=BORDER_COLOR),
    right=Side(style='thin', color=BORDER_COLOR),
    top=Side(style='thin', color=BORDER_COLOR),
    bottom=Side(style='thin', color=BORDER_COLOR)
)

# ----------------- SHEET 1: All Fragrances -----------------
ws1 = wb.active
ws1.title = f"All {len(processed_rows)} Products"
ws1.views.sheetView[0].showGridLines = True

# Add header
ws1.append([h[0] for h in headers])
ws1.row_dimensions[1].height = 28

for col_idx, cell in enumerate(ws1[1], 1):
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
    cell.border = thin_border

for row_idx, row in enumerate(processed_rows, 2):
    row_data = []
    for h in headers:
        val = row[h[1]]
        row_data.append(val)
    ws1.append(row_data)
    ws1.row_dimensions[row_idx].height = 20
    
    is_even = (row_idx % 2 == 0)
    for col_idx, cell in enumerate(ws1[row_idx], 1):
        cell.font = regular_font
        cell.border = thin_border
        if is_even:
            cell.fill = zebra_fill
            
        header_name = headers[col_idx - 1][0]
        # Alignments & Formats
        if header_name in ["SKU", "Internal ID", "Bottle Size (ml)", "Size Display", "Currency", "Featured", "Status"]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif header_name in ["Price (QAR)", "Original / Sticker Price (QAR)", "Discount (QAR)"]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            if isinstance(cell.value, (int, float)):
                cell.number_format = '#,##0.00'
        elif header_name in ["Description", "Key Notes", "Full Olfactory Notes"]:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Set Auto Filter and Freeze Panes
ws1.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(processed_rows) + 1}"
ws1.freeze_panes = "A2"

# Adjust column widths
for col in ws1.columns:
    max_len = 0
    col_letter = get_column_letter(col[0].column)
    header_title = str(col[0].value or '')
    for cell in col:
        val = str(cell.value or '')
        # Don't let long descriptions skew width completely
        if len(val) > 50:
            val = val[:50]
        if len(val) > max_len:
            max_len = len(val)
    adjusted_width = max(max_len + 4, len(header_title) + 4, 12)
    if col_letter in ['Q', 'P']: # Notes and description
        adjusted_width = min(adjusted_width, 45)
    ws1.column_dimensions[col_letter].width = min(adjusted_width, 50)

# ----------------- SHEET 2: Brand Summary -----------------
ws2 = wb.create_sheet(title="Brand Summary")
ws2.views.sheetView[0].showGridLines = True
ws2.row_dimensions[1].height = 28

brand_headers = ["Brand", "Total Products", "Min Price (QAR)", "Max Price (QAR)", "Avg Price (QAR)", "Categories Represented"]
ws2.append(brand_headers)

for col_idx, cell in enumerate(ws2[1], 1):
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
    cell.border = thin_border

brands_map = {}
for p in processed_rows:
    b = p['brand']
    if b not in brands_map:
        brands_map[b] = {'prices': [], 'categories': set()}
    brands_map[b]['prices'].append(p['price_qar'])
    brands_map[b]['categories'].add(p['category'])

sorted_brands = sorted(brands_map.items(), key=lambda x: (-len(x[1]['prices']), x[0]))

for row_idx, (brand_name, data) in enumerate(sorted_brands, 2):
    prices = data['prices']
    cats = ", ".join(sorted(list(data['categories'])))
    min_p = min(prices)
    max_p = max(prices)
    avg_p = round(sum(prices) / len(prices), 2)
    
    row_vals = [brand_name, len(prices), min_p, max_p, avg_p, cats]
    ws2.append(row_vals)
    ws2.row_dimensions[row_idx].height = 20
    
    is_even = (row_idx % 2 == 0)
    for col_idx, cell in enumerate(ws2[row_idx], 1):
        cell.font = regular_font
        cell.border = thin_border
        if is_even:
            cell.fill = zebra_fill
        if col_idx == 2:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [3, 4, 5]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '#,##0.00'
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Summary row for brands
brand_total_row = len(sorted_brands) + 2
all_prices = [p['price_qar'] for p in processed_rows]
ws2.append([
    "Total / Overall Catalog",
    len(processed_rows),
    min(all_prices),
    max(all_prices),
    round(sum(all_prices) / len(all_prices), 2),
    f"{len(brands_map)} Luxury Brands"
])
ws2.row_dimensions[brand_total_row].height = 22
for cell in ws2[brand_total_row]:
    cell.font = bold_font
    cell.fill = PatternFill(start_color="ECE7E1", end_color="ECE7E1", fill_type="solid")
    cell.border = thin_border
    if cell.column == 2:
        cell.alignment = Alignment(horizontal="center", vertical="center")
    elif cell.column in [3, 4, 5]:
        cell.alignment = Alignment(horizontal="right", vertical="center")
        cell.number_format = '#,##0.00'

for col in ws2.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws2.column_dimensions[col_letter].width = max(max_len + 4, 15)

# ----------------- SHEET 3: Category Breakdown -----------------
ws3 = wb.create_sheet(title="Category Breakdown")
ws3.views.sheetView[0].showGridLines = True
ws3.row_dimensions[1].height = 28

cat_headers = ["Category", "Fragrance Profile", "Product Count", "Catalog Share %", "Min Price (QAR)", "Max Price (QAR)", "Average Price (QAR)"]
ws3.append(cat_headers)

for col_idx, cell in enumerate(ws3[1], 1):
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_align
    cell.border = thin_border

cat_descriptions = {
    'Floral': 'Delicate blooms, romantic rose, jasmine, tuberose & powdery floral accords',
    'Fresh': 'Crisp citrus, sparkling bergamot, aquatic, aquatic green & summer notes',
    'Oriental': 'Warm amber, sensual vanilla, golden resin & exotic oriental spices',
    'Woody': 'Sophisticated cedarwood, sandalwood, vetiver, patchouli & smoky woods'
}

cat_map = {}
for p in processed_rows:
    c = p['category']
    if c not in cat_map:
        cat_map[c] = []
    cat_map[c].append(p['price_qar'])

for row_idx, (cat_name, c_prices) in enumerate(sorted(cat_map.items()), 2):
    count = len(c_prices)
    share = round((count / len(processed_rows)) * 100, 1)
    min_cp = min(c_prices)
    max_cp = max(c_prices)
    avg_cp = round(sum(c_prices) / count, 2)
    desc = cat_descriptions.get(cat_name, 'Fragrance notes and accords')
    
    ws3.append([cat_name, desc, count, f"{share}%", min_cp, max_cp, avg_cp])
    ws3.row_dimensions[row_idx].height = 22
    
    is_even = (row_idx % 2 == 0)
    for col_idx, cell in enumerate(ws3[row_idx], 1):
        cell.font = regular_font
        cell.border = thin_border
        if is_even:
            cell.fill = zebra_fill
        if col_idx in [3, 4]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [5, 6, 7]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '#,##0.00'

for col in ws3.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws3.column_dimensions[col_letter].width = max(max_len + 4, 16)

# ----------------- SHEET 4: Company & Compliance Info -----------------
ws4 = wb.create_sheet(title="About LUMÈRA LUXE")
ws4.views.sheetView[0].showGridLines = True

ws4.column_dimensions['A'].width = 30
ws4.column_dimensions['B'].width = 65

company_info = [
    ("LUMÈRA LUXE · Company & Catalog Specifications", ""),
    ("Brand Name", "LUMÈRA LUXE"),
    ("Brand Tagline", "Where Luxury Meets Affordability"),
    ("Legal Entity Name (English)", "Lumera Luxe Perfumes and Cosmetics W.L.L."),
    ("Legal Entity Name (Arabic)", "لوميرا لوكس للعطور ومستحضرات التجميل ذ.م.م"),
    ("Commercial Registration (C.R.)", "253967"),
    ("SME Classification", "Micro (متناهية الصغر)"),
    ("Legal Corporate Form", "W.L.L. (With Limited Liability / شركة ذات مسؤولية محدودة)"),
    ("Corporate Banking Partner", "Qatar National Bank (QNB) / بنك قطر الوطني"),
    ("Registered Location", "Doha, State of Qatar"),
    ("Official Currency", "QAR (Qatari Riyal)"),
    ("Total Products in Catalog", "200 Curated Luxury Perfumes"),
    ("Price Range", "59.00 QAR to 950.00 QAR"),
    ("Customer Concierge WhatsApp", "+974 6667 5166"),
    ("Customer Support Email", "info@lumeraluxe.com.qa"),
    ("Official Website", "https://lumeraluxe.qa"),
    ("Instagram", "@lumera.luxe974"),
    ("TikTok", "@luxescentqatar"),
    ("Dispatch & Delivery", "Nationwide Delivery across Qatar via local VIP courier dispatch")
]

for row_idx, (field, val) in enumerate(company_info, 1):
    ws4.append([field, val])
    ws4.row_dimensions[row_idx].height = 22
    cell_a = ws4.cell(row=row_idx, column=1)
    cell_b = ws4.cell(row=row_idx, column=2)
    
    if row_idx == 1:
        cell_a.font = Font(name="Segoe UI", size=13, bold=True, color=HEADER_FG)
        cell_a.fill = header_fill
        cell_b.fill = header_fill
        ws4.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)
        cell_a.alignment = Alignment(horizontal="left", vertical="center")
    else:
        cell_a.font = bold_font
        cell_b.font = regular_font
        cell_a.border = thin_border
        cell_b.border = thin_border
        cell_a.fill = PatternFill(start_color="F7F5F2", end_color="F7F5F2", fill_type="solid")
        cell_a.alignment = Alignment(horizontal="left", vertical="center")
        cell_b.alignment = Alignment(horizontal="left", vertical="center")

# Save workbook to both root and public/downloads
for target_xlsx in [XLSX_OUTPUT_PATH, PUBLIC_XLSX_PATH]:
    wb.save(target_xlsx)
    print(f"Generated XLSX: {target_xlsx}")

print("Successfully exported all 200 products to CSV and XLSX!")
