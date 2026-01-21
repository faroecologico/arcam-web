"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAppStore } from "@/store/useStore";
import { getCleanProductName } from "@/lib/woocommerce";
import { Button } from "@/components/ui/button";
import { ShoppingCart, FileText, Minus, Plus, Check } from "lucide-react";

export default function ProductDetail({ product, variants = [] }: { product: any, variants?: any[] }) {
    const { mode, addToCart, addToQuote, openCart } = useAppStore();
    const router = useRouter();
    const isEmpresa = mode === "empresa";
    const [quantity, setQuantity] = useState(1);
    const [selectedImage, setSelectedImage] = useState(product.images[0]?.src || "");

    // Use centralized clean name function
    const baseName = getCleanProductName(product.name);


    const handleAction = () => {
        const item = {
            id: String(product.id),
            name: product.name,
            price: parseFloat(product.price || "0"),
            quantity: quantity,
            image: product.images[0]?.src || "",
        };

        if (isEmpresa) {
            addToQuote(item);
        } else {
            addToCart(item);
        }

        openCart(); // Auto-open drawer
    };

    return (
        <div className="grid gap-8 lg:grid-cols-2">
            {/* IMAGES */}
            <div className="flex flex-col gap-4">
                <div className="relative aspect-square w-full overflow-hidden rounded-xl border bg-muted">
                    {selectedImage ? (
                        <Image
                            src={selectedImage}
                            alt={product.name}
                            fill
                            className="object-cover"
                            priority
                        />
                    ) : (
                        <div className="flex h-full items-center justify-center text-gray-400">Sin Imagen</div>
                    )}
                </div>
                {product.images.length > 1 && (
                    <div className="flex gap-4 overflow-x-auto pb-2">
                        {product.images.map((img: any) => (
                            <button
                                key={img.id}
                                onClick={() => setSelectedImage(img.src)}
                                className={`relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-lg border-2 ${selectedImage === img.src ? 'border-primary' : 'border-transparent'}`}
                            >
                                <Image src={img.src} alt={img.alt} fill className="object-cover" />
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {/* INFO */}
            <div>
                <h1 className="text-3xl font-heading font-bold text-foreground sm:text-4xl mb-2">{baseName}</h1>

                {isEmpresa && (
                    <p className="mt-2 text-sm font-mono text-muted-foreground">SKU: {product.sku}</p>
                )}

                <div className="mt-6">
                    {!isEmpresa ? (
                        <div className="flex items-baseline gap-4">
                            <span className="text-4xl font-bold text-foreground">
                                ${parseInt(product.price || "0").toLocaleString("es-CL")}
                            </span>
                            {product.regular_price !== product.price && (
                                <span className="text-lg text-muted-foreground line-through">
                                    ${parseInt(product.regular_price || "0").toLocaleString("es-CL")}
                                </span>
                            )}
                        </div>
                    ) : (
                        <div className="rounded-lg bg-muted p-4 border border-l-4 border-l-primary">
                            <p className="font-medium text-foreground">Precio sujeto a volumen</p>
                            <p className="text-sm text-muted-foreground">Cotiza para obtener condiciones comerciales.</p>
                        </div>
                    )}
                </div>

                {/* VARIANTS (Linked Products - Dropdown) */}
                {(() => {
                    // Combine variants with current product
                    let allVariants = variants && variants.length > 0 ? [...variants] : [];

                    // Add current product if not in list
                    if (!allVariants.some((v: any) => v.id === product.id)) {
                        allVariants.push(product);
                    }

                    // Sort by name for consistency (optional, but good)
                    allVariants.sort((a, b) => a.name.localeCompare(b.name));

                    // Logic to determine if we should show the selector
                    // Show if > 1 variant, OR if only 1 variant but it has specific info in name differing from baseName
                    const shouldShowSelector = allVariants.length > 1 || (allVariants.length === 1 && allVariants[0].name.replace(/^FERR?E?\.\s*/i, '').trim() !== baseName);

                    if (!shouldShowSelector) return null;

                    return (
                        <div className="mt-6">
                            <label className="text-sm font-medium mb-2 block text-muted-foreground">
                                Selecciona una opción:
                            </label>
                            <div className="relative">
                                <select
                                    className="w-full appearance-none rounded-lg border bg-background px-4 py-3 pr-8 text-sm font-medium shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
                                    value={product.slug}
                                    onChange={(e) => {
                                        const slug = e.target.value;
                                        // If selecting current again, do nothing (or re-nav)
                                        if (slug === product.slug) return;

                                        const linkPrefix = isEmpresa ? "/empresa/producto/" : "/producto/";
                                        router.push(`${linkPrefix}${slug}`);
                                    }}
                                >
                                    {allVariants.map((v: any) => {
                                        // Clean name relative to baseName to show only the differentiator (e.g. "Talla 40")
                                        const cleanName = v.name
                                            .replace(/^FERR?E?\.\s*/i, '') // Remove prefixes first
                                            .replace(baseName, '')       // Remove base name
                                            .replace(/^-/, '')           // Remove leading hyphen
                                            .trim();

                                        // If cleanName is empty (matched baseName exactly), use full cleaned name or "Estándar"
                                        const displayName = cleanName || v.name.replace(/^FERR?E?\.\s*/i, '');

                                        return (
                                            <option key={v.id} value={v.slug}>
                                                {displayName}
                                            </option>
                                        );
                                    })}
                                </select>
                                <div className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6" /></svg>
                                </div>
                            </div>
                        </div>
                    );
                })()}

                <div className="mt-8 space-y-4">
                    {/* QUANTITY */}
                    <div className="flex items-center gap-4">
                        <span className="text-sm font-medium">Cantidad:</span>
                        <div className="flex items-center rounded-md border">
                            <button
                                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                className="p-2 hover:bg-accent"
                            >
                                <Minus className="h-4 w-4" />
                            </button>
                            <span className="w-12 text-center font-medium">{quantity}</span>
                            <button
                                onClick={() => setQuantity(quantity + 1)}
                                className="p-2 hover:bg-accent"
                            >
                                <Plus className="h-4 w-4" />
                            </button>
                        </div>
                    </div>

                    {/* ACTIONS */}
                    <div className="flex gap-4">
                        <Button
                            size="lg"
                            className="flex-1 text-lg"
                            onClick={handleAction}
                            disabled={product.stock_status !== 'instock'}
                        >
                            {isEmpresa ? (
                                <>
                                    <FileText className="mr-2 h-5 w-5" /> Agregar a Cotización
                                </>
                            ) : (
                                <>
                                    <ShoppingCart className="mr-2 h-5 w-5" /> Agregar al Carrito
                                </>
                            )}
                        </Button>
                    </div>

                    {product.stock_status === 'instock' && (
                        <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400">
                            <Check className="h-4 w-4" /> Disponible en bodega
                        </div>
                    )}
                </div>

                <div className="mt-8 border-t pt-8">
                    <h3 className="font-bold mb-4">Descripción</h3>
                    <div className="prose dark:prose-invert max-w-none text-sm text-muted-foreground">
                        <p>{baseName}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
