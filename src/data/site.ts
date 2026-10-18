export interface SiteConfig {
  brandName: string;
  brandTagline: string;
  brandDescription: string;
  closingLine: string;
  location: string;
  currency: string;
  whatsappNumber: string; // international digits-only
  whatsappDisplay: string;
  email: string;
  instagramHandle: string;
  navigation: { label: string; href: string }[];
  promises: { title: string; description: string; icon: string }[];
}

export const siteConfig: SiteConfig = {
  brandName: 'LUMÈRA LUXE',
  brandTagline: 'Where Luxury Meets Affordability',
  brandDescription: 'Thoughtfully selected fragrances, trusted quality, and a personal touch—based in Qatar.',
  closingLine: 'Elegance in Every Scent',
  location: 'Doha, Qatar',
  currency: 'QAR',
  whatsappNumber: '97400000000', // Owner-verified number to be configured
  whatsappDisplay: '+974 0000 0000',
  email: 'concierge@lumeraluxe.qa',
  instagramHandle: '@lumeraluxe.qa',
  navigation: [
    { label: 'Home', href: '/' },
    { label: 'Shop Fragrances', href: '/shop/' },
    { label: 'Our Story', href: '/our-story/' },
    { label: 'Contact', href: '/contact/' }
  ],
  promises: [
    {
      title: 'Quality You Can Trust',
      description: 'Authentic designer and niche fragrances verified for genuine concentration and notes.',
      icon: 'shield'
    },
    {
      title: 'Luxury Within Reach',
      description: 'Curated luxury scents made accessible with honest and transparent pricing.',
      icon: 'sparkle'
    },
    {
      title: 'A Personal Touch',
      description: 'Direct concierge ordering on WhatsApp—tailored assistance and hand-packed delivery.',
      icon: 'chat'
    }
  ]
};
