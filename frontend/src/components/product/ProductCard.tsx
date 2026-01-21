import { getGenericImage } from "@/lib/imageUtils";
import { getCleanProductName } from "@/lib/woocommerce";

import Image from "next/image";
import Link from "next/link";
import { useAppStore } from "@/store/useStore";
import { Button } from "../ui/button";
import { ShoppingCart, FileText, Plus, Check } from "lucide-react";
import { useState } from "react";
import { motion } from "framer-motion";

interface Product {
    id: number;
    name: string;
    slug: string;
    price: string;
    regular_price: string;
    sale_price: string;
    images: { src: string; alt: string }[];
    sku: string;
    stock_quantity: number | null;
    stock_status: string;
    categories: { id: number; name: string; slug: string }[];
}

export default function ProductCard({ product, isB2B }: { product: Product, isB2B?: boolean }) {
    const { mode, addToCart, addToQuote, openCart } = useAppStore();
    const isEmpresa = isB2B !== undefined ? isB2B : mode === "empresa";
    const [added, setAdded] = useState(false);

    // Use centralized clean name function
    const baseName = getCleanProductName(product.name);


    const productLink = isEmpresa ? `/empresa/producto/${product.slug}` : `/producto/${product.slug}`;
    const fallbackImage = getGenericImage(product.id);

    const handleAction = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();

        const cartItem = {
            id: String(product.id),
            name: product.name,
            price: parseFloat(product.price || "0"),
            quantity: 1,
            image: product.images[0]?.src || fallbackImage,
        };

        if (isEmpresa) {
            addToQuote(cartItem);
        } else {
            addToCart(cartItem);
        }

        openCart(); // Auto-open drawer for better UX
        setAdded(true);
        setTimeout(() => setAdded(false), 2000);
    };

    // Unified View for both Modes (Dark/Light handled by Tailwind 'dark' class)
    return (
        <motion.div
            whileHover={{ y: -8 }}
            className="group relative overflow-hidden rounded-xl border bg-card transition-all hover:shadow-xl dark:border-slate-800 dark:bg-slate-900"
        >
            <Link href={productLink} className="block relative aspect-square w-full overflow-hidden bg-muted dark:bg-slate-800">
                <Image
                    src={product.images[0]?.src || fallbackImage}
                    alt={product.images[0]?.alt || product.name || "Producto ARCAM"}
                    fill
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    className={`object-cover transition-transform duration-500 group-hover:scale-110 ${!product.images[0]?.src ? "grayscale-[0.2]" : ""}`}
                />

                {product.stock_status !== 'instock' && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-white font-bold">
                        AGOTADO
                    </div>
                )}

                {/* Category Floating Badge */}
                <div className="absolute top-2 left-2 opacity-0 transform -translate-y-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-y-0">
                    <span className="bg-black/70 text-white text-[10px] px-2 py-1 rounded uppercase tracking-wider font-bold">
                        {product.categories?.[0]?.name}
                    </span>
                </div>
            </Link>

            <div className="p-4">
                <h3 className="line-clamp-2 text-sm font-medium text-foreground dark:text-slate-200 min-h-[40px] leading-tight">
                    <Link href={productLink}>{baseName}</Link>
                </h3>

                <div className="mt-3 flex items-center justify-between">
                    <div className="flex flex-col">
                        {!isEmpresa ? (
                            <span className="text-lg font-bold text-primary dark:text-green-400">
                                ${parseInt(product.price || "0").toLocaleString("es-CL")}
                            </span>
                        ) : (
                            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                                Cotización
                            </span>
                        )}
                    </div>

                    <Button
                        size={isEmpresa ? "sm" : "icon"}
                        className={`rounded-full shadow-md transition-all duration-300 
                            ${added
                                ? "bg-green-600 hover:bg-green-700"
                                : isEmpresa
                                    ? "bg-slate-800 hover:bg-slate-700 text-white dark:bg-slate-700 dark:hover:bg-slate-600"
                                    : "hover:scale-110"
                            }`}
                        onClick={handleAction}
                        disabled={product.stock_status !== 'instock'}
                    >
                        {added ? (
                            <Check className="h-5 w-5 text-white" />
                        ) : isEmpresa ? (
                            <div className="flex items-center gap-2 px-2">
                                <FileText className="h-4 w-4" />
                                <span className="text-xs font-medium">Cotizar</span>
                            </div>
                        ) : (
                            <Plus className="h-5 w-5" />
                        )}
                    </Button>
                </div>
            </div>
        </motion.div>
    );
}
