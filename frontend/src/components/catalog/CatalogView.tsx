"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import ProductGrid from "@/components/product/ProductGrid";
import CategorySidebar from "@/components/product/CategorySidebar";
import { useAppStore } from "@/store/useStore";
import { ArrowRight, LayoutGrid } from "lucide-react";

interface CatalogViewProps {
    products: any[];
    allCategories: any[];
    searchQuery?: string;
    selectedCategorySlug?: string;
}

export default function CatalogView({ products, allCategories, searchQuery, selectedCategorySlug }: CatalogViewProps) {
    const mode = useAppStore((state) => state.mode);
    const isEmpresa = mode === "empresa";

    // Filter categories to show in the "Banner Grid" 
    // Show top-level categories or related to selection
    const displayedCategories = allCategories.filter(c => c.count > 0).slice(0, 4);

    const getTitle = () => {
        if (searchQuery) return `Resultados para: "${searchQuery}"`;
        if (selectedCategorySlug) {
            const match = allCategories.find((c: any) => c.slug === selectedCategorySlug);
            return match ? match.name : "Catálogo";
        }
        return "Catálogo Completo";
    };

    return (
        <div className="container py-8 px-4 space-y-8">
            {/* HER THING: Modern Header / Banner Area */}
            <div className="relative rounded-3xl overflow-hidden bg-primary/5 dark:bg-primary/10 min-h-[200px] flex items-center p-8 border border-primary/10">
                <div className="relative z-10 max-w-2xl">
                    <h1 className="text-4xl md:text-5xl font-heading font-bold uppercase tracking-tight text-primary">
                        {getTitle()}
                    </h1>
                    <p className="text-muted-foreground mt-4 text-lg">
                        {searchQuery
                            ? "Resultados de tu búsqueda en nuestro catálogo profesional."
                            : "Explora nuestra gama de productos especializados para la industria y seguridad."
                        }
                    </p>
                </div>
                {/* Decorative Background Elements */}
                <div className="absolute right-0 top-0 w-1/3 h-full bg-gradient-to-l from-primary/10 to-transparent pointer-events-none" />
                <LayoutGrid className="absolute right-10 top-1/2 -translate-y-1/2 h-64 w-64 text-primary/5 rotate-12" />
            </div>

            {/* CATEGORY BANNERS (Featured) - Only show on main catalog or if useful */}
            {!searchQuery && !selectedCategorySlug && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {displayedCategories.map((cat) => (
                        <Link
                            key={cat.id}
                            href={isEmpresa ? `/empresa/catalogo?category=${cat.slug}` : `/catalogo?category=${cat.slug}`}
                            className="group relative h-40 rounded-2xl overflow-hidden bg-muted border border-border/50 hover:shadow-lg transition-all hover:scale-[1.02]"
                        >
                            {cat.image ? (
                                <Image
                                    src={cat.image.src}
                                    alt={cat.name}
                                    fill
                                    className="object-cover transition-transform duration-700 group-hover:scale-110"
                                />
                            ) : (
                                <div className="absolute inset-0 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-slate-800 dark:to-slate-900" />
                            )}
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent p-4 flex flex-col justify-end">
                                <h3 className="text-white font-bold text-lg leading-tight group-hover:text-primary-foreground transition-colors">
                                    {cat.name}
                                </h3>
                                <div className="flex items-center gap-2 text-white/80 text-xs mt-1 opacity-0 group-hover:opacity-100 transition-opacity transform translate-y-2 group-hover:translate-y-0">
                                    <span>Ver productos</span>
                                    <ArrowRight className="h-3 w-3" />
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            )}

            <div className="flex flex-col lg:flex-row gap-8">
                <aside className="w-full lg:w-64 flex-shrink-0">
                    <CategorySidebar categories={allCategories} />
                </aside>

                <div className="flex-1">
                    {products.length === 0 ? (
                        <div className="p-16 text-center border-2 border-dashed rounded-2xl bg-muted/30 flex flex-col items-center justify-center gap-4">
                            <div className="h-16 w-16 bg-muted rounded-full flex items-center justify-center text-muted-foreground">
                                <SearchIcon />
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold">No se encontraron productos</h3>
                                <p className="text-muted-foreground">Intenta con otros filtros o términos de búsqueda.</p>
                            </div>
                        </div>
                    ) : (
                        <ProductGrid products={products} />
                    )}
                </div>
            </div>
        </div>
    );
}

function SearchIcon() {
    return (
        <svg
            className="h-8 w-8"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
        >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
    )
}
