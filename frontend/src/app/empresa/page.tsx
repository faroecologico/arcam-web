import Hero from "@/components/layout/Hero";
import ProductGrid from "@/components/product/ProductGrid";
import { fetchWoo } from "@/lib/woocommerce";
import { Truck, ShieldCheck, CreditCard } from "lucide-react";

export const revalidate = 3600;

export default async function EmpresaPage() {
    let featuredProducts = [];
    try {
        featuredProducts = await fetchWoo("products", { per_page: "6", status: "publish", stock_status: "instock" });
    } catch (error) {
        console.error("Error fetching products:", error);
    }

    return (
        <div className="flex flex-col min-h-screen">
            {/* HERO is client-side but handled by layout state */}
            {/* Ideally we pass forcedMode to Hero if we updated it, but for now we rely on Store sync */}
            <Hero />

            {/* B2B VALUE PROPS */}
            <section className="bg-muted/50 py-12 dark:bg-slate-900/50">
                <div className="container px-4">
                    <div className="grid gap-8 md:grid-cols-3 text-center">
                        <div className="flex flex-col items-center p-6 rounded-lg border bg-card shadow-sm dark:border-slate-800">
                            <Truck className="h-10 w-10 text-primary mb-4" />
                            <h3 className="font-bold text-lg mb-2">Despacho Consolidado</h3>
                            <p className="text-sm text-muted-foreground">Envíos a todo Chile optimizados para grandes volúmenes.</p>
                        </div>
                        <div className="flex flex-col items-center p-6 rounded-lg border bg-card shadow-sm dark:border-slate-800">
                            <ShieldCheck className="h-10 w-10 text-primary mb-4" />
                            <h3 className="font-bold text-lg mb-2">Equipamiento Certificado</h3>
                            <p className="text-sm text-muted-foreground">Cumplimiento de normas técnicas y estándares de seguridad.</p>
                        </div>
                        <div className="flex flex-col items-center p-6 rounded-lg border bg-card shadow-sm dark:border-slate-800">
                            <CreditCard className="h-10 w-10 text-primary mb-4" />
                            <h3 className="font-bold text-lg mb-2">Facturación Directa</h3>
                            <p className="text-sm text-muted-foreground">Precios netos y facilidades de pago para empresas registradas.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* FEATURED CATALOG */}
            <section className="container py-16 px-4">
                <div className="mb-8">
                    <h2 className="text-2xl font-heading font-bold uppercase text-foreground">Catálogo Industrial</h2>
                    <p className="text-muted-foreground">Selección destacada para faena y operaciones.</p>
                </div>

                {featuredProducts.length > 0 ? (
                    <ProductGrid products={featuredProducts} isB2B={true} />
                ) : (
                    <p>Cargando catálogo...</p>
                )}
            </section>
        </div>
    );
}
