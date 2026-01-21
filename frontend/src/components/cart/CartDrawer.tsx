"use client";

import { useAppStore } from "@/store/useStore";
import { motion, AnimatePresence } from "framer-motion";
import { X, ShoppingCart, FileText, Trash2, Plus, Minus } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export function CartDrawer() {
    const {
        mode,
        isCartOpen,
        closeCart,
        cart,
        removeFromCart,
        quoteCart,
        removeFromQuote,
        addToCart,
        addToQuote
    } = useAppStore();
    const router = useRouter(); // Initialize router

    const isEmpresa = mode === "empresa";
    const items = isEmpresa ? quoteCart : cart;

    const total = items.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    const totalItems = items.reduce((acc, item) => acc + item.quantity, 0);

    const increment = (item: any) => {
        const newItem = { ...item, quantity: 1 };
        isEmpresa ? addToQuote(newItem) : addToCart(newItem);
    };

    const decrement = (item: any) => {
        // Custom logic to decrement? Store `addToCart` adds to current, so sending negative? 
        // No, `addToCart` logic in `useStore` adds quantity. To decrement we need a separate action or modify `addToCart` logic.
        // For simplicity in MVP, let's just allow removing or adding. 
        // Or better, let's assume `addToCart` with negative quantity works if we didn't guard against it?
        // Looking at `useStore`: `quantity: i.quantity + item.quantity`. Yes, sending -1 works.
        const newItem = { ...item, quantity: -1 };
        // Prevent going below 1 here or let store handle removing?
        if (item.quantity > 1) {
            isEmpresa ? addToQuote(newItem) : addToCart(newItem);
        } else {
            isEmpresa ? removeFromQuote(item.id) : removeFromCart(item.id);
        }
    };

    return (
        <AnimatePresence>
            {isCartOpen && (
                <>
                    {/* BACKDROP */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={closeCart}
                        className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm"
                    />

                    {/* DRAWER */}
                    <motion.div
                        initial={{ x: "100%" }}
                        animate={{ x: 0 }}
                        exit={{ x: "100%" }}
                        transition={{ type: "spring", damping: 25, stiffness: 200 }}
                        className="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col border-l bg-background shadow-xl sm:max-w-lg"
                    >
                        {/* HEADER */}
                        <div className="flex items-center justify-between border-b px-4 py-4">
                            <h2 className="flex items-center gap-2 text-lg font-bold">
                                {isEmpresa ? <FileText /> : <ShoppingCart />}
                                {isEmpresa ? "Cotización" : "Mi Carrito"}
                                <span className="text-sm font-normal text-muted-foreground">({totalItems} ítems)</span>
                            </h2>
                            <Button variant="ghost" size="icon" onClick={closeCart}>
                                <X className="h-5 w-5" />
                            </Button>
                        </div>

                        {/* LIST */}
                        <div className="flex-1 overflow-y-auto p-4">
                            {items.length === 0 ? (
                                <div className="flex h-full flex-col items-center justify-center space-y-4 text-center text-muted-foreground">
                                    {isEmpresa ? <FileText className="h-16 w-16 opacity-20" /> : <ShoppingCart className="h-16 w-16 opacity-20" />}
                                    <p>Tu {isEmpresa ? "cotización" : "carrito"} está vacío.</p>
                                    <Button variant="link" onClick={closeCart}>Seguir explorando</Button>
                                </div>
                            ) : (
                                <ul className="space-y-4">
                                    {items.map((item) => (
                                        <li key={item.id} className="flex gap-4">
                                            <div className="relative h-20 w-20 overflow-hidden rounded-md border bg-muted">
                                                {item.image && <Image src={item.image} alt={item.name} fill className="object-cover" />}
                                            </div>
                                            <div className="flex flex-1 flex-col justify-between">
                                                <div className="flex justify-between">
                                                    <h3 className="line-clamp-2 text-sm font-medium">{item.name}</h3>
                                                    <button onClick={() => isEmpresa ? removeFromQuote(item.id) : removeFromCart(item.id)} className="text-muted-foreground hover:text-destructive">
                                                        <Trash2 className="h-4 w-4" />
                                                    </button>
                                                </div>
                                                <div className="flex items-center justify-between mt-2">
                                                    <div className="flex items-center rounded-md border h-8">
                                                        <button onClick={() => decrement(item)} className="px-2 hover:bg-muted"><Minus className="h-3 w-3" /></button>
                                                        <span className="px-2 text-xs font-medium">{item.quantity}</span>
                                                        <button onClick={() => increment(item)} className="px-2 hover:bg-muted"><Plus className="h-3 w-3" /></button>
                                                    </div>
                                                    {!isEmpresa && (
                                                        <p className="font-bold text-sm">
                                                            ${(item.price * item.quantity).toLocaleString("es-CL")}
                                                        </p>
                                                    )}
                                                </div>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>

                        {/* FOOTER */}
                        <div className="border-t bg-muted/40 p-4">
                            {!isEmpresa && items.length > 0 && (
                                <div className="mb-4 flex items-center justify-between text-lg font-bold">
                                    <span>Total estimado</span>
                                    <span>${total.toLocaleString("es-CL")}</span>
                                </div>
                            )}

                            <Button
                                className="w-full"
                                size="lg"
                                disabled={items.length === 0}
                                onClick={() => {
                                    closeCart();
                                    if (isEmpresa) {
                                        router.push("/cotizacion");
                                    } else {
                                        router.push("/checkout");
                                    }
                                }}
                            >
                                {isEmpresa ? "Ver Cotización" : "Ir a Pagar"}
                            </Button>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
