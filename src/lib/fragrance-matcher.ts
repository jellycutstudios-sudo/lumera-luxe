/**
 * LUMÈRA LUXE · Fragrance Recommendation & Similarity Matcher
 * Pure, deterministic TypeScript recommendation engine. Zero external AI APIs.
 *
 * Scoring Weights (100% total):
 * 1. Fragrance Family: 40% (40 points)
 * 2. Longevity Preference: 25% (25 points)
 * 3. Sillage Preference: 25% (25 points)
 * 4. Occasion Suitability: 10% (10 points)
 */

import type { QuizAnswers } from '../data/fragrance-discovery';
import {
  getPerfumeMetadata,
  type PerfumeMetadata,
  type FragranceFamily,
  type LongevityRating,
  type SillageRating,
  type OccasionKey
} from '../data/fragrance-metadata';

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
  metadata: PerfumeMetadata;
}

export interface SimilarFragrance {
  product: ProductMatchRecord;
  similarityScore: number;
  sharedNotes: string[];
}

/**
 * Configurable matching weights for easy fine-tuning
 */
export const MATCHING_WEIGHTS = {
  family: 40,
  longevity: 25,
  sillage: 25,
  occasion: 10
} as const;

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
 * Category similarity matrix between the 4 major olfactory families
 * Returns baseline similarity score out of 40 points
 */
const CATEGORY_SIMILARITY_SCORES: Record<FragranceFamily, Record<FragranceFamily, number>> = {
  floral: {
    floral: 40,
    fresh: 18,     // Fresh floral, green tea rose, citrus blossoms
    gourmand: 16,  // Sweet floral, vanilla rose
    woody_amber: 12 // Floral chypre, woody rose
  },
  fresh: {
    fresh: 40,
    floral: 18,     // Fresh floral, dewy petals
    gourmand: 10,   // Citrus gourmand
    woody_amber: 12 // Citrus woody, aromatic cedar
  },
  gourmand: {
    gourmand: 40,
    woody_amber: 20, // Amber vanilla, roasted tonka, sweet resins
    floral: 16,      // Floral gourmand, sweet jasmine
    fresh: 10        // Citrus vanilla
  },
  woody_amber: {
    woody_amber: 40,
    gourmand: 20,    // Amber tonka, honeyed oud
    floral: 12,      // Woody floral, dark rose patchouli
    fresh: 12        // Fresh spicy woody
  }
};

/**
 * Numerical rating scales for distance calculation
 */
const LONGEVITY_SCALE: Record<string, number> = {
  light: 1,
  moderate: 2,
  long_lasting: 3
};

const SILLAGE_SCALE: Record<string, number> = {
  subtle: 1,
  moderate: 2,
  strong: 3
};

/**
 * Maps incoming legacy or new answer keys to canonical FragranceFamily
 */
function resolveFragranceFamily(answers: QuizAnswers): FragranceFamily | 'surprise' {
  const raw = answers.fragranceFamily || answers.scentPersona || answers.scentImpression;
  if (raw === 'fresh') return 'fresh';
  if (raw === 'floral' || raw === 'feminine') return 'floral';
  if (raw === 'gourmand' || raw === 'comforting') return 'gourmand';
  if (raw === 'woody_amber' || raw === 'captivating') return 'woody_amber';
  return 'surprise';
}

/**
 * Generates an honest, metadata-driven explanation for why a perfume was recommended.
 * Never invents claims that contradict actual product metadata.
 */
export function generateRecommendationReason(
  product: ProductMatchRecord,
  meta: PerfumeMetadata,
  answers: QuizAnswers
): string {
  const segments: string[] = [];

  // 1. Olfactory character
  const familyDescs: Record<FragranceFamily, string> = {
    floral: 'floral character',
    fresh: 'fresh citrus character',
    gourmand: 'sweet gourmand character',
    woody_amber: 'woody and amber character'
  };
  segments.push(familyDescs[meta.primaryFamily] || `${product.category} character`);

  // 2. Longevity profile (only when verified)
  if (meta.verified && meta.longevity !== 'unknown') {
    if (meta.longevity === 'long_lasting') {
      segments.push('long-lasting profile');
    } else if (meta.longevity === 'moderate') {
      segments.push('moderate, balanced wear');
    } else if (meta.longevity === 'light') {
      segments.push('light, refreshing wear');
    }
  }

  // 3. Sillage scent trail (only when verified)
  if (meta.verified && meta.sillage !== 'unknown') {
    if (meta.sillage === 'subtle') {
      segments.push('subtle scent trail');
    } else if (meta.sillage === 'moderate') {
      segments.push('moderate, inviting aura');
    } else if (meta.sillage === 'strong') {
      segments.push('radiant scent trail');
    }
  }

  // Construct sentence matching example format:
  // "Selected for its floral character, long-lasting profile, and subtle scent trail."
  let sentence = '';
  if (segments.length === 1) {
    sentence = `Selected for its ${segments[0]}.`;
  } else if (segments.length === 2) {
    sentence = `Selected for its ${segments[0]} and ${segments[1]}.`;
  } else {
    sentence = `Selected for its ${segments[0]}, ${segments[1]}, and ${segments[2]}.`;
  }

  // Accented by prominent notes from product data
  if (product.keyNotes && product.keyNotes.length > 0) {
    const notes = product.keyNotes.slice(0, 3).join(', ');
    sentence += ` Prominently featuring notes of ${notes}.`;
  }

  return sentence;
}

/**
 * Scores a product against the 4 consultation answers (Maximum 100 points).
 */
export function scoreProduct(
  product: ProductMatchRecord,
  answers: QuizAnswers
): { score: number; reason: string; metadata: PerfumeMetadata } {
  const meta = getPerfumeMetadata(product);
  let totalScore = 0;

  const allNotesText = `${product.keyNotes.join(' ')} ${product.rawNotes || ''} ${product.scentFamilies.join(' ')} ${product.description}`;

  // -------------------------------------------------------------
  // 1. Fragrance Family Matching (Weight: 40%)
  // -------------------------------------------------------------
  const chosenFamily = resolveFragranceFamily(answers);

  if (chosenFamily === 'surprise') {
    // Neutral full baseline: allows longevity, sillage, and occasion to rank
    totalScore += MATCHING_WEIGHTS.family;
  } else {
    if (meta.primaryFamily === chosenFamily) {
      totalScore += MATCHING_WEIGHTS.family; // 40 pts (Exact match)
    } else if (meta.secondaryFamilies && meta.secondaryFamilies.includes(chosenFamily)) {
      totalScore += 24; // 24 pts (Secondary family match: pure family matches are prioritized)
    } else {
      // Category similarity: 10 to 20 pts based on accords and note overlap
      const baseSim = CATEGORY_SIMILARITY_SCORES[chosenFamily]?.[meta.primaryFamily] || 12;
      let simScore = baseSim;

      // Note bonus: if product possesses prominent notes typical of chosen family
      if (chosenFamily === 'fresh' && hasAnyKeyword(allNotesText, ['citrus', 'bergamot', 'lemon', 'mandarin', 'tea', 'aquatic'])) {
        simScore = Math.min(22, simScore + 4);
      } else if (chosenFamily === 'floral' && hasAnyKeyword(allNotesText, ['rose', 'jasmine', 'peony', 'tuberose', 'violet'])) {
        simScore = Math.min(22, simScore + 4);
      } else if (chosenFamily === 'gourmand' && hasAnyKeyword(allNotesText, ['vanilla', 'tonka', 'amber', 'praline', 'caramel'])) {
        simScore = Math.min(22, simScore + 4);
      } else if (chosenFamily === 'woody_amber' && hasAnyKeyword(allNotesText, ['oud', 'incense', 'cedar', 'patchouli', 'leather'])) {
        simScore = Math.min(22, simScore + 4);
      }

      totalScore += simScore;
    }
  }

  // -------------------------------------------------------------
  // 2. Longevity Distance Ranking (Weight: 25%)
  // -------------------------------------------------------------
  const chosenLongevity = answers.longevity;

  if (!chosenLongevity || chosenLongevity === 'no_preference') {
    // "No preference" is neutral and does not favor one rating
    totalScore += 20;
  } else if (!meta.verified || meta.longevity === 'unknown') {
    // Unverified/unknown metadata receives modest neutral score (doesn't beat verified match)
    totalScore += 12;
  } else {
    const userVal = LONGEVITY_SCALE[chosenLongevity] ?? 2;
    const prodVal = LONGEVITY_SCALE[meta.longevity] ?? 2;
    const distance = Math.abs(userVal - prodVal);

    if (distance === 0) {
      totalScore += MATCHING_WEIGHTS.longevity; // 25 pts (Exact distance 0)
    } else if (distance === 1) {
      totalScore += 17; // 17 pts (Distance 1: adjacent)
    } else {
      totalScore += 5;  // 5 pts (Distance 2: opposite)
    }
  }

  // -------------------------------------------------------------
  // 3. Sillage Distance Ranking (Weight: 25%)
  // -------------------------------------------------------------
  const chosenSillage = answers.sillage || (answers.intensity === 'subtle' ? 'subtle' : answers.intensity === 'expressive' ? 'strong' : answers.intensity === 'balanced' ? 'moderate' : undefined);

  if (!chosenSillage || chosenSillage === 'no_preference') {
    // "No preference" is neutral and does not favor one rating
    totalScore += 20;
  } else if (!meta.verified || meta.sillage === 'unknown') {
    totalScore += 12;
  } else {
    const userVal = SILLAGE_SCALE[chosenSillage] ?? 2;
    const prodVal = SILLAGE_SCALE[meta.sillage] ?? 2;
    const distance = Math.abs(userVal - prodVal);

    if (distance === 0) {
      totalScore += MATCHING_WEIGHTS.sillage; // 25 pts (Exact distance 0)
    } else if (distance === 1) {
      totalScore += 17; // 17 pts (Distance 1: adjacent)
    } else {
      totalScore += 5;  // 5 pts (Distance 2: opposite)
    }
  }

  // -------------------------------------------------------------
  // 4. Occasion Suitability (Weight: 10%)
  // -------------------------------------------------------------
  const chosenOccasion = (answers.occasion || 'versatile') as OccasionKey;

  if (chosenOccasion === 'versatile') {
    totalScore += MATCHING_WEIGHTS.occasion; // 10 pts
  } else if (meta.occasions.includes(chosenOccasion) || meta.occasions.includes('versatile')) {
    totalScore += MATCHING_WEIGHTS.occasion; // 10 pts (Exact match)
  } else if (
    (chosenOccasion === 'everyday_office' && meta.occasions.includes('casual')) ||
    (chosenOccasion === 'casual' && meta.occasions.includes('everyday_office')) ||
    (chosenOccasion === 'special_occasions' && meta.occasions.includes('evening_events')) ||
    (chosenOccasion === 'evening_events' && meta.occasions.includes('special_occasions'))
  ) {
    totalScore += 7; // 7 pts (Adjacent occasion)
  } else {
    totalScore += 4; // 4 pts (Baseline)
  }

  // Clamp total to 100
  const finalScore = Math.min(100, Math.max(0, Math.round(totalScore)));
  const reason = generateRecommendationReason(product, meta, answers);

  return { score: finalScore, reason, metadata: meta };
}

/**
 * Finds top N recommendations from catalog for given quiz answers.
 * Guarantees brand diversity among the top recommendations.
 * Excludes draft or unavailable items.
 */
export function matchSignatureScents(
  catalog: ProductMatchRecord[],
  answers: QuizAnswers,
  limit = 3
): ScoredRecommendation[] {
  // Exclude drafts / unavailable products
  const activeProducts = catalog.filter((p) => !p.isDraft);

  // Deterministically score all products
  const scored: ScoredRecommendation[] = activeProducts.map((p) => {
    const { score, reason, metadata } = scoreProduct(p, answers);
    return {
      product: p,
      score,
      reason,
      metadata
    };
  });

  // Sort descending by score; if tied, prioritize verified products, then sort by slug
  scored.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (a.metadata.verified !== b.metadata.verified) {
      return a.metadata.verified ? -1 : 1;
    }
    return a.product.slug.localeCompare(b.product.slug);
  });

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

  // Fallback if not enough distinct brands exist
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
    .filter((res) => res.similarityScore >= 20);

  scoredSimilar.sort((a, b) => b.similarityScore - a.similarityScore);

  return scoredSimilar.slice(0, limit);
}
