/**
 * LUMÈRA LUXE · Fragrance Recommendation & Similarity Matcher
 * Pure, deterministic TypeScript recommendation engine. Zero external AI APIs.
 */

import type { QuizAnswers } from '../data/fragrance-discovery';

export interface ProductMatchRecord {
  id: string;
  slug: string;
  brand: string;
  name: string;
  fullName: string;
  category: string;
  scentFamilies: string[];
  keyNotes: string[];
  rawNotes?: string;
  description: string;
  concentration: string;
  sizeDisplay: string;
  priceMinor: number;
  priceDisplay: string;
  stickerPriceMinor?: number | null;
  image: string;
  isDraft?: boolean;
}

export interface ScoredRecommendation {
  product: ProductMatchRecord;
  score: number;
  reason: string;
}

export interface SimilarFragrance {
  product: ProductMatchRecord;
  similarityScore: number;
  sharedNotes: string[];
}

/**
 * Normalizes string for token matching
 */
function normalize(str: string): string {
  return str.toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
}

/**
 * Checks if any keyword appears in product's text fields
 */
function hasAnyKeyword(text: string, keywords: string[]): boolean {
  const normText = normalize(text);
  return keywords.some((kw) => normText.includes(normalize(kw)));
}

/**
 * Finds overlap between notes
 */
function getSharedNotes(notesA: string[], notesB: string[]): string[] {
  const normB = notesB.map(normalize);
  return notesA.filter((na) => normB.some((nb) => nb.includes(normalize(na)) || normalize(na).includes(nb)));
}

/**
 * Scores a product against the 6 quiz answers (Maximum 100 points).
 */
export function scoreProduct(product: ProductMatchRecord, answers: QuizAnswers): { score: number; reason: string } {
  let score = 0;
  const matchFactors: string[] = [];
  const allNotesText = `${product.keyNotes.join(' ')} ${product.rawNotes || ''} ${product.scentFamilies.join(' ')} ${product.description}`;
  const category = (product.category || '').toLowerCase();

  // 1. Q4: Scent Impression (Max 35 points - Primary Signal)
  const impression = answers.scentImpression;
  if (impression === 'fresh') {
    if (category === 'fresh' || product.scentFamilies.some((f) => /fresh|citrus|aquatic|green/i.test(f))) {
      score += 35;
      matchFactors.push('sparkling fresh clarity');
    } else if (hasAnyKeyword(allNotesText, ['citrus', 'bergamot', 'lemon', 'mandarin', 'tea', 'aquatic'])) {
      score += 24;
      matchFactors.push('clean citrus facets');
    }
  } else if (impression === 'feminine') {
    if (category === 'floral' || product.scentFamilies.some((f) => /floral|rose|violet|white floral/i.test(f))) {
      score += 35;
      matchFactors.push('delicate floral bouquet');
    } else if (hasAnyKeyword(allNotesText, ['rose', 'peony', 'jasmine', 'orange blossom', 'tuberose', 'magnolia'])) {
      score += 24;
      matchFactors.push('tender petal accords');
    }
  } else if (impression === 'comforting') {
    if (hasAnyKeyword(allNotesText, ['vanilla', 'tonka', 'amber', 'praline', 'honey', 'marshmallow', 'caramel', 'almond'])) {
      score += 35;
      matchFactors.push('warm, comforting gourmand vanilla');
    } else if (category === 'oriental' || product.scentFamilies.some((f) => /amber|oriental|gourmand/i.test(f))) {
      score += 25;
      matchFactors.push('soothing amber warmth');
    }
  } else if (impression === 'captivating') {
    if (hasAnyKeyword(allNotesText, ['oud', 'incense', 'leather', 'patchouli', 'saffron', 'tobacco', 'spices'])) {
      score += 35;
      matchFactors.push('magnetic oud and smoky incense');
    } else if (category === 'woody' || category === 'oriental') {
      score += 25;
      matchFactors.push('captivating depth');
    }
  }

  // 2. Q3: Atmosphere (Max 25 points - Contextual Environment)
  const atmosphere = answers.atmosphere;
  if (atmosphere === 'garden') {
    if (hasAnyKeyword(allNotesText, ['rose', 'peony', 'jasmine', 'violet', 'lily', 'neroli', 'freesia'])) {
      score += 25;
      matchFactors.push('blooming floral petals');
    }
  } else if (atmosphere === 'coastal') {
    if (hasAnyKeyword(allNotesText, ['marine', 'aquatic', 'bergamot', 'sea', 'citrus', 'mandarin', 'fig leaf', 'salt'])) {
      score += 25;
      matchFactors.push('sunny coastal breeze');
    }
  } else if (atmosphere === 'cozy') {
    if (hasAnyKeyword(allNotesText, ['vanilla', 'tonka bean', 'amber', 'cashmeran', 'musk', 'sandalwood'])) {
      score += 25;
      matchFactors.push('cozy ambery warmth');
    }
  } else if (atmosphere === 'night_out') {
    if (hasAnyKeyword(allNotesText, ['oud', 'leather', 'incense', 'patchouli', 'amber', 'black orchid', 'saffron', 'rum'])) {
      score += 25;
      matchFactors.push('glamorous evening richness');
    }
  }

  // 3. Q5: Lifestyle / Occasion (Max 15 points)
  const lifestyle = answers.lifestyle;
  if (lifestyle === 'everyday') {
    if (category === 'fresh' || category === 'floral' || hasAnyKeyword(allNotesText, ['sparkling', 'delicate', 'airy', 'mandarin', 'rose'])) {
      score += 15;
    }
  } else if (lifestyle === 'office') {
    if (hasAnyKeyword(allNotesText, ['clean', 'tea', 'iris', 'musk', 'cedar', 'subtle', 'peony'])) {
      score += 15;
    }
  } else if (lifestyle === 'special') {
    if (hasAnyKeyword(allNotesText, ['rose', 'jasmine', 'tuberose', 'parfum', 'amber', 'champagne'])) {
      score += 15;
    }
  } else if (lifestyle === 'evenings') {
    if (hasAnyKeyword(allNotesText, ['oud', 'intense', 'elixir', 'leather', 'incense', 'gourmand', 'amber'])) {
      score += 15;
    }
  }

  // 4. Q6: Intensity (Max 10 points)
  const intensity = answers.intensity;
  const isHeavyNotes = hasAnyKeyword(allNotesText, ['oud', 'incense', 'leather', 'patchouli', 'amber', 'elixir']);
  if (intensity === 'subtle') {
    if (!isHeavyNotes || product.concentration.includes('Toilette')) {
      score += 10;
    } else {
      score += 3;
    }
  } else if (intensity === 'expressive') {
    if (isHeavyNotes || product.concentration.includes('Parfum') || product.concentration.includes('Intense')) {
      score += 10;
    } else {
      score += 4;
    }
  } else {
    // balanced or variety: award steady baseline
    score += 8;
  }

  // 5. Q1: Personality (Max 10 points - Light Styling Signal)
  const personality = answers.personality;
  if (personality === 'romantic') {
    if (hasAnyKeyword(allNotesText, ['rose', 'peony', 'vanilla', 'sweet', 'blossom'])) score += 10;
  } else if (personality === 'bold') {
    if (hasAnyKeyword(allNotesText, ['oud', 'leather', 'spices', 'patchouli', 'intense'])) score += 10;
  } else if (personality === 'elegant') {
    if (hasAnyKeyword(allNotesText, ['iris', 'chypre', 'musk', 'sandalwood', 'cedar'])) score += 10;
  } else if (personality === 'adventurous') {
    if (hasAnyKeyword(allNotesText, ['citrus', 'blackcurrant', 'fig', 'pepper', 'exotic'])) score += 10;
  }

  // 6. Q2: Jewelry Preference (Max 5 points - Gentle Accent)
  const jewelry = answers.jewelry;
  if (jewelry === 'gold') {
    if (hasAnyKeyword(allNotesText, ['amber', 'vanilla', 'gold', 'honey', 'tonka', 'solar'])) {
      score += 5;
    } else {
      score += 2;
    }
  } else if (jewelry === 'silver') {
    if (hasAnyKeyword(allNotesText, ['musk', 'clean', 'citrus', 'tea', 'fresh', 'water', 'silver'])) {
      score += 5;
    } else {
      score += 2;
    }
  } else {
    // Both or Neither: Neutral points, never penalizes
    score += 3.5;
  }

  // Generate verified note-based reason
  const highlightNotes = product.keyNotes.slice(0, 3).join(', ');
  let reason = '';
  if (matchFactors.length > 0) {
    reason = `Chosen for its ${matchFactors.slice(0, 2).join(' and ')}, featuring notes of ${highlightNotes}.`;
  } else {
    reason = `Exquisite ${product.category} harmony featuring prominent notes of ${highlightNotes}.`;
  }

  return { score, reason };
}

/**
 * Finds top N recommendations from catalog for given quiz answers.
 * Guarantees brand diversity among the top recommendations.
 */
export function matchSignatureScents(
  catalog: ProductMatchRecord[],
  answers: QuizAnswers,
  limit = 3
): ScoredRecommendation[] {
  // Exclude drafts
  const activeProducts = catalog.filter((p) => !p.isDraft);

  // Score all
  const scored = activeProducts.map((p) => {
    const { score, reason } = scoreProduct(p, answers);
    return {
      product: p,
      score,
      reason
    };
  });

  // Sort by score descending
  scored.sort((a, b) => b.score - a.score);

  // Enforce brand diversity: maximum 1 product per brand in recommendations
  const chosen: ScoredRecommendation[] = [];
  const chosenBrands = new Set<string>();

  for (const item of scored) {
    if (!chosenBrands.has(item.product.brand)) {
      chosen.push(item);
      chosenBrands.add(item.product.brand);
      if (chosen.length >= limit) break;
    }
  }

  // Fallback if not enough distinct brands
  if (chosen.length < limit) {
    for (const item of scored) {
      if (!chosen.some((c) => c.product.id === item.product.id)) {
        chosen.push(item);
        if (chosen.length >= limit) break;
      }
    }
  }

  return chosen.slice(0, limit);
}

/**
 * Recommends 2-3 genuine similar fragrances for PDP "If You Love This, Try These"
 * Compares shared scent families and key notes.
 * Suppressed if no reliable olfactive overlap exists.
 */
export function findSimilarFragrances(
  targetProduct: ProductMatchRecord,
  allProducts: ProductMatchRecord[],
  limit = 3
): SimilarFragrance[] {
  const candidates = allProducts.filter(
    (p) => p.id !== targetProduct.id && !p.isDraft
  );

  const scoredSimilar = candidates
    .map((candidate) => {
      let similarityScore = 0;

      // Note overlap
      const sharedNotes = getSharedNotes(targetProduct.keyNotes, candidate.keyNotes);
      similarityScore += sharedNotes.length * 15;

      // Scent family overlap
      const sharedFamilies = targetProduct.scentFamilies.filter((f) =>
        candidate.scentFamilies.some((cf) => cf.toLowerCase() === f.toLowerCase())
      );
      similarityScore += sharedFamilies.length * 20;

      // Same category bonus
      if (targetProduct.category && candidate.category && targetProduct.category === candidate.category) {
        similarityScore += 10;
      }

      // Small penalty if same brand (encourage discovery of true olfactive alternatives)
      if (candidate.brand === targetProduct.brand) {
        similarityScore -= 5;
      }

      return {
        product: candidate,
        similarityScore,
        sharedNotes
      };
    })
    // Quality threshold: must have at least 20 points (e.g. shared family or multiple shared notes)
    .filter((res) => res.similarityScore >= 20);

  scoredSimilar.sort((a, b) => b.similarityScore - a.similarityScore);

  return scoredSimilar.slice(0, limit);
}
