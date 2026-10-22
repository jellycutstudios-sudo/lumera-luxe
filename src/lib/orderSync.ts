import { siteConfig } from '../data/site';

export interface RecordedOrderItem {
  id: string;
  name: string;
  brand: string;
  sizeDisplay: string;
  concentration: string;
  priceQar: number;
  quantity: number;
  itemTotalQar: number;
}

export interface RecordedOrder {
  orderRef: string;
  timestamp: string;
  dateQatar: string;
  customerName: string;
  phone: string;
  email: string;
  municipality: string;
  streetAddress: string;
  deliveryNotes: string;
  totalAmountQar: number;
  totalItemsCount: number;
  paymentMethod: string;
  itemsSummary: string;
  items: RecordedOrderItem[];
}

export const STORAGE_ORDER_HISTORY_KEY = 'lumera_order_history_v1';

/**
 * Saves order to local browser storage as an archive and dispatches
 * to Google Sheets webhook in the background.
 */
export async function recordOrderSubmission(order: RecordedOrder): Promise<void> {
  // 1. Persist in local storage vault as a safety archive
  try {
    const raw = localStorage.getItem(STORAGE_ORDER_HISTORY_KEY);
    const history: RecordedOrder[] = raw ? JSON.parse(raw) : [];
    history.unshift(order);
    localStorage.setItem(STORAGE_ORDER_HISTORY_KEY, JSON.stringify(history.slice(0, 50)));
  } catch (err) {
    console.warn('[LUMÈRA LUXE] Could not save order to local history archive:', err);
  }

  // 2. Transmit to Google Sheet Webhook if configured
  const webhookUrl = siteConfig.googleSheetWebhookUrl || (typeof window !== 'undefined' ? (window as any).__LUMERA_SHEET_URL__ : '');
  if (!webhookUrl || !webhookUrl.startsWith('http')) {
    console.info('[LUMÈRA LUXE] Google Sheet Webhook URL not set. Order stored in local archive:', order.orderRef);
    return;
  }

  try {
    // Mode 'no-cors' is required for Google Apps Script Web Apps when invoked from client-side
    // keepalive: true ensures completion even if page unloads or redirects to WhatsApp
    await fetch(webhookUrl, {
      method: 'POST',
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        orderRef: order.orderRef,
        timestamp: order.timestamp,
        dateQatar: order.dateQatar,
        customerName: order.customerName,
        phone: order.phone,
        email: order.email || 'N/A',
        municipality: order.municipality,
        streetAddress: order.streetAddress,
        deliveryNotes: order.deliveryNotes || 'None',
        totalAmountQar: order.totalAmountQar,
        totalItemsCount: order.totalItemsCount,
        paymentMethod: order.paymentMethod,
        itemsSummary: order.itemsSummary,
        itemsJson: JSON.stringify(order.items)
      }),
      keepalive: true
    });
    console.info(`[LUMÈRA LUXE] Order ${order.orderRef} dispatched to Google Sheet successfully.`);
  } catch (err) {
    console.warn('[LUMÈRA LUXE] Background Google Sheet sync error (order was still dispatched to WhatsApp):', err);
  }
}
