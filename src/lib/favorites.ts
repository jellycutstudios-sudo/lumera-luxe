/**
 * LUMÈRA LUXE — Client-side Wishlist / Favorites Store
 * Uses localStorage to persist customer favorites without login or passwords.
 */

const STORAGE_KEY = 'lumera_favorites_v1';

export function getFavorites(): string[] {
  if (typeof window === 'undefined') return [];
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

export function isFavorite(productId: string): boolean {
  return getFavorites().includes(productId);
}

export function toggleFavorite(productId: string): boolean {
  if (typeof window === 'undefined') return false;
  const favs = getFavorites();
  const index = favs.indexOf(productId);
  let isNowFav = false;

  if (index > -1) {
    favs.splice(index, 1);
    isNowFav = false;
  } else {
    favs.push(productId);
    isNowFav = true;
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(favs));
  } catch (e) {
    console.error('Failed to save favorites to localStorage', e);
  }

  // Dispatch custom event for real-time updates across components
  window.dispatchEvent(
    new CustomEvent('favorites-updated', {
      detail: { favorites: favs, productId, isNowFav }
    })
  );
  window.dispatchEvent(new Event('storage'));

  return isNowFav;
}

export function removeFavorite(productId: string): void {
  if (typeof window === 'undefined') return;
  const favs = getFavorites().filter((id) => id !== productId);
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(favs));
  } catch (e) {}

  window.dispatchEvent(
    new CustomEvent('favorites-updated', {
      detail: { favorites: favs, productId, isNowFav: false }
    })
  );
  window.dispatchEvent(new Event('storage'));
}
