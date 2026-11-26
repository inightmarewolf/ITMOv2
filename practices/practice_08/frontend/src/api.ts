export interface Order {
  id: number;
  owner: number;
  product: string;
  price: number;
}

export type ProductsMap = Record<string, number>;

const API_BASE = '/api';

async function parseJsonOrThrow<T>(res: Response): Promise<T> {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const message =
      typeof (data as { error?: unknown }).error === 'string'
        ? (data as { error: string }).error
        : `Ошибка сервера (${res.status})`;
    throw new Error(message);
  }
  return data as T;
}

export async function login(username: string, password: string): Promise<{ token: string }> {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  return parseJsonOrThrow<{ token: string }>(res);
}

export async function fetchProducts(): Promise<ProductsMap> {
  const res = await fetch(`${API_BASE}/products`);
  return parseJsonOrThrow<ProductsMap>(res);
}

export async function fetchOrders(): Promise<Order[]> {
  const res = await fetch(`${API_BASE}/orders`);
  return parseJsonOrThrow<Order[]>(res);
}

export async function createOrder(token: string, product: string): Promise<Order> {
  const res = await fetch(`${API_BASE}/orders`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Token': token,
    },
    body: JSON.stringify({ product }),
  });
  return parseJsonOrThrow<Order>(res);
}
