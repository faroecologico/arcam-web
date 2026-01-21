"use client";

import { useState } from "react";
import { useAppStore } from "@/store/useStore";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function CheckoutPage() {
    const { cart, clearCart } = useAppStore();
    const router = useRouter();
    const items = cart;

    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        phone: "",
        address: "",
        city: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        const orderData = {
            payment_method: "cod", // Placeholder for B2C payment
            payment_method_title: "Transferencia / Pagos varios",
            set_paid: false,
            status: "processing",
            billing: {
                first_name: formData.firstName,
                last_name: formData.lastName,
                address_1: formData.address,
                city: formData.city,
                email: formData.email,
                phone: formData.phone,
            },
            shipping: {
                first_name: formData.firstName,
                last_name: formData.lastName,
                address_1: formData.address,
                city: formData.city,
            },
            line_items: items.map(item => ({
                product_id: parseInt(item.id),
                quantity: item.quantity,
            })),
            meta_data: [
                { key: "order_type", value: "B2C_SALE" }
            ]
        };

        try {
            const res = await fetch("/api/checkout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(orderData),
            });

            if (!res.ok) throw new Error("Error submitting order");

            const result = await res.json();
            clearCart();
            router.push(`/order-received?id=${result.id}&type=order`);

        } catch (error) {
            console.error(error);
            alert("Hubo un error al procesar tu pedido.");
        } finally {
            setLoading(false);
        }
    };

    if (items.length === 0) {
        return (
            <div className="container flex min-h-[50vh] flex-col items-center justify-center">
                <h2 className="text-2xl font-bold">Tu carro está vacío</h2>
                <Button onClick={() => router.push("/catalogo")} className="mt-4">Volver al Catálogo</Button>
            </div>
        );
    }

    return (
        <div className="container max-w-2xl py-8">
            <h1 className="mb-8 text-3xl font-bold font-heading uppercase">
                Finalizar Compra
            </h1>

            <form onSubmit={handleSubmit} className="space-y-6 rounded-lg border p-6 bg-card shadow-sm">
                <div className="grid gap-4 sm:grid-cols-2">
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Nombre</label>
                        <Input required name="firstName" placeholder="Juan" onChange={handleChange} />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Apellido</label>
                        <Input required name="lastName" placeholder="Pérez" onChange={handleChange} />
                    </div>
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium">Email</label>
                    <Input required type="email" name="email" placeholder="juan@ejemplo.com" onChange={handleChange} />
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium">Teléfono</label>
                    <Input required type="tel" name="phone" placeholder="+56 9 1234 5678" onChange={handleChange} />
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium">Dirección de Despacho</label>
                    <Input required name="address" placeholder="Av. Principal 123" onChange={handleChange} />
                </div>

                <div className="space-y-2">
                    <label className="text-sm font-medium">Ciudad / Comuna</label>
                    <Input required name="city" placeholder="Santiago" onChange={handleChange} />
                </div>

                <div className="mt-8 border-t pt-6">
                    <h3 className="mb-4 font-bold text-lg">Resumen</h3>
                    <ul className="mb-4 space-y-2 text-sm text-foreground">
                        {items.map(i => (
                            <li key={i.id} className="flex justify-between">
                                <span>{i.quantity} x {i.name}</span>
                                <span className="font-semibold">${(i.price * i.quantity).toLocaleString("es-CL")}</span>
                            </li>
                        ))}
                    </ul>
                    <div className="flex justify-between text-xl font-bold border-t pt-2 text-primary">
                        <span>Total</span>
                        <span>${items.reduce((acc, i) => acc + (i.price * i.quantity), 0).toLocaleString("es-CL")}</span>
                    </div>
                </div>

                <Button type="submit" size="lg" className="w-full" disabled={loading}>
                    {loading ? <Loader2 className="animate-spin" /> : "Confirmar Pedido"}
                </Button>
            </form>
        </div>
    );
}
