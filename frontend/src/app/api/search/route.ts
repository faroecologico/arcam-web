import { NextResponse } from "next/server";
import { getSmartProducts, getCleanProductName, fetchWoo } from "@/lib/woocommerce";

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get("q");

    if (!query || query.length < 2) {
        return NextResponse.json([]);
    }

    try {
        // 1. First attempt: Search products directly
        let products = await getSmartProducts({ search: query });

        // 2. Second attempt: If no products, search for matching Categories
        if (products.length === 0) {
            console.log(`No products found for "${query}", trying category search...`);
            const categories = await fetchWoo("products/categories", { search: query, per_page: "1" });

            if (categories.length > 0) {
                const category = categories[0];
                console.log(`Found category: ${category.name} (ID: ${category.id})`);
                products = await getSmartProducts({ category: String(category.id) });
            } else {
                // 3. Third attempt: Main Tag search
                console.log(`No categories found for "${query}", trying tag search...`);
                let tags = await fetchWoo("products/tags", { search: query, per_page: "1" });

                if (tags.length > 0) {
                    const tag = tags[0];
                    console.log(`Found tag: ${tag.name} (ID: ${tag.id})`);
                    products = await getSmartProducts({ tag: String(tag.id) });
                } else {
                    // 4. Fourth Attempt: Keyword Tag Search (Broad Match)
                    // "Zapatos de seguridad" -> search tags for "Zapatos" OR "Seguridad"
                    console.log(`No exact tag found, trying keyword breakdown...`);

                    const stopWords = ["de", "la", "el", "en", "y", "o", "con", "para", "los", "las"];
                    const keywords = query.split(" ")
                        .map(w => w.trim().toLowerCase())
                        .filter(w => w.length > 2 && !stopWords.includes(w));

                    if (keywords.length > 0) {
                        // Find tags for each keyword
                        const tagPromises = keywords.map(k => fetchWoo("products/tags", { search: k, per_page: "1" }));
                        const tagResults = await Promise.all(tagPromises);

                        // Collect IDs of found tags
                        const foundTagIds = tagResults
                            .flatMap(result => result)
                            .map((t: any) => t.id);

                        if (foundTagIds.length > 0) {
                            console.log(`Found matching tags for keywords: ${foundTagIds.join(",")}`);
                            // Fetch products for these tags (OR logic roughly handled by fetching multiple)
                            // We'll just fetch from the first valid tag found to ensure relevance, or distinct ones?
                            // Let's force OR logic: products?tag=1,2,3... but Woo API uses 'tag' (ID) or 'tag_slug'.
                            // 'include' param is for product IDs. 'tag' param takes comma separated IDs in recent Woo versions.
                            products = await getSmartProducts({ tag: foundTagIds.join(",") });
                        }
                    }
                }
            }
        }

        // Return simplified data for the dropdown with clean names
        const suggestions = products.slice(0, 6).map((p: any) => ({
            id: p.id,
            name: getCleanProductName(p.name), // Use centralized clean name
            slug: p.slug,
            image: p.images[0]?.src || "/placeholder.png",
            price: p.price
        }));

        return NextResponse.json(suggestions);
    } catch (error) {
        console.error("Search API Error:", error);
        return NextResponse.json([]);
    }
}
