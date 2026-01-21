"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "../ui/button";
import { Checkbox } from "../ui/checkbox";
import { Label } from "../ui/label";
import { Filter, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Category {
    id: number;
    name: string;
    slug: string;
    count?: number;
}

interface CategorySidebarProps {
    categories: Category[];
    className?: string;
}

export default function CategorySidebar({ categories, className }: CategorySidebarProps) {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
    const [isOpen, setIsOpen] = useState(false); // Mobile toggle

    // Sync state with URL params
    useEffect(() => {
        const catParam = searchParams.get("categories");
        if (catParam) {
            setSelectedCategories(catParam.split(","));
        } else {
            setSelectedCategories([]);
        }
    }, [searchParams]);

    const toggleCategory = (slug: string) => {
        const newSelection = selectedCategories.includes(slug)
            ? selectedCategories.filter((s) => s !== slug)
            : [...selectedCategories, slug];

        setSelectedCategories(newSelection);
        updateUrl(newSelection);
    };

    const updateUrl = (selection: string[]) => {
        const params = new URLSearchParams(searchParams.toString());
        if (selection.length > 0) {
            params.set("categories", selection.join(","));
        } else {
            params.delete("categories");
        }
        // Reset page if filtering changes
        params.delete("page");

        router.push(`?${params.toString()}`);
    };

    const clearFilters = () => {
        setSelectedCategories([]);
        updateUrl([]);
    };

    // Priority categories requested by user
    const prioritySlugs = ["ropa-de-trabajo", "ferreteria", "materiales-de-construccion", "epp"];

    // Sort logic: Priority first, then alphabetical
    const sortedCategories = [...categories].sort((a, b) => {
        const aP = prioritySlugs.indexOf(a.slug);
        const bP = prioritySlugs.indexOf(b.slug);

        if (aP !== -1 && bP !== -1) return aP - bP;
        if (aP !== -1) return -1;
        if (bP !== -1) return 1;

        return a.name.localeCompare(b.name);
    });

    return (
        <>
            {/* Mobile Trigger */}
            <Button
                variant="outline"
                className="lg:hidden w-full mb-4 flex gap-2"
                onClick={() => setIsOpen(!isOpen)}
            >
                <Filter className="h-4 w-4" />
                {isOpen ? "Ocultar Filtros" : "Mostrar Filtros"}
            </Button>

            {/* Sidebar Content */}
            <div className={cn(
                "w-full lg:w-64 flex-shrink-0 space-y-6 transition-all duration-300",
                className,
                isOpen ? "block" : "hidden lg:block"
            )}>
                <div>
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-heading font-bold text-lg">Categorías</h3>
                        {selectedCategories.length > 0 && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={clearFilters}
                                className="h-auto px-2 text-xs text-muted-foreground hover:text-destructive"
                            >
                                Limpiar
                            </Button>
                        )}
                    </div>

                    <div className="space-y-3">
                        {sortedCategories.map((cat) => (
                            <div key={cat.id} className="flex items-center space-x-3">
                                <Checkbox
                                    id={`cat-${cat.id}`}
                                    checked={selectedCategories.includes(cat.slug)}
                                    onCheckedChange={() => toggleCategory(cat.slug)}
                                />
                                <Label
                                    htmlFor={`cat-${cat.id}`}
                                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer flex-1"
                                >
                                    {cat.name}
                                </Label>
                                {cat.count !== undefined && (
                                    <span className="text-xs text-muted-foreground tabular-nums">
                                        ({cat.count})
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Banner / Ad placeholder could go here */}
                <div className="p-4 bg-muted/50 rounded-xl border border-dashed border-border/60 text-center">
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-1">
                        ¿Necesitas ayuda?
                    </p>
                    <p className="text-sm">
                        Contacta a ventas para cotizaciones especiales.
                    </p>
                </div>
            </div>
        </>
    );
}
