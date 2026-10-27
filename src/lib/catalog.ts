import type productsData from '../data/products.json';

export type ProductList = typeof productsData;
export type Product = ProductList[0];

let cachedCatalog: ProductList | null = null;
let pendingPromise: Promise<ProductList> | null = null;

/**
 * Lazily loads the product catalog on-demand.
 * Prevents bundling the entire 196KB product catalog into the critical initial JS bundle.
 */
export async function getProductCatalog(): Promise<ProductList> {
  if (cachedCatalog) return cachedCatalog;
  if (pendingPromise) return pendingPromise;

  pendingPromise = import('../data/products.json').then((mod) => {
    cachedCatalog = mod.default;
    pendingPromise = null;
    return cachedCatalog;
  });

  return pendingPromise;
}

/**
 * Returns synchronously if already loaded, or null.
 */
export function getCachedProductCatalog(): ProductList | null {
  return cachedCatalog;
}
