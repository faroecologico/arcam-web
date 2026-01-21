"use client";

import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { ChevronRight, Menu, LayoutGrid } from "lucide-react";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { useAppStore } from "@/store/useStore";

interface Category {
    id: number;
    name: string;
    slug: string;
    parent?: number;
    image?: { src: string };
    children?: Category[]; // Recursive for later
}

interface MegaMenuProps {
    categories: Category[];
}

export default function MegaMenu({ categories = [] }: MegaMenuProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [hoveredCategory, setHoveredCategory] = useState<Category | null>(null);
    const mode = useAppStore((state) => state.mode);
    const isEmpresa = mode === "empresa";

    return (
        <div
            className="relative"
            onMouseEnter={() => setIsOpen(true)}
            onMouseLeave={() => setIsOpen(false)}
        >
            <Link
                href={isEmpresa ? "/empresa/catalogo" : "/catalogo"}
                className="flex items-center gap-2 cursor-pointer font-medium hover:text-primary py-2"
            >
                <LayoutGrid className="h-5 w-5" />
                <span>Todas las Categorías</span>
            </Link>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        transition={{ duration: 0.2 }}
                        className="absolute top-full left-0 mt-0 w-[800px] h-[500px] bg-white dark:bg-slate-950 rounded-lg shadow-2xl border border-gray-100 dark:border-gray-800 z-50 overflow-hidden flex"
                    >
                        {/* LEFT COLUMN: Main Categories */}
                        <div className="w-1/3 border-r bg-gray-50/50 dark:bg-slate-900/50 overflow-y-auto py-2">
                            {categories.map((cat) => (
                                <Link
                                    key={cat.id}
                                    href={isEmpresa ? `/empresa/catalogo?category=${cat.slug}` : `/catalogo?category=${cat.slug}`}
                                    className={cn(
                                        "flex items-center justify-between px-4 py-3 text-sm transition-colors hover:bg-white dark:hover:bg-slate-800 hover:text-primary",
                                        hoveredCategory?.id === cat.id && "bg-white dark:bg-slate-800 text-primary font-medium"
                                    )}
                                    onMouseEnter={() => setHoveredCategory(cat)}
                                >
                                    <span className="truncate">{cat.name}</span>
                                    <ChevronRight className="h-4 w-4 opacity-50" />
                                </Link>
                            ))}
                        </div>

                        {/* RIGHT COLUMN: Dynamic Content based on Hover */}
                        <div className="flex-1 p-6 bg-white dark:bg-slate-950">
                            {hoveredCategory ? (
                                <div className="h-full flex flex-col">
                                    <div className="flex items-start justify-between mb-6">
                                        <h3 className="text-2xl font-bold font-heading uppercase text-primary">
                                            {hoveredCategory.name}
                                        </h3>
                                        <Link
                                            href={isEmpresa ? `/empresa/catalogo?category=${hoveredCategory.slug}` : `/catalogo?category=${hoveredCategory.slug}`}
                                            className="text-xs font-medium bg-primary/10 text-primary px-3 py-1 rounded-full hover:bg-primary/20"
                                        >
                                            Ver todo
                                        </Link>
                                    </div>

                                    {/* Placeholder for subcategories or featured items */}
                                    <div className="grid grid-cols-2 gap-4">
                                        {/* Visual card for the category */}
                                        <div className="aspect-video relative rounded-lg overflow-hidden bg-muted group">
                                            {hoveredCategory.image ? (
                                                <Image
                                                    src={hoveredCategory.image.src}
                                                    alt={hoveredCategory.name}
                                                    fill
                                                    className="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110"
                                                />
                                            ) : (
                                                <div className="flex items-center justify-center h-full text-muted-foreground text-xs">Sin Imagen</div>
                                            )}
                                            <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors" />
                                        </div>

                                        <div className="space-y-2">
                                            <p className="text-sm text-muted-foreground">
                                                Explora nuestra colección de {hoveredCategory.name.toLowerCase()}.
                                                Calidad profesional para tu empresa.
                                            </p>
                                            <ul className="text-sm space-y-1 mt-4">
                                                <li className="flex items-center gap-2 text-foreground/80">
                                                    <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                                                    Equipamiento Certificado
                                                </li>
                                                <li className="flex items-center gap-2 text-foreground/80">
                                                    <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                                                    Stock Disponible
                                                </li>
                                                <li className="flex items-center gap-2 text-foreground/80">
                                                    <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                                                    Envíos a todo Chile
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="h-full flex flex-col items-center justify-center text-center text-muted-foreground opacity-50">
                                    <LayoutGrid className="h-16 w-16 mb-4 stroke-1" />
                                    <p>Selecciona una categoría para ver detalles</p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
