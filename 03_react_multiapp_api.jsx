// Portfolio sample: reusable API client for ecommerce + backoffice.

export function createApiClient({ baseUrl, getToken }) {
  async function request(path, { method = "GET", body } = {}) {
    const token = getToken ? getToken() : null;
    const headers = { "Content-Type": "application/json" };
    if (token) headers.Authorization = `Bearer ${token}`;

    const res = await fetch(`${baseUrl}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`HTTP ${res.status} ${txt}`);
    }

    if (res.status === 204) return null;
    return res.json();
  }

  return {
    auth: {
      register: (payload) => request("/api/v1/auth/register", { method: "POST", body: payload }),
      changePassword: (payload) => request("/api/v1/auth/change-password", { method: "POST", body: payload }),
    },
    commerce: {
      catalog: () => request("/api/v1/commerce/catalog/items?active_only=true"),
      checkoutSimulate: (payload) => request("/api/v1/commerce/checkout/simulate", { method: "POST", body: payload }),
      orders: () => request("/api/v1/commerce/orders"),
      entitlements: () => request("/api/v1/commerce/entitlements/me"),
    },
    backoffice: {
      createCatalogItem: (payload) => request("/api/v1/commerce/catalog/items", { method: "POST", body: payload }),
      grantBadge: (payload) => request("/api/v1/commerce/badges/grant", { method: "POST", body: payload }),
      rpc: (rpcName, payload) => request(`/api/v1/commerce/rpc/${rpcName}`, { method: "POST", body: { payload } }),
    },
  };
}
