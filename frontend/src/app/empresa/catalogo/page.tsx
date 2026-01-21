import { fetchWoo, getSmartProducts, getCategories, getProductsByCategories } from "@/lib/woocommerce";
import CatalogView from "@/components/catalog/CatalogView";

export const revalidate = 3600;

async function getProducts(categorySlugs?: string[], searchQuery?: string) {
    try {
        let categoryIds: number[] = [];
        let allCats: any[] = [];

        if (categorySlugs && categorySlugs.length > 0) {
            allCats = await getCategories();
            categoryIds = allCats
                .filter((c: any) => categorySlugs.includes(c.slug))
                .map((c: any) => c.id);
        }

        if (categoryIds.length > 1) {
            const products = await getProductsByCategories(categoryIds);
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                return products.filter((p: any) => p.name.toLowerCase().includes(q));
            }
            return products;
        }

        else if (categoryIds.length === 1) {
            const params: any = { status: "publish", category: String(categoryIds[0]) };
            if (searchQuery) params.search = searchQuery;
            return await getSmartProducts(params);
        }

        const params: any = { status: "publish" };
        if (searchQuery) params.search = searchQuery;

        return await getSmartProducts(params);
    } catch (error) {
        console.error("Error fetching products:", error);
        return [];
    }
}

interface PageProps {
    searchParams: Promise<{ categories?: string; category?: string; search?: string }>;
}

export default async function EmpresaCatalogoPage({ searchParams }: PageProps) {
    const params = await searchParams;
    const searchQuery = params.search;
    const categoriesParam = params.categories || params.category;
    const selectedSlugs = categoriesParam ? categoriesParam.split(",") : [];

    // Parallel fetch
    const [products, allCategories] = await Promise.all([
        getProducts(selectedSlugs, searchQuery),
        getCategories()
    ]);

    return (
        <CatalogView
            products={products}
            allCategories={allCategories}
            searchQuery={searchQuery}
            selectedCategorySlug={selectedSlugs[0]}
        />
    );
}
