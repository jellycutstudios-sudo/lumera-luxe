# LUMÈRA LUXE — Bank Review QA Test Report

**Test Date:** 21 October 2026  
**Environment:** Local Staging (`http://localhost:4321`) & Production Build (`astro build`)  
**Test Suite:** Functional routes, policy links, mobile responsiveness, cart arithmetic, WhatsApp order generation.

---

## 1. Automated & Functional Test Matrix

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Static Site Compilation (`npm run build`) | Zero errors, 139 HTML pages generated | Built 139 pages in 745ms | **PASS** |
| **TC-02** | Route `/` (Homepage) | HTTP 200, 4 scent pillars rendered with images | HTTP 200, 4 cards live | **PASS** |
| **TC-03** | Route `/shop/` (Collection) | HTTP 200, 117 approved products displayed | HTTP 200, 117 live items | **PASS** |
| **TC-04** | Route `/terms-and-conditions/` & `/terms/` | HTTP 200, complete terms displayed | HTTP 200, both routes resolve | **PASS** |
| **TC-05** | Route `/privacy-policy/` & `/privacy/` | HTTP 200, privacy disclosures live | HTTP 200, both routes resolve | **PASS** |
| **TC-06** | Route `/returns-refunds/` | HTTP 200, 3-day perfume return rules | HTTP 200, policy rendered | **PASS** |
| **TC-07** | Route `/shipping-delivery/` | HTTP 200, Qatar courier zones & fee terms | HTTP 200, policy rendered | **PASS** |
| **TC-08** | Route `/cancellation-policy/` | HTTP 200, pre/post dispatch cancellation | HTTP 200, policy rendered | **PASS** |
| **TC-09** | Route `/contact/` | HTTP 200, corporate identity panel visible | HTTP 200, corporate panel live | **PASS** |
| **TC-10** | Route `/checkout/` | HTTP 200, assisted WhatsApp disclaimer visible | HTTP 200, disclaimer & policy links live | **PASS** |
| **TC-11** | Scent Family Filter: Fresh | Displays all 36 Fresh & Citrus perfumes | 36 products matched | **PASS** |
| **TC-12** | Scent Family Filter: Floral | Displays all 68 Floral & Rose perfumes | 68 products matched | **PASS** |
| **TC-13** | Scent Family Filter: Amber | Displays all 59 Amber & Oriental perfumes | 59 products matched | **PASS** |
| **TC-14** | Scent Family Filter: Woody | Displays all 40 Woody & Earthy perfumes | 40 products matched | **PASS** |
| **TC-15** | Cart Arithmetic | Subtotal equals sum of `priceMinor * quantity` | 750 QAR test matches exactly | **PASS** |
| **TC-16** | WhatsApp Message Generation | Well-formed URI with encoded customer & product data | Valid `https://wa.me/97466675166?text=...` | **PASS** |
| **TC-17** | Empty Bag State | Shopping bag displays clean transparent graphic | Clean transparent RGBA bag on white | **PASS** |
| **TC-18** | Mobile Navigation | Bottom navigation sheet opens, links intact | Scent modal & links verified | **PASS** |

---

## 2. Failed Tests / Identified Gaps

| ID | Issue Description | Severity | Remediation Required |
| :--- | :--- | :---: | :--- |
| **GAP-01** | **Missing Official Commercial Registration (CR) Number** | **BLOCKER** | Client must provide the official Qatar CR certificate number for display on `/contact/` and footer. |
| **GAP-02** | **Unconfirmed Exact Registered Legal Company Name** | **BLOCKER** | Client must provide exact legal company name as registered with Qatar Ministry of Commerce and Industry (MOCI). |
| **GAP-03** | **Bank Name & Written Rejection Checklist** | **HIGH** | Client must share the exact bank name (e.g. QNB, CBQ, Dukhan) and specific rejection notice to verify bank-specific clauses. |
| **GAP-04** | **8 Candidate Products Require Owner Clarification** | **MEDIUM** | 8 items in `products.json` have volume or concentration typos from the supplier sheet; currently hidden from storefront. |

---

## 3. Production Deployment Gate Status

* **Production Deployment:** **LOCKED / HELD**.
* **Live DNS Migration (`lumeraluxe.com.qa`):** **NOT PERFORMED** (Held pending client written authorization).
