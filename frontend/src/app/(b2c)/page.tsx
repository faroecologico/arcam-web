import Link from "next/link";
import { fetchWoo, getCategories, getSmartProducts } from "@/lib/woocommerce";
import ProductCarousel from "@/components/product/ProductCarousel";
import InfiniteCategoryCarousel from "@/components/product/InfiniteCategoryCarousel";
import Hero from "@/components/layout/Hero";
import StoreInfo from "@/components/storefront/StoreInfo";
import { ShieldCheck, Truck, Clock } from "lucide-react";

export const revalidate = 3600;

async function getHomeData() {
  try {
    // 1. Get Categories
    const categories = await getCategories();

    // 2. Identify Key Categories (top 5 by ID or logic - using first 5 for now)
    // In production, you might want to filter by specific IDs or 'menu_order'
    const topCategories = categories.slice(0, 5);

    // 3. Fetch products for each top category
    const categorySections = await Promise.all(topCategories.map(async (cat: any) => {
      const products = await getSmartProducts({
        category: String(cat.id),
        orderby: "date"
      });
      return {
        ...cat,
        products: products.slice(0, 8)
      };
    }));

    // 4. Featured/Best Sellers
    const featuredProductsRaw = await getSmartProducts({
      featured: "true"
    });
    const featuredProducts = featuredProductsRaw.slice(0, 8);

    // 5. Seasonal Offers (On Sale)
    const seasonalOffersRaw = await getSmartProducts({
      on_sale: "true",
      stock_status: "instock"
    });
    const seasonalOffers = seasonalOffersRaw.slice(0, 8);


    return { categories, categorySections, featuredProducts, seasonalOffers };
  } catch (e) {
    console.error("Home Data Fetch Error", e);
    return { categories: [], categorySections: [], featuredProducts: [], seasonalOffers: [] };
  }
}

export default async function HomePage() {
  const { categories, categorySections, featuredProducts, seasonalOffers } = await getHomeData();

  return (
    <div className="flex flex-col min-h-screen">
      {/* 1. TOFU: HERO SECTION (Awareness) */}
      <Hero />

      {/* 2. MOFU: INFINITE CATEGORY CAROUSEL (Quick Access) */}
      <InfiniteCategoryCarousel categories={categories} />

      {/* 3. 4U: VALUE PROPOSITION (Desire) */}
      <section className="bg-muted/20 py-12">
        <div className="container px-4">
          <div className="grid md:grid-cols-3 gap-6">
            <div className="flex items-center gap-4 p-4 bg-background rounded-lg shadow-sm border">
              <div className="p-3 bg-primary/10 rounded-full text-primary">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-bold text-sm">Máxima Protección</h3>
                <p className="text-muted-foreground text-xs">Cumple normativa vigente.</p>
              </div>
            </div>
            <div className="flex items-center gap-4 p-4 bg-background rounded-lg shadow-sm border">
              <div className="p-3 bg-primary/10 rounded-full text-primary">
                <Truck className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-bold text-sm">Envío Rápido</h3>
                <p className="text-muted-foreground text-xs">A todo Chile en tiempo récord.</p>
              </div>
            </div>
            <div className="flex items-center gap-4 p-4 bg-background rounded-lg shadow-sm border">
              <div className="p-3 bg-primary/10 rounded-full text-primary">
                <Clock className="h-6 w-8" />
              </div>
              <div>
                <h3 className="font-bold text-sm">Atención 24/7</h3>
                <p className="text-muted-foreground text-xs">Soporte continuo.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. CONTENT CAROUSELS (Product Discovery) */}

      {/* Seasonal Offers */}
      {seasonalOffers.length > 0 && (
        <ProductCarousel
          title="Ofertas de Temporada"
          products={seasonalOffers}
          viewAllLink="/catalogo?on_sale=true"
        />
      )}

      {/* Featured First */}
      {featuredProducts.length > 0 && (
        <ProductCarousel
          title="Destacados"
          products={featuredProducts}
          viewAllLink="/catalogo?featured=true"
        />
      )}

      {/* Categories Sections */}
      {categorySections.map((section: any) => (
        section.products.length > 0 && (
          <ProductCarousel
            key={section.id}
            title={section.name}
            products={section.products}
            viewAllLink={`/catalogo?category=${section.slug}`}
          />
        )
      ))}

      {/* Store Information */}
      <StoreInfo />

      <div className="h-12 w-full"></div>
    </div>
  );
}
