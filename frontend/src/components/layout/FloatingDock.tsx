"use client";

import Link from "next/link";
import { useAppStore } from "@/store/useStore";
import { Home, Search, ShoppingCart, FileText, User } from "lucide-react";

export function FloatingDock() {
    const { mode, cart, quoteCart, openCart } = useAppStore();
    const isEmpresa = mode === "empresa";

    const totalItems = isEmpresa
        ? quoteCart.reduce((acc, item) => acc + item.quantity, 0)
        : cart.reduce((acc, item) => acc + item.quantity, 0);

    return (
        <div className="fixed bottom-4 left-1/2 z-50 w-[90%] max-w-sm -translate-x-1/2 rounded-full border bg-background/70 p-2 shadow-lg backdrop-blur-lg md:hidden">
            <nav className="flex items-center justify-around">
                <Link href="/" className="flex flex-col items-center gap-1 p-2 text-muted-foreground hover:text-primary">
                    <Home className="h-5 w-5" />
                    <span className="text-[10px] font-medium">Inicio</span>
                </Link>

                <Link href="/buscar" className="flex flex-col items-center gap-1 p-2 text-muted-foreground hover:text-primary">
                    <Search className="h-5 w-5" />
                    <span className="text-[10px] font-medium">Buscar</span>
                </Link>

                <button
                    onClick={openCart}
                    className="relative flex flex-col items-center gap-1 p-2 text-muted-foreground hover:text-primary"
                >
                    <div className="relative">
                        {isEmpresa ? <FileText className="h-5 w-5" /> : <ShoppingCart className="h-5 w-5" />}
                        {totalItems > 0 && (
                            <span className="absolute -right-2 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[9px] text-white">
                                {totalItems}
                            </span>
                        )}
                    </div>
                    <span className="text-[10px] font-medium">{isEmpresa ? "Cotizar" : "Carrito"}</span>
                </button>

                <Link href="/perfil" className="flex flex-col items-center gap-1 p-2 text-muted-foreground hover:text-primary">
                    <User className="h-5 w-5" />
                    <span className="text-[10px] font-medium">Perfil</span>
                </Link>
            </nav>
        </div>
    );
}
