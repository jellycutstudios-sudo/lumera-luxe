export const FREE_DELIVERY_THRESHOLD_QAR = 300;
export const DELIVERY_FEE_QAR = 25;

export function getDeliveryFeeQar(subtotalMinor: number): number {
  return subtotalMinor > FREE_DELIVERY_THRESHOLD_QAR * 100 ? 0 : DELIVERY_FEE_QAR;
}
