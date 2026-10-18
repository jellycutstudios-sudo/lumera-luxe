import { siteConfig } from '../data/site';

export interface CartItem {
  id: string;
  name: string;
  brand: string;
  sizeDisplay: string;
  concentration: string;
  priceMinor: number;
  quantity: number;
  image?: string;
}

export interface CustomerDeliveryInfo {
  fullName: string;
  phone: string;
  address: string;
  city: string;
  notes?: string;
  paymentMethod?: string;
}

export function formatWhatsAppOrderMessage(
  items: CartItem[],
  customerInfo?: CustomerDeliveryInfo | { name?: string; deliveryArea?: string; notes?: string }
): string {
  const dateStr = new Date().toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  const subtotalMinor = items.reduce(
    (sum, item) => sum + item.priceMinor * item.quantity,
    0
  );
  const subtotalQar = (subtotalMinor / 100).toFixed(0);

  let message = `⚜️ *LUMÈRA LUXE — NEW ORDER* ⚜️\n`;
  message += `_Placed: ${dateStr}_\n`;
  message += `━━━━━━━━━━━━━━━━━━━━━\n\n`;

  if (customerInfo) {
    const fullName = ('fullName' in customerInfo ? customerInfo.fullName : customerInfo.name) || '';
    const phone = ('phone' in customerInfo ? customerInfo.phone : '') || '';
    const address = ('address' in customerInfo ? customerInfo.address : customerInfo.deliveryArea) || '';
    const city = ('city' in customerInfo ? customerInfo.city : '') || 'Doha';
    const notes = customerInfo.notes || '';
    const payment = ('paymentMethod' in customerInfo ? customerInfo.paymentMethod : '') || 'Payment Link via WhatsApp';

    message += `📍 *CUSTOMER & DELIVERY DETAILS:*\n`;
    if (fullName) message += `• *Customer:* ${fullName.trim()}\n`;
    if (phone) message += `• *Phone / WhatsApp:* ${phone.trim()}\n`;
    if (address) message += `• *Delivery Address:* ${address.trim()}\n`;
    if (city) message += `• *City / Municipality:* ${city.trim()} (Qatar)\n`;
    message += `• *Payment Method:* ${payment.trim()}\n`;
    if (notes && notes.trim()) message += `• *Delivery Notes:* ${notes.trim()}\n`;
    message += `\n━━━━━━━━━━━━━━━━━━━━━\n\n`;
  }

  message += `🛍️ *PRODUCT DETAILS:*\n`;
  items.forEach((item, idx) => {
    const itemSubtotal = ((item.priceMinor * item.quantity) / 100).toFixed(0);
    message += `${idx + 1}. *${item.brand.toUpperCase()} — ${item.name.toUpperCase()}*\n`;
    message += `   • Size & Type: ${item.sizeDisplay} · ${item.concentration}\n`;
    message += `   • Quantity: ${item.quantity} × ${(item.priceMinor / 100).toFixed(0)} QAR\n`;
    message += `   • Subtotal: *${itemSubtotal} QAR*\n\n`;
  });

  message += `━━━━━━━━━━━━━━━━━━━━━\n`;
  message += `💰 *TOTAL AMOUNT:* *${subtotalQar} QAR*\n`;
  message += `🚚 *DELIVERY:* Express Courier in Qatar (Payment via WhatsApp)\n\n`;
  message += `Please confirm product availability and dispatch window. Thank you!`;

  return message;
}

export function generateWhatsAppLink(
  items: CartItem[],
  customerInfo?: CustomerDeliveryInfo | { name?: string; deliveryArea?: string; notes?: string }
): string {
  const message = formatWhatsAppOrderMessage(items, customerInfo);
  const phone = siteConfig.whatsappNumber.replace(/[^0-9]/g, '');
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
}
