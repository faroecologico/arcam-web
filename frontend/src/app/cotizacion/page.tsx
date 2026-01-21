"use client";

import { useAppStore } from "@/store/useStore";
import { Button } from "@/components/ui/button";
import { Trash2, ArrowRight } from "lucide-react";
import Link from "next/link";
import Image from "next/image";

export default function QuotePage() {
    const { quoteCart, removeFromQuote, updateQuoteQuantity } = useAppStore();

    if (quoteCart.length === 0) {
        return (
            <div className="container flex min-h-[50vh] flex-col items-center justify-center p-4 text-center">
                <h2 className="text-2xl font-bold mb-4">Lista de Cotización Vacía</h2>
                <p className="text-muted-foreground mb-6">Agrega productos del catálogo industrial para solicitar una cotización formal.</p>
                <Link href="/empresa/catalogo">
                    <Button>Ir al Catálogo Industrial</Button>
                </Link>
            </div>
        );
    }

    return (
        <div className="container max-w-4xl py-12 px-4">
            <h1 className="mb-2 text-3xl font-heading font-bold uppercase text-primary">Solicitud de Cotización</h1>
            <p className="mb-8 text-muted-foreground">Revisa los ítems antes de enviar tu solicitud a nuestro equipo de ventas.</p>

            <div className="rounded-lg border bg-card shadow-sm dark:border-slate-800">
                <div className="p-6 space-y-6">
                    {quoteCart.map((item) => (
                        <div key={item.id} className="flex items-center gap-4 border-b pb-6 last:border-0 last:pb-0">
                            <div className="relative h-20 w-20 overflow-hidden rounded-md bg-muted">
                                {item.image ? (
                                    <Image src={item.image} alt={item.name} fill className="object-cover" />
                                ) : (
                                    <div className="flex h-full w-full items-center justify-center text-xs text-muted-foreground">Sin Foto</div>
                                )}
                            </div>

                            <div className="flex-1 min-w-0">
                                <h3 className="font-medium text-lg leading-tight">{item.name}</h3>
                                <p className="text-sm text-muted-foreground mt-1">SKU: {item.id}</p>
                            </div>

                            <div className="flex items-center gap-4">
                                <div className="flex items-center rounded-md border bg-background">
                                    <button
                                        className="px-3 py-1 hover:bg-muted"
                                        onClick={() => updateQuoteQuantity(item.id, Math.max(1, item.quantity - 1))}
                                    >-</button>
                                    <span className="w-12 text-center text-sm font-medium">{item.quantity}</span>
                                    <button
                                        className="px-3 py-1 hover:bg-muted"
                                        onClick={() => updateQuoteQuantity(item.id, item.quantity + 1)}
                                    >+</button>
                                </div>

                                <Button variant="ghost" size="icon" onClick={() => removeFromQuote(item.id)} className="text-destructive hover:text-destructive hover:bg-destructive/10">
                                    <Trash2 className="h-5 w-5" />
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="border-t p-6 dark:border-slate-800 bg-muted/20">
                    <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                        <Link href="/empresa/catalogo" className="text-sm font-medium text-muted-foreground hover:text-primary">
                            &larr; Agregar más productos
                        </Link>
                        <Link href="/cotizacion/solicitar">
                            <Button size="lg" className="w-full sm:w-auto">
                                Continuar a Datos de Empresa <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
