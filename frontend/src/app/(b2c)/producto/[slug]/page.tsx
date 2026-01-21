import { fetchWoo, getProductsByIds } from "@/lib/woocommerce";
import ProductDetail from "@/components/product/ProductDetail";
import { notFound } from "next/navigation";

interface PageProps {
    params: { slug: string };
}

export const revalidate = 3600;

async function getProduct(slug: string) {
    try {
        const products = await fetchWoo("products", { slug });
        return products.length > 0 ? products[0] : null;
    } catch (error) {
        console.error("Error fetching product:", error);
        return null;
    }
}

export default async function ProductPage({ params }: PageProps) {
    const { slug } = await params;
    const product = await getProduct(slug);

    if (!product) {
        notFound();
    }

    // Fetch Variants (Linked Products)
    let variants: any[] = [];
    const variantMeta = product.meta_data?.find((m: any) => m.key === "_woosl_ids");

    if (variantMeta && variantMeta.value) {
        let textIds = variantMeta.value;
        // Handle if it's already an array or a string like "[1,2,3]" or "1,2,3"
        let ids: number[] = [];

        if (Array.isArray(textIds)) {
            ids = textIds;
        } else if (typeof textIds === 'string') {
            // Clean brackets if present and split
            const cleaned = textIds.replace(/[\[\]]/g, '');
            if (cleaned.trim()) {
                ids = cleaned.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
            }
        }

        // Filter out current product ID to avoid duplicate self-reference if desired, 
        // but typically variants include the set. Let's keep all for now or filter out.
        // Usually you want to show ALL siblings including self logic is handled in UI.

        if (ids.length > 0) {
            variants = await getProductsByIds(ids);
        }
    }

    return (
        <div className="container py-8 px-4">
            <ProductDetail product={product} variants={variants} />
        </div>
    );
}
