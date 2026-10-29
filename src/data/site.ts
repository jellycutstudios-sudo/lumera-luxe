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
  instagramUrl?: string;
  tiktokHandle?: string;
  tiktokUrl?: string;
  whatsappUrl?: string;
  // Official Business Identity & Bank Review Compliance
  legalEntityName: string;
  legalEntityNameAr?: string;
  commercialRegistrationNumber: string;
  smeClassification?: string;
  legalForm?: string;
  corporateBank?: string;
  registeredOffice: string;
  dispatchHub: string;
  customerSupportEmail: string;
  complianceNotice: string;
  isBankReviewDraft: boolean;
  googleSheetWebhookUrl?: string;
  navigation: { label: string; href: string }[];
  promises: { title: string; description: string; icon: string }[];
}

export const siteConfig: SiteConfig = {
  brandName: 'LUMÈRA LUXE',
  brandTagline: 'Where Luxury Meets Affordability',
  brandDescription: 'Thoughtfully selected fragrances, trusted quality, and personal concierge service based in Qatar.',
  closingLine: 'Elegance in Every Scent',
  location: 'Doha, Qatar',
  currency: 'QAR',
  whatsappNumber: '97466675166',
  whatsappDisplay: '+974 6667 5166',
  email: 'info@lumeraluxe.com.qa',
  customerSupportEmail: 'info@lumeraluxe.com.qa',
  legalEntityName: 'Lumera Luxe Perfumes and Cosmetics W.L.L.',
  legalEntityNameAr: 'لوميرا لوكس للعطور ومستحضرات التجميل ذ.م.م',
  commercialRegistrationNumber: '253967',
  smeClassification: 'Micro (متناهية الصغر)',
  legalForm: 'W.L.L. (With Limited Liability / شركة ذات مسؤولية محدودة)',
  corporateBank: 'Qatar National Bank (QNB) / بنك قطر الوطني',
  registeredOffice: 'Doha, State of Qatar',
  dispatchHub: 'Nationwide Delivery across Qatar',
  complianceNotice: 'Boutique storefront operating under WhatsApp concierge order verification. No automated online card gateway is integrated.',
  isBankReviewDraft: false,
  googleSheetWebhookUrl: import.meta.env.PUBLIC_GOOGLE_SHEET_WEBHOOK_URL || 'https://script.google.com/macros/s/AKfycbyUBG0JbxspFySy_SKAI8-1az6i8lQ75JODW-q5OAd6us-4whx5iSQ2t5d4yq22C3amuA/exec',
  instagramHandle: '@lumera.luxe974',
  instagramUrl: 'https://www.instagram.com/lumera.luxe974?utm_source=qr&dlrf=MWRmMTR2bzFsdjZxdg==',
  tiktokHandle: '@luxescentqatar',
  tiktokUrl: 'https://www.tiktok.com/@luxescentqatar?_r=1&_t=ZS-9AgLPESklXA',
  whatsappUrl: 'https://wa.me/97466675166',
  navigation: [
    { label: 'Shop', href: '/shop/' },
    { label: 'Discovery', href: '/scent-styling/' },
    { label: 'About', href: '/our-story/' },
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
      description: 'Direct concierge ordering on WhatsApp with personal assistance and hand-packed delivery.',
      icon: 'chat'
    }
  ]
};
