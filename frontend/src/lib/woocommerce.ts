const WOO_URL = process.env.NEXT_PUBLIC_WOO_URL;
const CK = process.env.WC_CONSUMER_KEY;
const CS = process.env.WC_CONSUMER_SECRET;

/**
 * Basic Fetcher for WooCommerce REST API
 * @param endpoint e.g. 'products', 'orders'
 * @param params Object with query parameters
 */
export async function fetchWoo(endpoint: string, params: Record<string, string> = {}) {
    if (!WOO_URL || !CK || !CS) {
        throw new Error("WooCommerce credentials missing. URL: " + WOO_URL);
    }

    const url = new URL(`${WOO_URL}/wp-json/wc/v3/${endpoint}`);

    // Default filters: Published and In Stock
    if (!params.status) url.searchParams.append("status", "publish");
    if (!params.stock_status) url.searchParams.append("stock_status", "instock");

    // Auth params
    url.searchParams.append("consumer_key", CK!);
    url.searchParams.append("consumer_secret", CS!);

    // Extra params
    Object.keys(params).forEach((key) => {
        url.searchParams.append(key, params[key]);
    });

    const res = await fetch(url.toString(), {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
        next: { revalidate: 3600 }, // Cache for 1 hour by default
    });

    if (!res.ok) {
        const errorBody = await res.text();
        throw new Error(`WooCommerce API Error (${res.status}): ${errorBody}`);
    }

    return res.json();
}

/**
 * Create an Order (or Quote) in WooCommerce
 * @param data Order object matching WC REST API structure
 */
export async function createOrder(data: any) {
    const url = new URL(`${WOO_URL}/wp-json/wc/v3/orders`);
    url.searchParams.append("consumer_key", CK!);
    url.searchParams.append("consumer_secret", CS!);

    const res = await fetch(url.toString(), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!res.ok) {
        const errorBody = await res.text();
        throw new Error(`Order Creation Error (${res.status}): ${errorBody}`);
    }

    return res.json();
}

/**
 * Helper to clean and normalize categories
 */
function cleanCategories(categories: any[]) {
    const seen = new Set();

    return categories
        .filter(cat => cat.slug !== "uncategorized")
        .map(cat => {
            let name = cat.name.trim();

            // 1. Normalize specific cases first (handling accents/typos)
            const lower = name.toLowerCase();
            if (lower === "ferreteria" || lower === "ferretería" || lower === "ferreteria general" || lower === "ferretería general") {
                name = "Ferretería";
            } else if (lower === "ropa de trabajo") {
                name = "Ropa de Trabajo";
            } else {
                // Generic Title Case for others
                name = name.replace(/\w\S*/g, (txt: string) => {
                    // Skip small words like "de", "y", "en" if not first word? 
                    // For now simple Title Case
                    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                });
            }

            return { ...cat, name };
        })
        .filter(cat => {
            // 2. Deduplicate based on the normalized name
            if (seen.has(cat.name)) return false;
            seen.add(cat.name);
            return true;
        });
}

/**
 * Fetch all product categories (with pagination)
 */
export async function getCategories() {
    let allCategories: any[] = [];
    let page = 1;
    let hasMore = true;

    while (hasMore) {
        const categories = await fetchWoo("products/categories", {
            per_page: "100",
            hide_empty: "true",
            parent: "0",
            page: String(page)
        });

        allCategories = [...allCategories, ...categories];

        // If we got less than 100, we've reached the end
        if (categories.length < 100) {
            hasMore = false;
        } else {
            page++;
        }
    }

    return cleanCategories(allCategories);
}

/**
 * Fetch specific products by their IDs
 * Used for variant grouping
 */
export async function getProductsByIds(ids: number[]) {
    if (!ids.length) return [];

    return fetchWoo("products", {
        include: ids.join(","),
        per_page: "100"
    });
}

/**
 * Find a customer by email
 */
export async function getCustomerByEmail(email: string) {
    const res = await fetchWoo("customers", { email, role: "all" });
    return res.length > 0 ? res[0] : null;
}

/**
 * Create a new customer
 */
export async function createCustomer(data: any) {
    const url = new URL(`${WOO_URL}/wp-json/wc/v3/customers`);
    url.searchParams.append("consumer_key", CK!);
    url.searchParams.append("consumer_secret", CS!);

    const res = await fetch(url.toString(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    if (!res.ok) {
        const errorBody = await res.text();
        throw new Error(`Customer Creation Error (${res.status}): ${errorBody}`);
    }

    return res.json();
}

export async function getOrdersByCustomer(customerId: number) {
    if (!customerId) return [];
    return fetchWoo("orders", { customer: String(customerId), per_page: "20" });
}

/**
 * Get clean product name by removing all variant information
 * Removes: sizes, colors, genders, dimensions, etc.
 * This ensures consistent product names across the entire frontend
 */
export function getCleanProductName(fullName: string): string {
    return fullName
        // Remove prefixes
        .replace(/^FERR?E?\.?\s*/i, '')           // Remove "FERR." or "FERRE." prefix

        // Remove size/talla variants (at end or middle)
        .replace(/\s+TALLA\s+[A-Z0-9\.\/\-]+/gi, '') // Remove "TALLA X", "TALLA L", "TALLA 42"
        .replace(/\s+T[A-Z0-9]+$/i, '')              // Remove "TX", "TL", "TXL"
        .replace(/\s+Talla\s+[A-Z0-9]+/gi, '')       // Remove "Talla L"

        // Remove color variants (common colors in Spanish)
        .replace(/\s+(NEGRO|NEGRA|AZUL|ROJO|ROJA|VERDE|AMARILLO|AMARILLA|BLANCO|BLANCA|GRIS|NARANJO|NARANJA|CAFE|ROSADO|ROSADA|CELESTE|MORADO|MORADA)(\s+\([^)]+\))?/gi, '')

        // Remove gender variants
        .replace(/\s+(VARON|VARONE|HOMBRE|DAMA|MUJER|UNISEX)/gi, '')

        // Remove numeric sizes with degree symbol or hash
        .replace(/\s+N[°º]?\s*[0-9]+/gi, '')         // Remove "N° 42", "N 40"
        .replace(/\s+#\s*[0-9]+/gi, '')               // Remove "# 10"
        .replace(/[°º]\s*[0-9]+/gi, '')              // Remove "°43", "º40" (often attached to previous word like GYBK°43)

        // Remove codes in parentheses at end (common SKU or ID)
        .replace(/\s*\(\d+\)\s*$/gi, '')             // Remove "(108057)"

        // Remove complex color/style codes (often uppercase with slash)
        // e.g. "GYBK/ROSADO", "BKBL/AZUL", "NEGRO/GRIS", "GYBK" often at end or before size
        .replace(/\s+[A-Z]+\/[A-Z]+(\s|$)/gi, ' ')   // Remove "WORD/WORD"
        .replace(/\s+[A-Z]{3,}(\s|$)/g, ' ')         // Remove standalone uppercase codes (>3 chars) like "GYBK" if checking carefully? 
        // Be careful not to remove valid words. Let's stick to slash pattern and specific context.

        // Remove specific SKUE-like codes noticed in screenshots (GYBK, BISCOE, ARCKET if they are models? actually models should stay)
        // User wants "ZAPATILLA SKECHERS ARCKET" but removing "GYBK°43"
        // The degree regex above handles "°43", leaving "GYBK". 
        // We need to clean "GYBK" if it's a color code.

        // Remove known loose junk at end
        .replace(/\s*-\s*[A-Z0-9]+$/i, '')           // Remove "- SKUE"

        // Remove dimensions/measurements (at end) - KEEPing mm/cm as they are usually product specs
        .replace(/\s+\d+(\.\d+)?\s*(m|kg|gr|g|lt|l|ml|cc|mts?|metros?)\s*$/gi, '')

        // Remove standalone single letters at end (often size indicators)
        .replace(/\s+[A-Z]$/i, '')

        // Clean up multiple spaces and trim
        .replace(/\s+/g, ' ')
        .trim();
}

/**
 * Helper to deduplicate products based on their "Base Name"
 * Removes variants like "TALLA X", "N° 40", colors, genders, etc.
 */
export function deduplicateProducts(products: any[]) {
    const groups: Record<string, any> = {};

    products.forEach((p) => {
        const baseName = getCleanProductName(p.name);

        if (!groups[baseName]) {
            groups[baseName] = { ...p, cleanName: baseName };
        } else {
            // Keep the one with an image if the stored one doesn't have one
            // or maybe keep the cheaper one? For now, first wins or image preference
            if (!groups[baseName]?.images?.length && p.images?.length) {
                groups[baseName] = { ...p, cleanName: baseName };
            }
        }
    });

    return Object.values(groups);
}

// ... existing code ...

/**
 * Fetch products for multiple categories (OR logic)
 * @param categoryIds Array of category IDs
 */
export async function getProductsByCategories(categoryIds: number[]) {
    if (!categoryIds.length) return [];

    // Parallel fetch for each category
    const promises = categoryIds.map(id =>
        getSmartProducts({ category: String(id), per_page: "20" }) // Fetch top 20 from each to keep it fast
    );

    const results = await Promise.all(promises);

    // Flatten and Deduplicate
    const allProducts = results.flat();
    return deduplicateProducts(allProducts);
}

/**
 * Smart Product Fetcher with Deduplication
 */
export async function getSmartProducts(params: Record<string, string> = {}) {
    // Fetch a bit more than requested to ensure we have enough after deduplication
    // limit 100 is max for WC usually
    const fetchParams = { ...params, per_page: "100" };
    const products = await fetchWoo("products", fetchParams);

    if (!Array.isArray(products)) return [];

    return deduplicateProducts(products);
}
