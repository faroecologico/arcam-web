import { getCategories } from "@/lib/woocommerce";
import { Header } from "@/components/layout/Header";
import { ModeSync } from "@/components/layout/ModeSync";

export default async function B2CLayout({
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
        <>
            <ModeSync mode="persona" />
            <Header categories={categories} />
            <div className="pt-0">
                {children}
            </div>
        </>
    );
}
