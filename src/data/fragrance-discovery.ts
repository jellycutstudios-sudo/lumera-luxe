/**
 * LUMÈRA LUXE · Fragrance Discovery Data & Layering Architecture
 * Master configuration for the 4-question personal consultation and curated layering pairs.
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
  explainer?: string;
  options: QuizOption[];
}

export interface QuizAnswers {
  fragranceFamily?: string;
  longevity?: string;
  sillage?: string;
  occasion?: string;
  // Backward compatibility fields
  scentPersona?: string;
  atmosphere?: string;
  intensity?: string;
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
    id: 'fragranceFamily',
    number: 1,
    title: 'Which fragrance family do you prefer?',
    subtitle: 'Step 1 of 4 · Fragrance Family',
    options: [
      { id: 'fresh', label: 'Fresh & Citrus', subtitle: 'Crisp bergamot, zesty lemon, sea breeze, and uplifting green botanicals' },
      { id: 'floral', label: 'Floral & Romantic', subtitle: 'Grasse rose, luminous jasmine, delicate white petals, and powdery blossoms' },
      { id: 'gourmand', label: 'Sweet & Gourmand', subtitle: 'Velvety Madagascar vanilla, warm roasted tonka, and golden praline' },
      { id: 'woody_amber', label: 'Woody & Amber', subtitle: 'Royal agarwood oud, sacred frankincense, dark cedar, and amber warmth' }
    ]
  },
  {
    id: 'longevity',
    number: 2,
    title: 'How long would you like your fragrance to last?',
    subtitle: 'Step 2 of 4 · Desired Longevity',
    options: [
      { id: 'light', label: 'Light (a few hours is fine)', subtitle: '2–4 hours of subtle, delicate refreshment' },
      { id: 'moderate', label: 'Moderate', subtitle: '5–7 hours of graceful, balanced presence' },
      { id: 'long_lasting', label: 'Long-lasting', subtitle: '8+ hours that endure from morning through evening' },
      { id: 'no_preference', label: 'No preference', subtitle: 'Neutral — open to any lasting profile' }
    ]
  },
  {
    id: 'sillage',
    number: 3,
    title: 'How noticeable should your fragrance be?',
    subtitle: 'Step 3 of 4 · Scent Trail (Sillage)',
    explainer: 'Sillage (pronounced see-yahzh) refers to how far a fragrance’s scent travels in the air around you.',
    options: [
      { id: 'subtle', label: 'Subtle: stays close to the skin', subtitle: 'An intimate whisper noticed only in close embrace' },
      { id: 'moderate', label: 'Moderate: noticeable nearby', subtitle: 'An inviting aura easily perceptible within arm’s length' },
      { id: 'strong', label: 'Strong: leaves a noticeable scent trail', subtitle: 'A commanding presence that projects and lingers in the room' },
      { id: 'no_preference', label: 'No preference', subtitle: 'Neutral — open to any projection level' }
    ]
  },
  {
    id: 'occasion',
    number: 4,
    title: 'When will you mainly wear it?',
    subtitle: 'Step 4 of 4 · Occasion Suitability',
    options: [
      { id: 'everyday_office', label: 'Everyday / Office', subtitle: 'Polished, composed elegance for daily routines and workspace settings' },
      { id: 'casual', label: 'Casual Outings', subtitle: 'Effortless chic for coffee dates, weekend brunches, and relaxed moments' },
      { id: 'special_occasions', label: 'Special Occasions', subtitle: 'Regal gatherings, milestone celebrations, weddings, and banquets' },
      { id: 'evening_events', label: 'Evening / Events', subtitle: 'Magnetic evening allure for fine dining, soirées, and night-time celebrations' },
      { id: 'versatile', label: 'Versatile / Any Occasion', subtitle: 'An all-around signature flacon suited for any moment in Qatar' }
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
  const familyMap: Record<string, string> = {
    fresh: 'clean, uplifting citrus & botanical clarity',
    floral: 'graceful, tender floral poetry and romantic petals',
    gourmand: 'warm, velvety vanilla and golden gourmand sweetness',
    woody_amber: 'deep, magnetic royal oud, rich woods, and amber warmth',
    surprise: 'a multifaceted, adventurous discovery of haute parfumerie',
    comforting: 'warm, cocooning amber and vanilla sweetness',
    captivating: 'deep, magnetic royal oud and sacred spices'
  };

  const longevityMap: Record<string, string> = {
    light: 'a light, refreshing wear',
    moderate: 'a poised, moderate longevity',
    long_lasting: 'an enduring, long-lasting profile',
    no_preference: 'a versatile lasting presence'
  };

  const sillageMap: Record<string, string> = {
    subtle: 'an intimate, skin-close whisper',
    moderate: 'a graceful, arm’s-length aura',
    strong: 'a commanding, head-turning scent trail',
    no_preference: 'a harmoniously balanced sillage',
    balanced: 'a graceful, head-turning aura',
    expressive: 'a rich, commanding sillage',
    variety: 'a multifaceted, versatile sillage'
  };

  const occasionMap: Record<string, string> = {
    everyday_office: 'daily signature moments and polished professional settings',
    casual: 'casual outings and relaxed weekend gatherings',
    special_occasions: 'milestone celebrations, weddings, and regal galas',
    evening_events: 'glamorous late dinners and magnetic soirées',
    versatile: 'any refined occasion across Doha',
    everyday: 'daily signature moments',
    office: 'polished professional settings',
    special: 'milestone celebrations and weddings',
    evenings: 'glamorous late dinners and soirées'
  };

  const familyKey = answers.fragranceFamily || answers.scentPersona || answers.scentImpression || 'surprise';
  const familyText = familyMap[familyKey] || 'timeless distinction';
  const longevityText = longevityMap[answers.longevity || ''] || 'an enduring presence';
  const sillageKey = answers.sillage || answers.intensity || 'no_preference';
  const sillageText = sillageMap[sillageKey] || 'a harmoniously balanced aura';
  const occasionKey = answers.occasion || answers.lifestyle || 'versatile';
  const occasionText = occasionMap[occasionKey] || 'any refined occasion in Qatar';

  return `Curated for ${occasionText}, your bespoke olfactory wardrobe embraces ${familyText}. Balanced with ${longevityText} and ${sillageText}, these flacons unfold seamlessly—crafted to feel enduring, intimate, and unmistakably yours in Qatar.`;
}
