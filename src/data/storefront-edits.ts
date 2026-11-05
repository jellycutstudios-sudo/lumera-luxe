export const discoverySlugs = [
  'boucheron-ambre-d-alexandrie',
  'hermes-eau-des-merveilles-l',
  'chopard-leather-malaki',
  'boucheron-patchouli-d-angkor'
];

export const occasions = [
  {
    id: 'everyday',
    title: 'Everyday & Office',
    image: '/assets/brand/occasion-everyday.webp',
    slugs: ['dolce-and-gabbana-light-blue', 'boucheron-quatre-en-bleu', 'chanel-gabrielle', 'dior-joy']
  },
  {
    id: 'date-night',
    title: 'Date Night',
    image: '/assets/brand/occasion-date-night.webp',
    slugs: ['carolina-herrera-good-girl', 'burberry-burberry-goddess', 'dolce-gabbana-devotion', 'tom-ford-velvet-orchid']
  },
  {
    id: 'majlis',
    title: 'Majlis & Evening',
    image: '/assets/brand/occasion-majlis.webp',
    slugs: ['chopard-oud-malaki', 'chopard-black-incense-malaki', 'dolce-and-gabbana-velvet-desert-oud', 'tom-ford-black-orchid']
  },
  {
    id: 'gifting',
    title: 'Celebrations',
    image: '/assets/brand/occasion-gifting.webp',
    slugs: ['chanel-n-5', 'yves-saint-laurent-libre', 'parfums-de-marly-delina', 'dior-j-adore']
  }
];

export function isEligibleForShowcase(product: { slug: string; isDraft?: boolean }) {
  return !product.isDraft && product.slug !== 'aigner-iconista';
}

export function hasSpecialPrice(product: { priceMinor: number; stickerPriceMinor?: number | null }) {
  return (product.stickerPriceMinor ?? 0) > product.priceMinor;
}
