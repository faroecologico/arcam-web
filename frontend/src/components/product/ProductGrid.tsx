"use client";

import { useAppStore } from "@/store/useStore";
import ProductCard from "./ProductCard";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface ProductGridProps {
    products: any[];
    isB2B?: boolean;
}

const container = {
    hidden: { opacity: 0 },
    show: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1
        }
    }
};

const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
};

export default function ProductGrid({ products, isB2B }: ProductGridProps) {
    const { mode } = useAppStore();
    const isEmpresa = isB2B !== undefined ? isB2B : mode === "empresa";

    return (
        <motion.div
            variants={container}
            initial="hidden"

            animate="show"
            className={cn(
                "grid gap-4",
                isEmpresa
                    ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
                    : "grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5"
            )}
        >
            {products.map((p) => (
                <motion.div key={p.id} variants={item}>
                    <ProductCard product={p} isB2B={isEmpresa} />
                </motion.div>
            ))}
        </motion.div>
    );
}
