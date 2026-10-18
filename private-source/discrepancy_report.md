# LUMÈRA LUXE — Source Audit & Discrepancy Report
Generated from `LumeraLuxePerfumesandPricing.xlsx`

Total records parsed: 25
Total flagged with discrepancies (marked draft pending owner approval): 8
Total ready for immediate preview: 17

## Identified Discrepancies & Blockers

| Row | Brand | Sheet 1 Name | Issues Detected |
|---|---|---|---|
| 6 | Carolina Herrera | Carolina Herrera CH Women EDP | Name mismatch: Brands='Carolina Herrera CH Women EDP' vs ImageNotes='Carolina Herrera CH Women EDT' |
| 8 | Chanel | Chanel Nᵒ5 EDU | Name mismatch: Brands='Chanel Nᵒ5 EDU' vs ImageNotes='Chanel N 5 EDU'<br>EDU concentration requires owner confirmation (EDP/EDT) |
| 14 | Dolce & Gabbana | Dolce & Gabbana The Only One EDP | Size mismatch: Brands='100ml' vs ImageNotes='100' |
| 15 | Dolce & Gabbana | Dolce & Gababana Dolce Rose EDT | Brand typo 'Dolce & Gababana' corrected to 'Dolce & Gabbana' |
| 17 | Givenchy | Givenchy Dahlia Divin EDP | Size mismatch: Brands='100ml' vs ImageNotes='75ml' |
| 22 | Lancôme | Lancome IDOLE EDP | Size mismatch: Brands='100ml' vs ImageNotes='75ml' |
| 23 | Lanvin | Lanvin Jenne Blossom EDP | Perfume name typo 'Jenne' (Jeanne Blossom) |
| 24 | Lalique | Lalique Amethyst Eclat EDU | EDU concentration requires owner confirmation (EDP/EDT) |

## Commercial Notes
1. **Currency**: Provisionally set to **QAR** (Qatar Riyals) as requested in implementation plan.
2. **Change Sticker Column**: Kept strictly as internal private data (`stickerPriceMinor`). Never exposed in customer-facing UI as a discount or strike-through price.
3. **EDU Concentrations**: Confirmed need for owner input on Chanel N°5 and Lalique Amethyst Éclat.
4. **Volume Conflicts**: Givenchy Dahlia Divin and Lancôme Idôle show 100ml in Brands vs 75ml in Image and notes.
