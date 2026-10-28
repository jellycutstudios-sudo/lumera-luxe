/**
 * LUMÈRA LUXE · Verified Perfume Consultation Metadata
 * Maintainable local product metadata structure storing verified olfactory profiles,
 * longevity ratings, sillage characteristics, and occasion suitabilities.
 *
 * Rules:
 * - Only verified ratings from perfume consensus / manufacturer profiles are marked `verified: true`.
 * - Unknown or unverified ratings are marked `longevity: 'unknown'`, `sillage: 'unknown'`, `verified: false`, and `reviewFlag: true`.
 * - Never fabricate longevity or sillage data based solely on EDP/EDT concentration.
 */

export type LongevityRating = 'light' | 'moderate' | 'long_lasting' | 'unknown';
export type SillageRating = 'subtle' | 'moderate' | 'strong' | 'unknown';
export type FragranceFamily = 'fresh' | 'floral' | 'gourmand' | 'woody_amber';
export type OccasionKey = 'everyday_office' | 'casual' | 'special_occasions' | 'evening_events' | 'versatile';

export interface PerfumeMetadata {
  slug: string;
  primaryFamily: FragranceFamily;
  secondaryFamilies?: FragranceFamily[];
  longevity: LongevityRating;
  sillage: SillageRating;
  occasions: OccasionKey[];
  verified: boolean;
  reviewFlag?: boolean;
}

/**
 * Display labels for UI rendering
 */
export const FAMILY_DISPLAY_LABELS: Record<FragranceFamily, string> = {
  fresh: 'Fresh & Citrus',
  floral: 'Floral & Romantic',
  gourmand: 'Sweet & Gourmand',
  woody_amber: 'Woody & Amber'
};

export const LONGEVITY_DISPLAY_LABELS: Record<LongevityRating, string> = {
  light: 'Light (2–4 hrs)',
  moderate: 'Moderate (5–7 hrs)',
  long_lasting: 'Long-lasting (8+ hrs)',
  unknown: 'Not Specified'
};

export const SILLAGE_DISPLAY_LABELS: Record<SillageRating, string> = {
  subtle: 'Subtle (skin-close)',
  moderate: 'Moderate (arm’s length)',
  strong: 'Strong (scent trail)',
  unknown: 'Not Specified'
};

export const OCCASION_DISPLAY_LABELS: Record<OccasionKey, string> = {
  everyday_office: 'Everyday / Office',
  casual: 'Casual Outings',
  special_occasions: 'Special Occasions',
  evening_events: 'Evening / Events',
  versatile: 'Versatile / Any Occasion'
};

/**
 * Verified metadata dictionary keyed by perfume slug.
 */
export const VERIFIED_PERFUME_METADATA: Record<string, PerfumeMetadata> = {
  // ==========================================
  // FRESH & CITRUS
  // ==========================================
  'dolce-and-gabbana-light-blue': {
    slug: 'dolce-and-gabbana-light-blue',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual', 'versatile'],
    verified: true
  },
  'herm-s-un-jardin-sur-le-nil': {
    slug: 'herm-s-un-jardin-sur-le-nil',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'chanel-chance-eau-fra-che': {
    slug: 'chanel-chance-eau-fra-che',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual', 'versatile'],
    verified: true
  },
  'boucheron-quatre-en-bleu': {
    slug: 'boucheron-quatre-en-bleu',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'boucheron-orange-de-bahia': {
    slug: 'boucheron-orange-de-bahia',
    primaryFamily: 'fresh',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['casual', 'versatile', 'special_occasions'],
    verified: true
  },
  'guerlain-aqua-allegoria-pamplelune': {
    slug: 'guerlain-aqua-allegoria-pamplelune',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'versace-versense': {
    slug: 'versace-versense',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'versace-dylan-turquoise': {
    slug: 'versace-dylan-turquoise',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'giorgio-armani-acqua-di-gioia': {
    slug: 'giorgio-armani-acqua-di-gioia',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'donna-karan-be-delicious': {
    slug: 'donna-karan-be-delicious',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'marc-jacobs-daisy-eau-so-fresh': {
    slug: 'marc-jacobs-daisy-eau-so-fresh',
    primaryFamily: 'fresh',
    secondaryFamilies: ['floral'],
    longevity: 'light',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'herm-s-un-jardin-cyth-re': {
    slug: 'herm-s-un-jardin-cyth-re',
    primaryFamily: 'fresh',
    secondaryFamilies: ['woody_amber'],
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'versatile'],
    verified: true
  },
  'dolce-and-gabbana-dolce-shine': {
    slug: 'dolce-and-gabbana-dolce-shine',
    primaryFamily: 'fresh',
    secondaryFamilies: ['floral'],
    longevity: 'light',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'chanel-chance-eau-tendre': {
    slug: 'chanel-chance-eau-tendre',
    primaryFamily: 'fresh',
    secondaryFamilies: ['floral'],
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual', 'versatile'],
    verified: true
  },

  // ==========================================
  // FLORAL & ROMANTIC
  // ==========================================
  'parfums-de-marly-delina': {
    slug: 'parfums-de-marly-delina',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events', 'versatile'],
    verified: true
  },
  'parfums-de-marly-delina-exclusif': {
    slug: 'parfums-de-marly-delina-exclusif',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  },
  'chanel-n-5': {
    slug: 'chanel-n-5',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  },
  'dior-miss-dior': {
    slug: 'dior-miss-dior',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'special_occasions', 'versatile'],
    verified: true
  },
  'chlo-chlo-eau-de-parfum': {
    slug: 'chlo-chlo-eau-de-parfum',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual', 'versatile'],
    verified: true
  },
  'chlo-love-story': {
    slug: 'chlo-love-story',
    primaryFamily: 'floral',
    secondaryFamilies: ['fresh'],
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'bvlgari-omnia-amethyste': {
    slug: 'bvlgari-omnia-amethyste',
    primaryFamily: 'floral',
    longevity: 'moderate',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'bvlgari-rose-goldea': {
    slug: 'bvlgari-rose-goldea',
    primaryFamily: 'floral',
    longevity: 'moderate',
    sillage: 'subtle',
    occasions: ['everyday_office', 'special_occasions'],
    verified: true
  },
  'lanc-me-idole': {
    slug: 'lanc-me-idole',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'subtle',
    occasions: ['everyday_office', 'versatile'],
    verified: true
  },
  'guerlain-idylle': {
    slug: 'guerlain-idylle',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'subtle',
    occasions: ['everyday_office', 'special_occasions'],
    verified: true
  },
  'givenchy-l-interdit': {
    slug: 'givenchy-l-interdit',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  },
  'elie-saab-le-parfum': {
    slug: 'elie-saab-le-parfum',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  },
  'versace-bright-crystal-absolu': {
    slug: 'versace-bright-crystal-absolu',
    primaryFamily: 'floral',
    secondaryFamilies: ['fresh'],
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'versatile'],
    verified: true
  },
  'marc-jacobs-daisy': {
    slug: 'marc-jacobs-daisy',
    primaryFamily: 'floral',
    secondaryFamilies: ['fresh'],
    longevity: 'light',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'narciso-rodriguez-fleur-musc': {
    slug: 'narciso-rodriguez-fleur-musc',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'versatile'],
    verified: true
  },
  'chanel-gabrielle': {
    slug: 'chanel-gabrielle',
    primaryFamily: 'floral',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'special_occasions', 'versatile'],
    verified: true
  },
  'gucci-flora-gorgeous-gardenia-intense': {
    slug: 'gucci-flora-gorgeous-gardenia-intense',
    primaryFamily: 'floral',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'gucci-flora-gorgeous-magnolia': {
    slug: 'gucci-flora-gorgeous-magnolia',
    primaryFamily: 'floral',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'tom-ford-caf-rose': {
    slug: 'tom-ford-caf-rose',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'chanel-coco-mademoiselle': {
    slug: 'chanel-coco-mademoiselle',
    primaryFamily: 'floral',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'special_occasions', 'versatile'],
    verified: true
  },
  'yves-saint-laurent-libre': {
    slug: 'yves-saint-laurent-libre',
    primaryFamily: 'floral',
    secondaryFamilies: ['gourmand', 'woody_amber'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['versatile', 'special_occasions', 'evening_events'],
    verified: true
  },

  // ==========================================
  // SWEET & GOURMAND
  // ==========================================
  'carolina-herrera-good-girl': {
    slug: 'carolina-herrera-good-girl',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'carolina-herrera-good-girl-blush': {
    slug: 'carolina-herrera-good-girl-blush',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['versatile', 'evening_events'],
    verified: true
  },
  'yves-saint-laurent-black-opium': {
    slug: 'yves-saint-laurent-black-opium',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'lanc-me-la-vie-est-belle': {
    slug: 'lanc-me-la-vie-est-belle',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events', 'casual'],
    verified: true
  },
  'jean-paul-gaultier-scandal': {
    slug: 'jean-paul-gaultier-scandal',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'jean-paul-gaultier-la-belle': {
    slug: 'jean-paul-gaultier-la-belle',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'burberry-burberry-goddess': {
    slug: 'burberry-burberry-goddess',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'versatile', 'evening_events'],
    verified: true
  },
  'dolce-gabbana-devotion': {
    slug: 'dolce-gabbana-devotion',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['fresh'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['casual', 'versatile', 'evening_events'],
    verified: true
  },
  'dolce-gabbana-the-one': {
    slug: 'dolce-gabbana-the-one',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'viktor-and-rolf-flowerbomb': {
    slug: 'viktor-and-rolf-flowerbomb',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'ariana-grande-cloud': {
    slug: 'ariana-grande-cloud',
    primaryFamily: 'gourmand',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'ariana-grande-sweet-like-candy': {
    slug: 'ariana-grande-sweet-like-candy',
    primaryFamily: 'gourmand',
    longevity: 'light',
    sillage: 'subtle',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'boucheron-feve-tonka-de-canaima': {
    slug: 'boucheron-feve-tonka-de-canaima',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['woody_amber'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'prada-paradoxe': {
    slug: 'prada-paradoxe',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['versatile', 'everyday_office', 'special_occasions'],
    verified: true
  },
  'paco-rabanne-olymp-a': {
    slug: 'paco-rabanne-olymp-a',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['casual', 'evening_events'],
    verified: true
  },
  'elie-saab-girl-of-now': {
    slug: 'elie-saab-girl-of-now',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },

  // ==========================================
  // WOODY & AMBER
  // ==========================================
  'tom-ford-black-orchid': {
    slug: 'tom-ford-black-orchid',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'chopard-oud-malaki': {
    slug: 'chopard-oud-malaki',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'chopard-black-incense-malaki': {
    slug: 'chopard-black-incense-malaki',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'chopard-leather-malaki': {
    slug: 'chopard-leather-malaki',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'boucheron-ambre-d-alexandrie': {
    slug: 'boucheron-ambre-d-alexandrie',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['gourmand'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'boucheron-oud-de-carthage': {
    slug: 'boucheron-oud-de-carthage',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'boucheron-patchouli-d-angkor': {
    slug: 'boucheron-patchouli-d-angkor',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['special_occasions', 'versatile'],
    verified: true
  },
  'guerlain-cuir-intense': {
    slug: 'guerlain-cuir-intense',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'guerlain-patchouli-ardent': {
    slug: 'guerlain-patchouli-ardent',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'narciso-rodriguez-pure-musc': {
    slug: 'narciso-rodriguez-pure-musc',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'subtle',
    occasions: ['everyday_office', 'versatile'],
    verified: true
  },
  'narciso-rodriguez-for-her': {
    slug: 'narciso-rodriguez-for-her',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'evening_events', 'versatile'],
    verified: true
  },
  'herm-s-eau-des-merveilles': {
    slug: 'herm-s-eau-des-merveilles',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['fresh'],
    longevity: 'moderate',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'chlo-nomade': {
    slug: 'chlo-nomade',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office', 'versatile'],
    verified: true
  },
  'dolce-and-gabbana-velvet-desert-oud': {
    slug: 'dolce-and-gabbana-velvet-desert-oud',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'tom-ford-noir-extreme': {
    slug: 'tom-ford-noir-extreme',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['gourmand'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'tom-ford-velvet-orchid': {
    slug: 'tom-ford-velvet-orchid',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'versace-crystal-noir': {
    slug: 'versace-crystal-noir',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'givenchy-l-interdit-rouge': {
    slug: 'givenchy-l-interdit-rouge',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'cartier-la-panth-re': {
    slug: 'cartier-la-panth-re',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['special_occasions', 'everyday_office'],
    verified: true
  },
  'calvin-klein-euphoria': {
    slug: 'calvin-klein-euphoria',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'casual'],
    verified: true
  },
  'parfums-de-marly-valaya': {
    slug: 'parfums-de-marly-valaya',
    primaryFamily: 'fresh',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'versatile'],
    verified: true
  },
  'dolce-and-gabbana-l-imp-ratrice': {
    slug: 'dolce-and-gabbana-l-imp-ratrice',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'versace-bright-crystal': {
    slug: 'versace-bright-crystal',
    primaryFamily: 'fresh',
    secondaryFamilies: ['floral'],
    longevity: 'light',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'bvlgari-omnia-crystalline': {
    slug: 'bvlgari-omnia-crystalline',
    primaryFamily: 'fresh',
    longevity: 'moderate',
    sillage: 'subtle',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'moschino-toy-2': {
    slug: 'moschino-toy-2',
    primaryFamily: 'fresh',
    secondaryFamilies: ['floral'],
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['everyday_office', 'casual'],
    verified: true
  },
  'dior-j-adore': {
    slug: 'dior-j-adore',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['special_occasions', 'versatile'],
    verified: true
  },
  'gucci-bloom': {
    slug: 'gucci-bloom',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'versatile'],
    verified: true
  },
  'gucci-flora-gorgeous-gardenia': {
    slug: 'gucci-flora-gorgeous-gardenia',
    primaryFamily: 'floral',
    longevity: 'moderate',
    sillage: 'moderate',
    occasions: ['casual', 'everyday_office'],
    verified: true
  },
  'giorgio-armani-my-way': {
    slug: 'giorgio-armani-my-way',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'versatile'],
    verified: true
  },
  'giorgio-armani-my-way-intense': {
    slug: 'giorgio-armani-my-way-intense',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'guerlain-insolence': {
    slug: 'guerlain-insolence',
    primaryFamily: 'floral',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  },
  'dior-pure-poison': {
    slug: 'dior-pure-poison',
    primaryFamily: 'gourmand',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'mugler-alien-goddess': {
    slug: 'mugler-alien-goddess',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'mugler-angel-elixir': {
    slug: 'mugler-angel-elixir',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'jean-paul-gaultier-scandal-le-parfum': {
    slug: 'jean-paul-gaultier-scandal-le-parfum',
    primaryFamily: 'gourmand',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'guerlain-samsara': {
    slug: 'guerlain-samsara',
    primaryFamily: 'woody_amber',
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  },
  'guerlain-mon-guerlain': {
    slug: 'guerlain-mon-guerlain',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'moderate',
    occasions: ['everyday_office', 'versatile'],
    verified: true
  },
  'burberry-my-burberry-black': {
    slug: 'burberry-my-burberry-black',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'givenchy-l-interdit-eau-de-parfum-intense': {
    slug: 'givenchy-l-interdit-eau-de-parfum-intense',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['evening_events', 'special_occasions'],
    verified: true
  },
  'elie-saab-le-parfum-royal': {
    slug: 'elie-saab-le-parfum-royal',
    primaryFamily: 'woody_amber',
    secondaryFamilies: ['floral'],
    longevity: 'long_lasting',
    sillage: 'strong',
    occasions: ['special_occasions', 'evening_events'],
    verified: true
  }
};

/**
 * Returns verified or conservative fallback metadata for any product in the catalog.
 * Missing metadata is marked 'unknown' and flagged for review.
 * Never invents longevity or sillage ratings.
 */
export function getPerfumeMetadata(product: {
  slug?: string;
  category?: string;
  scentFamilies?: string[];
  keyNotes?: string[];
  description?: string;
}): PerfumeMetadata {
  const slug = product.slug || '';
  if (slug && VERIFIED_PERFUME_METADATA[slug]) {
    return VERIFIED_PERFUME_METADATA[slug];
  }

  // Deduce family from category and scentFamilies
  const cat = (product.category || '').toLowerCase();
  const families = (product.scentFamilies || []).join(' ').toLowerCase();

  let primaryFamily: FragranceFamily = 'floral';
  if (cat === 'fresh' || /fresh|citrus|aquatic|green/i.test(families)) {
    primaryFamily = 'fresh';
  } else if (cat === 'floral' || /floral|rose|violet|jasmine/i.test(families)) {
    primaryFamily = 'floral';
  } else if (/gourmand|vanilla|tonka|praline|caramel/i.test(families)) {
    primaryFamily = 'gourmand';
  } else if (cat === 'woody' || cat === 'oriental' || /woody|amber|oud|incense|leather/i.test(families)) {
    primaryFamily = 'woody_amber';
  }

  // Missing longevity and sillage are marked 'unknown' and flagged for review
  return {
    slug,
    primaryFamily,
    longevity: 'unknown',
    sillage: 'unknown',
    occasions: ['versatile'],
    verified: false,
    reviewFlag: true
  };
}
