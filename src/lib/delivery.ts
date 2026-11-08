export const FREE_DELIVERY_THRESHOLD_QAR = 300;

export const QATAR_DELIVERY_AREAS = [
  { value: 'Doha', label: 'Doha (Ad-Dawhah)' },
  { value: 'The Pearl & Lusail', label: 'The Pearl & Lusail' },
  { value: 'Al Rayyan & Education City', label: 'Al Rayyan & Education City' },
  { value: 'Al Wakrah & Wukair', label: 'Al Wakrah & Wukair' },
  { value: 'Al Daayen', label: 'Al Daayen' },
  { value: 'Umm Salal', label: 'Umm Salal' },
  { value: 'Al Khor', label: 'Al Khor' },
  { value: 'Other Qatar Area', label: 'Other area in Qatar' }
] as const;

export function isFreeDelivery(subtotalMinor: number): boolean {
  return subtotalMinor > FREE_DELIVERY_THRESHOLD_QAR * 100;
}

export function getDeliveryFeeQar(subtotalMinor: number): number {
  return isFreeDelivery(subtotalMinor) ? 0 : 0;
}
