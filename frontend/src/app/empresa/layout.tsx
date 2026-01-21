import { getCategories } from "@/lib/woocommerce";
import { Header } from "@/components/layout/Header";
import { ModeSync } from "@/components/layout/ModeSync";

export default async function EmpresaLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    // Fetch categories for the Header
    const categories = await getCategories().catch(err => {
        console.error("Failed to fetch categories:", err);
        return [];
    });

    return (
        <div className="dark">
            {/* Force dark mode class on container to cascade variables */}
            <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
                <ModeSync mode="empresa" />
                <Header categories={categories} forcedMode="empresa" />
                <div className="pt-0">
                    {children}
                </div>
            </div>
        </div>
    );
}
