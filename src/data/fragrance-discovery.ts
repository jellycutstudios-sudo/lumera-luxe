/**
 * LUMÈRA LUXE · Fragrance Discovery Data & Layering Architecture
 * Master configuration for the 6-question personal consultation and curated layering pairs.
 */

export interface QuizOption {
  id: string;
  label: string;
  subtitle?: string;
  icon?: string;
}

export interface QuizQuestion {
  id: string;
  number: number;
  title: string;
  subtitle: string;
  options: QuizOption[];
}

export interface QuizAnswers {
  scentPersona?: string;
  atmosphere?: string;
  occasion?: string;
  intensity?: string;
  // Backward compatibility fields
  personality?: string;
  jewelry?: string;
  scentImpression?: string;
  lifestyle?: string;
}

export interface LayeringPair {
  id: string;
  title: string;
  baseSlug: string;
  topSlug: string;
  description: string;
  ritualNote: string;
}

export const QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: 'scentPersona',
    number: 1,
    title: 'What scent profile speaks to you most?',
    subtitle: 'Step 1 of 4 · Scent Persona',
    options: [
      { id: 'fresh', label: 'Fresh, Crisp & Uplifting', subtitle: 'Sparkling Italian citrus, invigorating sea air, and clean crisp linen' },
      { id: 'floral', label: 'Soft & Romantic Floral', subtitle: 'Delicate Grasse rose, luminous jasmine, and tender powdery petals' },
      { id: 'comforting', label: 'Warm, Sweet & Comforting', subtitle: 'Velvety Madagascar vanilla, golden amber, and roasted tonka bean' },
      { id: 'captivating', label: 'Bold, Smoky & Captivating', subtitle: 'Royal agarwood oud, sacred frankincense, dark leather, and spices' }
    ]
  },
  {
    id: 'atmosphere',
    number: 2,
    title: 'Where do you feel most inspired?',
    subtitle: 'Step 2 of 4 · Preferred Atmosphere',
    options: [
      { id: 'garden', label: 'A Blooming Royal Garden', subtitle: 'Dewy petals, green botanicals, and sun-warmed blossoms' },
      { id: 'coastal', label: 'A Sunlit Coastal Escape', subtitle: 'Salty sea breeze, azure Mediterranean waters, and open mineral air' },
      { id: 'cozy', label: 'A Warm, Intimate Evening', subtitle: 'Soft cashmere, flickering candlelight, and cocooning sweetness' },
      { id: 'night_out', label: 'An Opulent Night in Doha', subtitle: 'Gilded ballrooms, ambient low lighting, and magnetic evening allure' }
    ]
  },
  {
    id: 'occasion',
    number: 3,
    title: 'When will you reach for this flacon?',
    subtitle: 'Step 3 of 4 · Occasion & Routine',
    options: [
      { id: 'everyday', label: 'Everyday Signature & Coffee', subtitle: 'An effortless daily luxury for mornings, work routines, and casual chic moments' },
      { id: 'office', label: 'Polished Professional Spaces', subtitle: 'Sophisticated, composed, and tastefully tailored close to the skin' },
      { id: 'special', label: 'Weddings & Milestone Celebrations', subtitle: 'Regal gatherings, celebratory moments, and unforgettable impressions' },
      { id: 'evenings', label: 'Glamorous Evenings & Late Dinners', subtitle: 'Intimate dinners, lounge soirées, and magnetic night-time allure' }
    ]
  },
  {
    id: 'intensity',
    number: 4,
    title: 'How would you like your presence felt?',
    subtitle: 'Step 4 of 4 · Desired Presence',
    options: [
      { id: 'subtle', label: 'Soft & Intimate', subtitle: 'A gentle, skin-close whisper noticed only in close embrace' },
      { id: 'balanced', label: 'Balanced & Noticeable', subtitle: 'A graceful aura that turns heads with effortless composure' },
      { id: 'expressive', label: 'Bold & Expressive', subtitle: 'A rich, commanding trail that announces your arrival and lingers beautifully' },
      { id: 'variety', label: 'Open to Discovery', subtitle: 'Versatile and curious to experience different projection weights' }
    ]
  }
];

/**
 * Curated Fragrance Layering Combinations (Up to 5 verified pairings).
 * Referenced by slug to guarantee data integrity with products.json.
 */
export const CURATED_LAYERING_PAIRS: LayeringPair[] = [
  {
    id: 'pair-rose-amber',
    title: 'Velvet Rose & Golden Amber',
    baseSlug: 'boucheron-ambre-d-alexandrie',
    topSlug: 'dior-miss-dior',
    description: 'A sumptuous dialogue between regal Grasse rose and warm, honeyed Alexandrian amber. The airy floral top notes float effortlessly over a deep, golden resinous base.',
    ritualNote: 'Apply the warm base of Ambre d’Alexandrie to pulse points first, then mist Miss Dior lightly across your collarbones and scarf.'
  },
  {
    id: 'pair-citrus-oud',
    title: 'Mineral Citrus & Royal Oud',
    baseSlug: 'chopard-oud-malaki',
    topSlug: 'herm-s-eau-des-merveilles',
    description: 'Sparkling Italian orange and mineral elemi resin cast a crystalline radiance over the dark, smoky tobacco and oud heart of Chopard Oud Malaki.',
    ritualNote: 'Spray Oud Malaki on wrists and behind the ears, then veil your aura with two sprays of Eau des Merveilles.'
  },
  {
    id: 'pair-orchid-incense',
    title: 'Midnight Orchid & Sacred Incense',
    baseSlug: 'chopard-black-incense-malaki',
    topSlug: 'tom-ford-velvet-orchid',
    description: 'Black Incense Malaki provides a brooding, sacred Somalian frankincense foundation that elevates the sweet honeyed rum and black orchid nectar of Tom Ford into pure mystique.',
    ritualNote: 'A striking evening ritual: apply one measured spray of Black Incense to the nape of the neck and layer Velvet Orchid along pulse points.'
  },
  {
    id: 'pair-aldehydic-patchouli',
    title: 'Haute Aldehydes & Sacred Woods',
    baseSlug: 'boucheron-patchouli-d-angkor',
    topSlug: 'chanel-n-5',
    description: 'The world’s most iconic golden aldehydic bouquet finds profound earthy grounding in noble Indonesian patchouli and sacred guaiac wood.',
    ritualNote: 'Mist Patchouli d’Angkor at the base of the throat, allowing the effervescent champagne aldehydes of N°5 to settle on top.'
  },
  {
    id: 'pair-solar-desert',
    title: 'Bahia Citrus & Desert Oud',
    baseSlug: 'dolce-and-gabbana-velvet-desert-oud',
    topSlug: 'boucheron-orange-de-bahia',
    description: 'A fascinating contrast of Brazilian sunshine and Middle Eastern warmth: crisp orange and lush green fig leaf temper the deep smoky amber and agarwood of Velvet Desert Oud.',
    ritualNote: 'An invigorating day-to-night layering pairing designed for discerning collectors in Doha.'
  },
  {
    id: 'pair-tonka-delina',
    title: 'Rose Nectar & Venezuelan Tonka',
    baseSlug: 'boucheron-feve-tonka-de-canaima',
    topSlug: 'parfums-de-marly-delina',
    description: 'The sensual Turkish rose and tart lychee nectar of Delina discover an intoxicating, velvety base in Venezuelan tonka bean and bitter almond.',
    ritualNote: 'Anchor your wrists with the warm almond and tonka of Fève Tonka de Canaima, then veil your décolletage with Delina’s radiant rose aura.'
  },
  {
    id: 'pair-leather-orange-blossom',
    title: 'Imperial Leather & Moroccan Blossom',
    baseSlug: 'guerlain-cuir-intense',
    topSlug: 'yves-saint-laurent-libre',
    description: 'A bold, majestic contrast where the noble Osmanthus and smoky bark leather of Cuir Intense meets the bright Moroccan orange blossom and diva lavender of Libre.',
    ritualNote: 'Spray one measured burst of Cuir Intense on the nape, then sweep Libre across your wrists and hair for an arresting, regal trail.'
  },
  {
    id: 'pair-carthage-tuberose',
    title: 'Carthage Honey Oud & Velvet Tuberose',
    baseSlug: 'boucheron-oud-de-carthage',
    topSlug: 'carolina-herrera-good-girl',
    description: 'Deep labdanum leather and dark honeyed oud establish a rich, royal throne for the luminous tuberose, roasted cocoa, and jasmine sambac of Good Girl.',
    ritualNote: 'Apply Oud de Carthage to pulse points at the throat, layering Good Girl on the wrists for an opulent, sensual sillage.'
  },
  {
    id: 'pair-white-musk-black-orchid',
    title: 'Crystalline White Musk & Midnight Orchid',
    baseSlug: 'tom-ford-black-orchid',
    topSlug: 'narciso-rodriguez-pure-musc',
    description: 'Pure Musc casts a soft, powdery cashmere veil over the dark truffles, black plum, and intoxicating patchouli of Black Orchid, creating an ethereal yet mysterious halo.',
    ritualNote: 'Mist Tom Ford Black Orchid onto the chest, then layer Pure Musc generously over arms and shoulders to soften and illuminate the fragrance trail.'
  },
  {
    id: 'pair-leather-citrus-rose',
    title: 'Smoky Leather & Luminous Mandarin',
    baseSlug: 'chopard-leather-malaki',
    topSlug: 'chanel-coco-mademoiselle',
    description: 'The noble cedarwood, warm amber, and smoked leather of Leather Malaki provide timeless architectural depth to Coco Mademoiselle’s sparkling orange and Grasse rose heart.',
    ritualNote: 'Apply Leather Malaki to lower pulse points, allowing Coco Mademoiselle to radiate with sparkling freshness up close.'
  }
];

/**
 * Deterministic personalized introduction template generator.
 * Combines style, atmosphere, and impression answers into natural, elegant prose without AI APIs.
 */
export function generatePersonalizedIntro(answers: QuizAnswers): string {
  const personaMap: Record<string, string> = {
    fresh: 'clean, uplifting citrus clarity',
    floral: 'graceful, tender floral poetry',
    comforting: 'warm, cocooning amber and vanilla sweetness',
    captivating: 'deep, magnetic royal oud and sacred spices'
  };

  const atmosphereMap: Record<string, string> = {
    garden: 'morning floral gardens in bloom',
    coastal: 'the crisp serenity of coastal escapes',
    cozy: 'the intimate warmth of candlelit evenings',
    night_out: 'the opulent glamour of Doha nights'
  };

  const occasionMap: Record<string, string> = {
    everyday: 'daily signature moments',
    office: 'polished professional settings',
    special: 'milestone celebrations and weddings',
    evenings: 'glamorous late dinners and soirées'
  };

  const intensityMap: Record<string, string> = {
    subtle: 'an intimate, skin-close whisper',
    balanced: 'a graceful, head-turning aura',
    expressive: 'a rich, commanding sillage',
    variety: 'a multifaceted, versatile sillage'
  };

  const personaText = personaMap[answers.scentPersona || answers.scentImpression || ''] || 'timeless distinction';
  const atmosphereText = atmosphereMap[answers.atmosphere || ''] || 'moments of beauty';
  const occasionText = occasionMap[answers.occasion || answers.lifestyle || ''] || 'any refined occasion';
  const intensityText = intensityMap[answers.intensity || ''] || 'a harmoniously balanced aura';

  return `Tailored for ${occasionText} and inspired by ${atmosphereText}, your olfactory persona celebrates ${personaText}. Finished with ${intensityText}, your matched flacons unfold seamlessly—crafted to feel enduring, intimate, and unmistakably yours in Qatar.`;
}
