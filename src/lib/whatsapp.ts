import { siteConfig } from '../data/site';

export interface CartItem {
  id: string;
  name: string;
  brand: string;
  sizeDisplay: string;
  concentration: string;
  priceMinor: number;
  quantity: number;
}

export function formatWhatsAppOrderMessage(
  items: CartItem[],
  customerInfo?: { name?: string; deliveryArea?: string; notes?: string }
): string {
  const dateStr = new Date().toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  });

  const subtotalMinor = items.reduce(
    (sum, item) => sum + item.priceMinor * item.quantity,
    0
  );
  const subtotalQar = (subtotalMinor / 100).toFixed(0);

  let message = `*LUMÈRA LUXE — Fragrance Order Request*\n`;
  message += `_Date: ${dateStr}_\n\n`;

  if (customerInfo?.name) {
    message += `*Customer:* ${customerInfo.name.trim()}\n`;
  }
  if (customerInfo?.deliveryArea) {
    message += `*Delivery Area:* ${customerInfo.deliveryArea.trim()} (Qatar)\n`;
  }
  if (customerInfo?.notes) {
    message += `*Notes:* ${customerInfo.notes.trim()}\n`;
  }
  if (customerInfo?.name || customerInfo?.deliveryArea || customerInfo?.notes) {
    message += `\n`;
  }

  message += `*Selected Fragrances:*\n`;
  items.forEach((item, idx) => {
    const itemSubtotal = ((item.priceMinor * item.quantity) / 100).toFixed(0);
    message += `${idx + 1}. *${item.brand} — ${item.name}*\n`;
    message += `   ${item.sizeDisplay} · ${item.concentration}\n`;
    message += `   Qty: ${item.quantity} × ${(item.priceMinor / 100).toFixed(0)} QAR = *${itemSubtotal} QAR*\n\n`;
  });

  message += `*Estimated Subtotal:* ${subtotalQar} QAR\n`;
  message += `_(Excludes delivery charge. Final total and delivery time will be confirmed by LUMÈRA LUXE)_\n\n`;
  message += `Please confirm product availability, delivery details, and payment instructions. Thank you!`;

  return message;
}

export function generateWhatsAppLink(
  items: CartItem[],
  customerInfo?: { name?: string; deliveryArea?: string; notes?: string }
): string {
  const message = formatWhatsAppOrderMessage(items, customerInfo);
  const phone = siteConfig.whatsappNumber.replace(/[^0-9]/g, '');
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
}
