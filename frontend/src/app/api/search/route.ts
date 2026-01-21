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
                // 3. Third attempt: If no categories, search for matching Tags
                console.log(`No categories found for "${query}", trying tag search...`);
                const tags = await fetchWoo("products/tags", { search: query, per_page: "1" });

                if (tags.length > 0) {
                    const tag = tags[0];
                    console.log(`Found tag: ${tag.name} (ID: ${tag.id})`);
                    products = await getSmartProducts({ tag: String(tag.id) });
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
