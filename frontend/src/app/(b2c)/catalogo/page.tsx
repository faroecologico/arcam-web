import { fetchWoo, getSmartProducts, getCategories, getProductsByCategories } from "@/lib/woocommerce";
import ProductGrid from "@/components/product/ProductGrid";
import CategorySidebar from "@/components/product/CategorySidebar";

export const revalidate = 3600;

async function getProducts(categorySlugs?: string[], searchQuery?: string) {
    try {
        let categoryIds: number[] = [];
        let allCats: any[] = [];

        // If sorting or filtering by specific known categories, we might not need all logic
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

        // No category filter
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

export default async function CatalogoPage({ searchParams }: PageProps) {
    const params = await searchParams;
    const searchQuery = params.search;

    // Normalize to array
    const categoriesParam = params.categories || params.category;
    const selectedSlugs = categoriesParam ? categoriesParam.split(",") : [];

    // Parallel fetch: Products + All Categories
    // Note: getProducts might fetch categories internally if slugs are provided, but efficiently
    // We need all cats for Sidebar anyway.
    const allCategories = await getCategories();

    // Pass slugs to getProducts. It's safe to re-fetch or pass data?
    // Simplify getProducts to take resolved IDs?
    // Let's just keep logic inside getProducts for now, but optimize:
    // We already have allCategories here. Let's resolve IDs here to save a request.

    let products: any[] = [];

    if (selectedSlugs.length > 0) {
        const categoryIds = allCategories
            .filter((c: any) => selectedSlugs.includes(c.slug))
            .map((c: any) => c.id);

        if (categoryIds.length > 1) {
            products = await getProductsByCategories(categoryIds);
            if (searchQuery) {
                const q = searchQuery.toLowerCase();
                products = products.filter((p: any) => p.name.toLowerCase().includes(q));
            }
        } else if (categoryIds.length === 1) {
            const p: any = { status: "publish", category: String(categoryIds[0]) };
            if (searchQuery) p.search = searchQuery;
            products = await getSmartProducts(p);
        } else {
            // Slugs valid but match no IDs? Should fallback
            products = [];
        }
    } else {
        const p: any = { status: "publish" };
        if (searchQuery) p.search = searchQuery;
        products = await getSmartProducts(p);
    }

    // Title Logic
    const getTitle = () => {
        if (searchQuery) return `Resultados para: "${searchQuery}"`;
        if (selectedSlugs.length === 1) {
            const match = allCategories.find((c: any) => c.slug === selectedSlugs[0]);
            return match ? `Categoría: ${match.name}` : "Catálogo";
        }
        if (selectedSlugs.length > 1) return "Categorías Seleccionadas";
        return "Catálogo General";
    };

    return (
        <div className="container py-8 px-4">
            <div className="mb-8">
                <h1 className="text-3xl font-heading font-bold uppercase tracking-tight text-foreground">
                    {getTitle()}
                </h1>
                <p className="text-muted-foreground mt-2">
                    {searchQuery
                        ? "Explora los productos que coinciden con tu búsqueda."
                        : "Explora nuestra selección de productos profesionales."
                    }
                </p>
            </div>

            <div className="flex flex-col lg:flex-row gap-8">
                <aside className="w-full lg:w-64 flex-shrink-0">
                    <CategorySidebar categories={allCategories} />
                </aside>

                <div className="flex-1">
                    {products.length === 0 ? (
                        <div className="p-12 text-center border border-dashed rounded-lg bg-muted/30">
                            <p>No se encontraron productos.</p>
                            <p className="text-sm text-muted-foreground mt-2">Intenta limpiar los filtros.</p>
                        </div>
                    ) : (
                        <ProductGrid products={products} />
                    )}
                </div>
            </div>
        </div>
    );
}
