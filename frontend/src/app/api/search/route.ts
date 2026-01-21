import { NextResponse } from "next/server";
import { getSmartProducts, getCleanProductName } from "@/lib/woocommerce";

export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get("q");

    if (!query || query.length < 2) {
        return NextResponse.json([]);
    }

    try {
        // Fetch products using our smart deduplicated logic
        const products = await getSmartProducts({ search: query });

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
