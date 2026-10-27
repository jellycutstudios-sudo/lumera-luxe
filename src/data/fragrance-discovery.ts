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
  personality?: string;
  jewelry?: string;
  atmosphere?: string;
  scentImpression?: string;
  lifestyle?: string;
  intensity?: string;
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
    id: 'personality',
    number: 1,
    title: 'How would you describe your personal style?',
    subtitle: 'Step 1 of 6 · Personal Style',
    options: [
      { id: 'romantic', label: 'Soft & Romantic', subtitle: 'Graceful, gentle, and drawn to timeless beauty' },
      { id: 'bold', label: 'Confident & Bold', subtitle: 'Unapologetic, distinctive, and presence-driven' },
      { id: 'elegant', label: 'Calm & Elegant', subtitle: 'Understated, composed, and effortlessly refined' },
      { id: 'adventurous', label: 'Playful & Adventurous', subtitle: 'Vibrant, curious, and full of spirited warmth' }
    ]
  },
  {
    id: 'jewelry',
    number: 2,
    title: 'Which jewelry feels most like you?',
    subtitle: 'Step 2 of 6 · Styling Nuance',
    options: [
      { id: 'gold', label: 'Gold — Warm & Timeless', subtitle: 'Luminous glow, warm yellow and rose gold tones' },
      { id: 'silver', label: 'Silver — Cool & Modern', subtitle: 'Crisp platinum, white gold, and sleek minimalist lines' },
      { id: 'both', label: 'Both — A Little of Everything', subtitle: 'Fluid versatility mixing warm and cool metals' },
      { id: 'neither', label: 'Neither — Effortlessly Minimal', subtitle: 'Bare skin, uncluttered simplicity, pure natural comfort' }
    ]
  },
  {
    id: 'atmosphere',
    number: 3,
    title: 'Where do you feel most like yourself?',
    subtitle: 'Step 3 of 6 · Preferred Atmosphere',
    options: [
      { id: 'garden', label: 'A Garden in Bloom', subtitle: 'Dewy petals, lush greenery, and morning blossoms' },
      { id: 'coastal', label: 'A Sunny Coastal Escape', subtitle: 'Crisp sea breezes, bright sunshine, and mineral air' },
      { id: 'cozy', label: 'A Cozy Evening', subtitle: 'Warm cashmere, soft candlelight, and rich comforting sweetness' },
      { id: 'night_out', label: 'An Elegant Night Out', subtitle: 'Low ambient lighting, opulent ambiance, and magnetic evening allure' }
    ]
  },
  {
    id: 'scentImpression',
    number: 4,
    title: 'What would you love your fragrance to express?',
    subtitle: 'Step 4 of 6 · Scent Impression',
    options: [
      { id: 'fresh', label: 'Fresh & Clean', subtitle: 'Invigorating citrus, sparkling air, and pristine linen accords' },
      { id: 'feminine', label: 'Soft & Feminine', subtitle: 'Delicate petals, romantic rose, and powdery floral elegance' },
      { id: 'comforting', label: 'Warm & Comforting', subtitle: 'Velvety vanilla, golden amber, and soothing tonka bean' },
      { id: 'captivating', label: 'Bold & Captivating', subtitle: 'Precious oud wood, smoky incense, and dark oriental spices' }
    ]
  },
  {
    id: 'lifestyle',
    number: 5,
    title: 'When do you usually wear perfume?',
    subtitle: 'Step 5 of 6 · Occasion & Routine',
    options: [
      { id: 'everyday', label: 'Everyday Moments', subtitle: 'A welcoming signature for coffee, errands, and daily rituals' },
      { id: 'office', label: 'Work & Professional Spaces', subtitle: 'Polished, well-mannered, and tastefully close to the skin' },
      { id: 'special', label: 'Special Occasions', subtitle: 'Weddings, celebratory milestones, and memorable gatherings' },
      { id: 'evenings', label: 'Evenings Out', subtitle: 'Late dinners, gala evenings, and intimate gatherings' }
    ]
  },
  {
    id: 'intensity',
    number: 6,
    title: 'How would you like your fragrance to feel?',
    subtitle: 'Step 6 of 6 · Desired Intensity',
    options: [
      { id: 'subtle', label: 'Soft & Subtle', subtitle: 'An intimate skin scent noticed only in close embrace' },
      { id: 'balanced', label: 'Balanced & Noticeable', subtitle: 'A graceful sillage that turns heads without overwhelming' },
      { id: 'expressive', label: 'Bold & Expressive', subtitle: 'A commanding, unforgettable trail that announces your arrival' },
      { id: 'variety', label: 'I Love Variety', subtitle: 'Flexible and open to experiencing different sillage weights' }
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
  const styleMap: Record<string, string> = {
    romantic: 'a soft, romantic style',
    bold: 'a confident, presence-driven aesthetic',
    elegant: 'a calm, composed elegance',
    adventurous: 'a vibrant, spirited personality'
  };

  const atmosphereMap: Record<string, string> = {
    garden: 'morning floral gardens in bloom',
    coastal: 'the crisp serenity of coastal escapes',
    cozy: 'the intimate comfort of warm evenings',
    night_out: 'the opulent glamour of elegant nights'
  };

  const jewelryMap: Record<string, string> = {
    gold: 'warm, timeless gold accents',
    silver: 'cool, contemporary silver minimalism',
    both: 'a versatile love of mixed fine metals',
    neither: 'effortless, unadorned simplicity'
  };

  const impressionMap: Record<string, string> = {
    fresh: 'clean, uplifting clarity',
    feminine: 'graceful, tender floral poetry',
    comforting: 'warm, cocooning sweetness',
    captivating: 'deep, unforgettable magnetic presence'
  };

  const styleText = styleMap[answers.personality || ''] || 'a refined personal style';
  const jewelryText = jewelryMap[answers.jewelry || ''] || 'understated sophistication';
  const atmosphereText = atmosphereMap[answers.atmosphere || ''] || 'moments of beauty';
  const impressionText = impressionMap[answers.scentImpression || ''] || 'timeless distinction';

  return `You embody ${styleText} complemented by ${jewelryText}. Drawn to ${atmosphereText}, your ideal signature flacon unfolds with ${impressionText}—crafted to feel intimate, enduring, and effortlessly yours.`;
}
