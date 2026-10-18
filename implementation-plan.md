# LUMÈRA LUXE — Antigravity implementation plan

## 1. Product direction
Build a premium, spacious fragrance storefront for Qatar. Prioritise effortless mobile browsing, clear product information and personal service. The mood is a quiet fragrance boutique: warm ivory, rich ink, restrained copper and generous whitespace.

Phase-one assumption: catalogue, shopping bag and WhatsApp order requests. Payment, availability and delivery are confirmed personally. No online payment processing, customer accounts or automated inventory in this scope. Confirm this assumption before implementing a different checkout. Currency is provisionally QAR because the business is based in Qatar; the spreadsheet itself does not explicitly identify a currency.

## 2. Source audit and launch blockers
The supplied workbook contains 25 product rows in Brands and a corresponding list in Image and notes. The Arabic sheet has no populated cell values. There are 25 embedded media files stored using Excel rich-data relationships; standard cell extraction returns #VALUE! for the image cells. Recover pictures through workbook metadata and verify their product mapping visually. Do not associate images merely by ZIP file order.

Suggested selling prices span 170–680 in unspecified currency. Use these only as provisional prices pending owner approval. The Change sticker column is ambiguous: never display it as an original price, MSRP or discount reference until its meaning is confirmed.

Resolve these differences before publishing the affected records:
- Carolina Herrera CH Women: EDP in Brands versus EDT in Image and notes.
- Givenchy Dahlia Divin: 100 ml in Brands versus 75 ml in Image and notes.
- Lancôme Idôle: 100 ml in Brands versus 75 ml in Image and notes.
- Chanel N°5 and Lalique Amethyst Éclat use EDU, which requires confirmation rather than an automatic replacement.
- Review names such as Carolina Herrera CH CH, Lanvin Jenne Blossom and Dolce & Gababana against bottle labels and owner-approved details.
- Clean whitespace, spelling and formatting in notes without inventing scent claims. Verify notes against the exact fragrance variant before publishing. The workbook does not reliably divide notes into top, heart and base, so initially display a simple Key notes list.
- Product availability, descriptions, image usage permission and currency require owner confirmation.

Keep raw workbook values in a private import report. Public data must contain only approved customer-facing fields. Mark unresolved products as draft; exclude drafts from public pages, search and structured data.

## 3. Visual system
| Element | Specification |
|---|---|
| Page background | Warm ivory #FAF8F4 |
| Alternate surface | Soft stone #F1EAE2 |
| Main text | Deep brown-black #25211E |
| Accent | Copper #A6532D, used sparingly |
| Borders | Warm neutral #E3DBD2 |
| Display type | Cormorant Garamond, medium weight, self-hosted WOFF2 |
| Body and controls | Inter, regular and medium, self-hosted WOFF2 |
| Mobile body size | 16 px; line height 1.5–1.65 |
| Mobile title | Fluid 36–44 px |
| Desktop title | Fluid 56–72 px |
| Content width | Maximum 1200 px |
| Mobile page gutters | 20 px; 16 px at very narrow widths |
| Desktop gutters | 40–64 px |
| Section spacing | 56–72 px mobile; 88–112 px desktop |
| Grid gaps | 16 px mobile; 24–32 px desktop |
| Controls | At least 44 × 44 px; primary buttons around 48–52 px tall |
| Corners | Restrained 4–8 px; avoid excessive pill shapes |

Use the existing copper logo. Create a horizontal header arrangement with emblem left and wordmark right, and a standalone emblem for favicon use. Confirm the SVG reconstruction with the owner because it slightly changes the original lettering. Convert the final approved logo lettering to vector outlines for consistent website rendering; retain its editable source separately.

Avoid gold gradients, glass panels, dense bordered cards, decorative dashboards, fake ratings, countdown timers, unsolicited popups, scrolling announcements, custom cursors and autoplay video. Luxury should come from composition, typography and photography.

## 4. Pages and navigation
Header: Home, Shop, Our Story, Contact. Desktop has search and bag controls. Mobile has compact logo, search, bag count and an accessible menu. Keep the header approximately 64–72 px tall. Do not add a competing fixed bottom navigation bar.

Routes:
- / — home
- /shop/ — catalogue
- /perfumes/[slug]/ — individual product pages
- /bag/ — review selections and request an order
- /our-story/ — brand story, mission, vision and promise
- /contact/ — approved WhatsApp, phone, email, hours and social links
- /delivery-returns/ — owner-approved delivery, cancellation, return and refund information
- /privacy/ — accurate explanation of data handling
- /404.html — helpful recovery links

Only show locations, hours and channels actually supplied by the owner. Keep missing values in private configuration as TODOs, never publish dummy phone numbers or sample addresses.

## 5. Homepage composition
1. Editorial hero. Headline: Where Luxury Meets Affordability. Supporting line: Thoughtfully selected fragrances, trusted quality, and a personal touch—based in Qatar. One primary button: Explore Fragrances. Small secondary link: Our Story. One carefully composed photograph, ideally using real stocked products. On mobile, copy precedes the image and the main button is visible without excessive scrolling.
2. Selected fragrances. Four owner-selected products, with a View all fragrances link. Label them Selected for You or Discover the Collection; do not call them bestsellers without sales evidence.
3. Explore by scent. Three or four restrained text links or image tiles using approved catalogue families. Each links to a filtered catalogue. Populate only supported categories.
4. Brand story. A short two- or three-sentence introduction paired with one editorial image. Link to the complete story.
5. Our promise. Quality You Can Trust; Luxury Within Reach; A Personal Touch. Present as a calm text row on desktop and a simple vertical group on mobile.
6. Personal assistance. Need help choosing a scent? Offer a single WhatsApp conversation link.
7. Footer. Brand sign-off, navigation, contact and policy links. Use one closing line, Elegance in Every Scent. Do not repeat every supplied tagline throughout the page.

Keep the full mission, vision and long introduction on Our Story, rather than making the homepage a wall of text. Do not add reviews until real, approved customer reviews are available.

## 6. Catalogue and product experience
Catalogue: two columns on typical mobile widths, three on tablet and four on desktop. At unusually narrow widths or enlarged text, allow a one-column layout. Product cards have a 4:5 image area, brand, fragrance name, size/concentration and price. Keep names readable; avoid hover-only controls. Use the same image scale and neutral backdrop across all products without stretching or cropping bottles.

Search by name, brand and verified notes. Provide brand, scent-family and price filters. Mobile filters open in a bottom sheet with clear labels, result count, Apply and Clear. Desktop uses a compact filter toolbar. Support price ascending/descending and name sorting. Keep filters in URL parameters; preserve filters and scroll position when returning from a product. Include an informative zero-results state. With 25 products, display the complete grid with lazy-loaded images rather than infinite scrolling.

Product page: large bottle image, brand, full name, confirmed size/concentration, price, simple description, key notes, quantity and Add to bag. Allow accessible image enlargement. Display availability only when verified; otherwise use Availability confirmed on WhatsApp. A small delivery/returns section links to the complete policy. Optional related fragrances use real shared note/family tags, maximum three or four items.

On mobile, introduce a compact sticky Add to bag bar only after the original button scrolls out of view. Respect safe-area insets and do not overlap content or other controls. On add, update the bag count and announce Added to bag with a View bag action; do not forcibly open a full-screen cart every time.

## 7. WhatsApp ordering
Flow: Browse → product → Add to bag → review bag → Send order request on WhatsApp → owner confirms availability, final total, delivery and payment instructions.

Bag shows items, variant, unit price, quantity, subtotal and remove controls. Collect only optional first name and delivery area initially; obtain detailed address and payment receipt privately during the WhatsApp conversation. If the owner requires an address form later, explain that its fields are included in the outgoing message and do not persist them in browser storage.

Store only product IDs, variant IDs and quantities in localStorage. Recalculate against current catalogue data on load; remove unavailable IDs and notify the customer of price changes. Never trust saved client prices. These prices remain an estimate until the business confirms them.

Generate the message with encodeURIComponent using the verified WhatsApp number in international digits-only format. Include item names, variants, quantities, unit prices, subtotal and optional delivery area. Add Please confirm availability, delivery charge and payment instructions. Do not present an unknown delivery fee as zero or label a subtotal as a final payable total.

Opening WhatsApp is not proof a message was sent, an order accepted or a payment received. Do not display Order confirmed or clear the bag automatically. Provide Copy order details and a visible contact fallback. Check long messages for realistic multi-item bags.

For manual payment, the owner supplies verified payment instructions after accepting the request. Customer shares the receipt privately; the owner verifies actual receipt of funds before dispatch. A screenshot alone is not a payment-status integration. Returns/refunds remain manually managed under an owner-approved policy.

## 8. Micro-interactions
| Interaction | Treatment |
|---|---|
| Button press | Small colour change and optional 0.98 scale; 120–160 ms |
| Product hover | Image scale up to 1.025; 220–280 ms; pointer devices only |
| Menu/filter sheet | Short slide and fade; 180–240 ms |
| Add to bag | Count update and brief inline confirmation; 160–220 ms |
| Accordion | Smooth disclosure; approximately 180 ms |
| Editorial reveal | Once-only opacity and 8–12 px movement; 250–350 ms |

Content must remain visible and usable if scripts fail. Respect prefers-reduced-motion and disable translations/scaling for those users. No scroll hijacking, long page transitions, perpetual floating bottles, large parallax or animation blocking a click. Use CSS transitions first; no animation library is needed for these effects.

## 9. Technical architecture
Recommended: Astro static pages, TypeScript, CSS design tokens and small React islands for search/filter, bag and interactive controls. Keep product pages pre-rendered and all essential product content available without JavaScript. Plain client scripts may replace React if they remain simpler.

A static-first implementation fits this small catalogue and keeps hosting portable. Current official Astro documentation supports static deployment to Vercel without extra configuration; the Cloudflare guide recommends Workers for new projects. Keep server-only dependencies out of the first version. Select and pin supported dependency versions when implementation starts.

Suggested structure:
- src/pages/ — routes and generated product pages
- src/components/ — header, footer, product card, hero, filter sheet, bag controls
- src/data/products.json — approved catalogue only
- src/data/site.ts — brand content, contact channels and confirmed business information
- src/lib/catalog.ts — validation, sorting and filtering
- src/lib/bag.ts — client-side bag state and current-price reconciliation
- src/lib/whatsapp.ts — message generation and contact URL
- src/styles/ — tokens, typography, layouts and motion
- src/assets/products/ — optimised product source images
- scripts/ — repeatable workbook import and validation
- private-source/ — source workbook and review notes, excluded from deployed assets

Product model: id, slug, brand, name, sizeMl, concentration, currency, priceMinor, images with alt text, scentFamilies, notes, description, availabilityStatus, featured, publicationStatus. Use stable IDs and an extensible variant field when the same fragrance gains multiple sizes. Optional compareAtPriceMinor stays absent until validated. Keep source sheet/row and unresolved issues in the private import report.

Provide a documented update workflow: edit approved catalogue or import a revised workbook → review changes → validate → commit → preview → publish. There is no business-owner admin dashboard in phase one. Add a CMS only if independent owner editing becomes a requirement.

## 10. Assets, accessibility and performance
Recover and inspect the embedded product pictures; verify exact bottle/box, size and concentration. If the images are too small or mismatched, request replacements. Do not generate counterfeit-looking product labels or invent commercial bottle designs. Optional generated imagery may be used only for decorative mood imagery with no implication that it is an exact product photograph.

Use responsive AVIF/WebP images with explicit dimensions and preserved aspect ratio. Load the hero image eagerly, lazy-load below-fold products, and avoid embedding the Excel file in the public build. Use text alternatives describing the actual product. Limit initial fonts to two families and essential weights.

Accessibility: WCAG AA contrast as a target, visible keyboard focus, proper labels, semantic headings, accessible status announcements and no hover dependence. Dialogs trap focus, close with Escape and return focus to their opener. Check 200% zoom and 320 px layouts.

Performance targets, not guarantees: mobile Lighthouse performance 90+, accessibility 95+, LCP under 2.5 s, CLS under 0.1 and INP under 200 ms when field data becomes available. Test under mobile throttling, not only desktop broadband. Aim for initial hero media under 250 KB where quality permits and card images approximately 40–100 KB. Prioritise product label legibility over rigid file-size targets.

## 11. SEO and measurement
Unique titles/descriptions, canonical URLs, sitemap, robots rules, social preview image and readable product URLs. Product structured data must match the displayed verified price, currency and availability; omit unknown fields. Add brand Organisation data only with confirmed contact details. Do not fabricate ratings, reviews, addresses or in-stock status.

Track product views, search, filter use, bag additions and WhatsApp request clicks if analytics is enabled. Treat a WhatsApp click as an enquiry signal, not a sale. Never send personal information, message contents or addresses to analytics. Keep Arabic-ready component structure and CSS logical properties, but launch Arabic only after approved translations and RTL testing. The workbook's empty Arabic sheet is not translation content.

## 12. Implementation sequence in Antigravity
1. Foundation and data review: inspect source files, produce the discrepancy report, recover image relationships, establish approved fields and draft flags. Scaffold the project, tokens and routes.
2. Design checkpoint: implement only header, mobile hero and one representative product card using real content. Review at 390 px and 1440 px before extending the system.
3. Storefront: build home, catalogue, product template, search/filter and empty states. Generate product routes from validated records.
4. Ordering: implement bag, persistence, quantities, current-price reconciliation, WhatsApp message and fallbacks. Ensure no false order/payment confirmations.
5. Content and refinement: story, contact, approved policies, micro-interactions, responsive image optimisation and SEO.
6. QA and launch: run build/type checks and targeted end-to-end checks, inspect mobile screenshots, deploy preview, resolve owner data/policy blockers, then publish.

Do not ask Antigravity to build everything in one unreviewed pass. At each stage, supply this plan and ask it to finish that stage, describe changes and report unresolved content.

## 13. Acceptance checklist
- All 25 source products are accounted for as published or held drafts; no unresolved record silently published.
- Product images map to correct records and confirmed variants.
- No Change sticker discounts, invented testimonials or unverified availability claims.
- Product links work on direct navigation and refresh.
- Search/filter combinations, clear filters and zero results work.
- Bag survives refresh; quantity limits and price totals behave correctly.
- WhatsApp text matches the bag, preserves accents and includes confirmed contact number.
- WhatsApp cancellation/failure does not falsely confirm an order or delete the bag.
- No horizontal overflow at 320, 375, 390, 768 and 1440 px; test actual iPhone Safari and Android Chrome.
- Keyboard use, focus restoration, reduced motion and sticky CTA safe areas work.
- Approved delivery/returns policy, currency, pricing, contact channels and image rights are ready.
- Production hostname/canonical, HTTPS, sitemap, redirects and 404 work.

## 14. Deployment and later upgrades
Use Git as the source of truth. Vercel is the simplest proposed first deployment: import the repository, build with npm run build and deploy the static dist directory using the detected Astro preset. Review branch/PR previews before production merges. Cloudflare Workers Static Assets is the alternative; configure the generated dist assets and correct HTML/404 handling. Recheck current provider instructions during deployment. No runtime secrets are needed for a public catalogue plus WhatsApp link.

Later phases may introduce a CMS, verified inventory, real order records, customer notifications and a payment gateway. Payment integration requires server-side price validation, webhook signature verification, idempotent payment/order updates, reconciliation, refund handling and access control. Preserve stable product IDs now so that future order data can reuse them. Do not promise that a gateway alone provides order management.

## 15. Information to collect from the owner
Verified WhatsApp number, email and social accounts; approved logo; currency and final selling prices; confirmed bottle variants; stock handling; delivery areas/charges/timing; payment instructions; return/refund/cancellation policy; product-image permission; and whether launch is English-only. Missing items should not block building the design, but must block publishing the relevant functionality or claim.

## Antigravity kickoff instruction
Read this complete plan and inspect the supplied workbook and approved logo before implementation. Build a production-quality, mobile-first LUMÈRA LUXE fragrance catalogue using Astro and TypeScript, with small interactive islands only where needed. Follow the exact spacious ivory/copper visual direction. Start with source audit, design tokens, header, hero and a representative real product card. Preserve the brand spelling LUMÈRA LUXE. Report source conflicts rather than guessing. Keep unconfirmed products as drafts. Build the phase-one WhatsApp order-request flow only after the initial visual checkpoint. Never fabricate stock, discounts, testimonials, delivery claims or business contact details. Finish each phase with a successful build and a concise list of implemented work and unresolved inputs.

## Technical references checked
- https://docs.astro.build/en/guides/deploy/vercel/
- https://docs.astro.build/en/guides/deploy/cloudflare/
- https://vercel.com/docs/git
