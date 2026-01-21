"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useAppStore } from "@/store/useStore";
import { Search, ShoppingCart, FileText, Menu, User, LogIn, UserPlus, X, ChevronRight, TrendingUp } from "lucide-react";
import DualToggle from "./DualToggle";
import { Button } from "../ui/button";
import MegaMenu from "./MegaMenu";
import { useState, useEffect, useRef } from "react";
import { AnimatePresence, motion } from "framer-motion";

export function Header({ categories = [], forcedMode }: { categories?: any[], forcedMode?: "persona" | "empresa" }) {
    const mode = useAppStore((state) => state.mode);
    const cart = useAppStore((state) => state.cart);
    const quoteCart = useAppStore((state) => state.quoteCart);
    const openCart = useAppStore((state) => state.openCart);
    const effectiveMode = forcedMode || mode;
    const isEmpresa = effectiveMode === "empresa";
    const [isUserOpen, setIsUserOpen] = useState(false);
    const [userDropdownTimer, setUserDropdownTimer] = useState<NodeJS.Timeout | null>(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [suggestions, setSuggestions] = useState<any[]>([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [isSearchFocused, setIsSearchFocused] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(-1);
    const inputRef = useRef<HTMLInputElement>(null);
    const router = useRouter();

    // Debounced search effect
    useEffect(() => {
        const timer = setTimeout(async () => {
            if (searchQuery.length >= 3) {
                setIsLoading(true);
                try {
                    const res = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
                    if (res.ok) {
                        const data = await res.json();
                        setSuggestions(data);
                        setShowSuggestions(true);
                        setSelectedIndex(-1);
                    }
                } catch (error) {
                    console.error("Search fetch error", error);
                } finally {
                    setIsLoading(false);
                }
            } else {
                setSuggestions([]);
                setShowSuggestions(false);
                setSelectedIndex(-1);
            }
        }, 300);

        return () => clearTimeout(timer);
    }, [searchQuery]);

    const totalItems = isEmpresa
        ? quoteCart.reduce((acc, item) => acc + item.quantity, 0)
        : cart.reduce((acc, item) => acc + item.quantity, 0);

    // Auth dropdown handlers with delay
    const handleUserMouseEnter = () => {
        if (userDropdownTimer) clearTimeout(userDropdownTimer);
        setIsUserOpen(true);
    };

    const handleUserMouseLeave = () => {
        const timer = setTimeout(() => setIsUserOpen(false), 500); // 500ms grace period
        setUserDropdownTimer(timer);
    };

    const toggleUserDropdown = () => {
        setIsUserOpen(!isUserOpen);
    };

    const handleSearch = () => {
        if (!searchQuery.trim()) return;
        setShowSuggestions(false);
        setIsSearchFocused(false);

        const targetPath = isEmpresa ? "/catalogo" : "/catalogo"; // Simplified logic as per component
        const query = `?search=${encodeURIComponent(searchQuery)}`;

        router.push(`${targetPath}${query}`);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
                const product = suggestions[selectedIndex];
                const url = isEmpresa ? `/empresa/producto/${product.slug}` : `/producto/${product.slug}`;
                router.push(url);
                setShowSuggestions(false);
                setIsSearchFocused(false);
            } else {
                handleSearch();
            }
        } else if (e.key === "ArrowDown") {
            e.preventDefault();
            setSelectedIndex((prev) => (prev + 1) % suggestions.length);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            setSelectedIndex((prev) => (prev - 1 + suggestions.length) % suggestions.length);
        } else if (e.key === "Escape") {
            setShowSuggestions(false);
            setIsSearchFocused(false);
            inputRef.current?.blur();
        }
    };

    return (
        <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md transition-colors duration-300">
            <div className="container flex h-16 items-center justify-between px-4">
                {/* LOGO */}
                <Link href="/" className="mr-6 flex items-center space-x-2">
                    <div className="relative h-12 w-32">
                        <Image
                            src={isEmpresa ? "/images/logo-arcam-white.png" : "/images/logo-arcam.png"}
                            alt="ARCAM Logo"
                            fill
                            sizes="(max-width: 768px) 100px, 128px"
                            className="object-contain"
                            priority
                        />
                    </div>
                </Link>

                {/* SEARCH */}
                <div className="hidden flex-1 md:flex md:items-center md:gap-6 justify-center">
                    <div className="relative w-full max-w-lg group">
                        <div className="relative transition-all duration-300 focus-within:ring-2 focus-within:ring-primary/50  focus-within:shadow-lg rounded-full">
                            < Button
                                variant="ghost"
                                size="icon"
                                className="absolute left-1 top-1/2 -translate-y-1/2 h-8 w-8 text-muted-foreground hover:bg-transparent"
                                onClick={handleSearch}
                            >
                                <Search className="h-4 w-4" />
                            </Button>
                            <input
                                type="search"
                                placeholder={isEmpresa ? "Buscar productos por SKU..." : "Buscar ropa de trabajo, EPP..."}
                                className="w-full rounded-full border border-border bg-muted/40 backdrop-blur-sm pl-10 pr-10 py-2.5 text-sm transition-all focus:bg-background focus:outline-none placeholder:text-muted-foreground/70"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyDown={handleKeyDown}
                                onFocus={() => setIsSearchFocused(true)}
                                onBlur={() => setTimeout(() => setIsSearchFocused(false), 200)}
                            />
                            {searchQuery && (
                                <button
                                    onClick={() => {
                                        setSearchQuery("");
                                        setSuggestions([]);
                                        inputRef.current?.focus();
                                    }}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                                >
                                    <X className="h-4 w-4" />
                                </button>
                            )}
                        </div>

                        {/* Enhanced Dropdown */}
                        <AnimatePresence>
                            {isSearchFocused && (
                                <motion.div
                                    initial={{ opacity: 0, y: 10, scale: 0.98 }}
                                    animate={{ opacity: 1, y: 0, scale: 1 }}
                                    exit={{ opacity: 0, y: 10, scale: 0.98 }}
                                    transition={{ duration: 0.2 }}
                                    className="absolute top-full left-0 mt-2 w-[120%] -left-[10%] bg-white/95 dark:bg-slate-950/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/10 dark:border-white/5 overflow-hidden z-[60]"
                                >
                                    <div className="p-2">
                                        {/* Loading State */}
                                        {isLoading ? (
                                            <div className="p-4 space-y-3">
                                                <div className="flex items-center gap-3 animate-pulse">
                                                    <div className="h-10 w-10 bg-muted rounded-lg" />
                                                    <div className="space-y-2 flex-1">
                                                        <div className="h-4 bg-muted rounded w-3/4" />
                                                        <div className="h-3 bg-muted rounded w-1/2" />
                                                    </div>
                                                </div>
                                                <div className="flex items-center gap-3 animate-pulse">
                                                    <div className="h-10 w-10 bg-muted rounded-lg" />
                                                    <div className="space-y-2 flex-1">
                                                        <div className="h-4 bg-muted rounded w-3/4" />
                                                        <div className="h-3 bg-muted rounded w-1/2" />
                                                    </div>
                                                </div>
                                            </div>
                                        ) : searchQuery.length < 2 ? (
                                            // Empty State / Trending
                                            <div className="p-4">
                                                <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
                                                    <TrendingUp className="h-3 w-3" />
                                                    Tendencias
                                                </div>
                                                <div className="flex flex-wrap gap-2">
                                                    {["Zapatos de Seguridad", "Cascos", "Polar", "Chaleco Geólogo"].map((term) => (
                                                        <button
                                                            key={term}
                                                            onClick={() => {
                                                                setSearchQuery(term);
                                                                inputRef.current?.focus();
                                                            }}
                                                            className="px-3 py-1.5 bg-muted/50 hover:bg-primary/10 hover:text-primary text-sm rounded-full transition-colors"
                                                        >
                                                            {term}
                                                        </button>
                                                    ))}
                                                </div>
                                            </div>
                                        ) : suggestions.length > 0 ? (
                                            // Results
                                            <>
                                                <div className="px-3 py-2 text-xs font-semibold text-muted-foreground border-b border-border/50">
                                                    Productos Sugeridos
                                                </div>
                                                <div className="py-1">
                                                    {suggestions.map((product, index) => (
                                                        <Link
                                                            key={product.id}
                                                            href={isEmpresa ? `/empresa/producto/${product.slug}` : `/producto/${product.slug}`}
                                                            onClick={() => setShowSuggestions(false)}
                                                            className={`
                                                                flex items-center gap-4 p-3 rounded-xl transition-all group
                                                                ${index === selectedIndex ? 'bg-primary/10' : 'hover:bg-muted/50'}
                                                            `}
                                                        >
                                                            <div className="relative h-12 w-12 flex-shrink-0 bg-white rounded-lg overflow-hidden border border-border/50 shadow-sm group-hover:scale-105 transition-transform">
                                                                <Image
                                                                    src={product.image}
                                                                    alt={product.name}
                                                                    fill
                                                                    className="object-cover"
                                                                />
                                                            </div>
                                                            <div className="flex-1 min-w-0">
                                                                <p className="text-sm font-medium text-foreground truncate group-hover:text-primary transition-colors">
                                                                    {product.name}
                                                                </p>
                                                                {product.price && (
                                                                    <p className="text-xs text-muted-foreground font-mono mt-0.5">
                                                                        {new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(product.price)}
                                                                    </p>
                                                                )}
                                                            </div>
                                                            <ChevronRight className={`h-4 w-4 text-muted-foreground transition-transform ${index === selectedIndex ? 'translate-x-1 text-primary' : 'group-hover:translate-x-1'}`} />
                                                        </Link>
                                                    ))}
                                                </div>
                                                <button
                                                    onClick={handleSearch}
                                                    className="w-full p-3 text-center text-sm font-medium text-primary hover:bg-primary/5 transition-colors border-t border-border/50"
                                                >
                                                    Ver todos los resultados para "{searchQuery}"
                                                </button>
                                            </>
                                        ) : (
                                            // No Results
                                            <div className="p-8 text-center text-muted-foreground">
                                                <Search className="h-8 w-8 mx-auto mb-3 opacity-50" />
                                                <p className="text-sm">No encontramos productos para "{searchQuery}"</p>
                                            </div>
                                        )}
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                    <nav className="flex items-center gap-8 text-sm font-medium">
                        <Link href="/" className="transition-colors hover:text-primary">
                            Inicio
                        </Link>

                        {/* Mega Menu Integration */}
                        <MegaMenu categories={categories} />

                        <Link href="/nosotros" className="transition-colors hover:text-primary">
                            Nosotros
                        </Link>
                    </nav>
                </div>

                {/* ACTIONS */}
                <div className="flex items-center gap-2 md:gap-4">
                    <div>
                        <DualToggle />
                    </div>

                    {/* AUTH BUBBLE */}
                    <div
                        className="relative hidden md:block"
                        onMouseEnter={handleUserMouseEnter}
                        onMouseLeave={handleUserMouseLeave}
                    >
                        <Button
                            variant="ghost"
                            size="icon"
                            className="relative rounded-full hover:bg-muted"
                            onClick={toggleUserDropdown}
                        >
                            <User className="h-5 w-5" />
                        </Button>

                        {isUserOpen && (
                            <div className="absolute right-0 top-full mt-2 w-48 rounded-md border bg-white dark:bg-slate-950 p-2 shadow-lg ring-1 ring-black/5 z-50 animate-in fade-in zoom-in-95 duration-200">
                                <Link href="/login" className="flex items-center gap-2 rounded px-3 py-2 text-sm hover:bg-muted transition-colors">
                                    <LogIn className="h-4 w-4" />
                                    <span>Iniciar Sesión</span>
                                </Link>
                                <Link href="/registro" className="flex items-center gap-2 rounded px-3 py-2 text-sm hover:bg-muted transition-colors">
                                    <UserPlus className="h-4 w-4" />
                                    <span>Registrarse</span>
                                </Link>
                            </div>
                        )}
                    </div>

                    <Button
                        variant="ghost"
                        size="icon"
                        className="relative"
                        onClick={openCart}
                    >
                        {isEmpresa ? <FileText className="h-5 w-5" /> : <ShoppingCart className="h-5 w-5" />}
                        {totalItems > 0 && (
                            <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-[10px] text-white">
                                {totalItems}
                            </span>
                        )}
                    </Button>

                    <Button variant="ghost" size="icon" className="md:hidden">
                        <Menu className="h-5 w-5" />
                    </Button>
                </div>
            </div>
        </header>
    );
}
