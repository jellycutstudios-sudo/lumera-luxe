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
  email?: string;
  address: string;
  city: string;
  notes?: string;
  paymentMethod?: string;
}

export interface SupportInquiryInfo {
  topic: string;
  name?: string;
  phone?: string;
  message?: string;
}

export function formatWhatsAppOrderMessage(
  items: CartItem[],
  customerInfo?: CustomerDeliveryInfo | { name?: string; deliveryArea?: string; notes?: string; email?: string }
): string {
  const dateStr = new Date().toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  const orderRef = Math.floor(1000 + Math.random() * 9000);

  const subtotalMinor = items.reduce(
    (sum, item) => sum + item.priceMinor * item.quantity,
    0
  );
  const subtotalQar = (subtotalMinor / 100).toFixed(0);
  const totalItemCount = items.reduce((acc, it) => acc + it.quantity, 0);

  let message = `✨ *LUMÈRA LUXE · ORDER REQUEST*\n`;
  message += `_Ref: #LL-${orderRef} · ${dateStr}_\n`;
  message += `────────────────────────\n\n`;

  message += `🛍️ *ITEMS ORDERED (${totalItemCount}):*\n`;
  items.forEach((item, idx) => {
    const itemSubtotal = ((item.priceMinor * item.quantity) / 100).toFixed(0);
    message += `${idx + 1}. *${item.brand.toUpperCase()} · ${item.name}*\n`;
    message += `   • Size & Type: ${item.sizeDisplay} · ${item.concentration}\n`;
    message += `   • Quantity: ${item.quantity} × ${(item.priceMinor / 100).toFixed(0)} QAR\n`;
    message += `   • Item Total: *${itemSubtotal} QAR*\n\n`;
  });

  message += `────────────────────────\n`;
  message += `💰 *ORDER SUMMARY:*\n`;
  message += `• Products Subtotal: ${subtotalQar} QAR\n`;
  message += `• Qatar Delivery: *FREE* (Express Courier)\n`;
  message += `• *Total Amount:* *${subtotalQar} QAR*\n`;

  if (customerInfo) {
    const fullName = ('fullName' in customerInfo ? customerInfo.fullName : customerInfo.name) || '';
    const phone = ('phone' in customerInfo ? customerInfo.phone : '') || '';
    const address = ('address' in customerInfo ? customerInfo.address : customerInfo.deliveryArea) || '';
    const city = ('city' in customerInfo ? customerInfo.city : '') || 'Doha';
    const notes = customerInfo.notes || '';
    const payment = ('paymentMethod' in customerInfo ? customerInfo.paymentMethod : '') || 'Cash / Card on Delivery (POS)';

    message += `• Payment Method: ${payment.trim()}\n\n`;

    message += `────────────────────────\n`;
    message += `📍 *DELIVERY DETAILS (QATAR):*\n`;
    if (fullName) message += `• Customer: ${fullName.trim()}\n`;
    if (phone) message += `• Phone: ${phone.trim()}\n`;
    const email = ('email' in customerInfo ? customerInfo.email : '') || '';
    if (email && email.trim()) message += `• Email: ${email.trim()}\n`;
    if (address) message += `• Address: ${address.trim()}\n`;
    message += `• Municipality: ${city.trim()}, Qatar\n`;
    if (notes && notes.trim()) message += `• Special Notes: ${notes.trim()}\n`;
    message += `\n`;
  } else {
    message += `• Payment Method: Cash / Card on Delivery (POS)\n\n`;
  }

  message += `────────────────────────\n`;
  message += `Hello LUMÈRA LUXE Concierge, please confirm product availability and dispatch schedule. Thank you!`;

  return message;
}

export function formatWhatsAppSupportMessage(info: SupportInquiryInfo): string {
  const topic = info.topic || 'Fragrance Advice';
  const name = info.name?.trim();
  const phone = info.phone?.trim();
  const msg = info.message?.trim() || 'I would like personal assistance with fragrance selection and boutique availability in Qatar.';

  let output = `⚜️ *LUMÈRA LUXE · CONCIERGE SUPPORT*\n`;
  output += `────────────────────────\n`;
  output += `📋 *Topic:* ${topic}\n`;
  if (name) {
    output += `👤 *Customer:* ${name}\n`;
  }
  if (phone) {
    output += `📱 *Phone:* ${phone}\n`;
  }
  output += `📍 *Location:* Doha, Qatar\n`;
  output += `────────────────────────\n`;
  output += `💬 *Inquiry:*\n${msg}\n\n`;
  output += `────────────────────────\n`;
  output += `Hello LUMÈRA LUXE Concierge, looking forward to your assistance. Thank you!`;

  return output;
}

export function generateWhatsAppLink(
  items: CartItem[],
  customerInfo?: CustomerDeliveryInfo | { name?: string; deliveryArea?: string; notes?: string }
): string {
  const message = formatWhatsAppOrderMessage(items, customerInfo);
  const phone = siteConfig.whatsappNumber.replace(/[^0-9]/g, '');
  return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
}
