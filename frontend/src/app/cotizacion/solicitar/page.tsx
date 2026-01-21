"use client";

import { useState } from "react";
import { useAppStore } from "@/store/useStore";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { Loader2, ArrowLeft, User, Briefcase, FileText, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function QuoteRequestPage() {
    // --- AUTH GUARD: REQUIRE LOGIN TO QUOTE ---
    const { quoteCart, clearQuote, isAuthenticated, user } = useAppStore();
    const router = useRouter();
    const [loading, setLoading] = useState(false);

    // Form fields for B2B Quote - Pre-fill with user data if available
    const [formData, setFormData] = useState({
        firstName: user?.firstName || "",
        lastName: user?.lastName || "",
        email: user?.email || "",
        phone: user?.phone || "",
        company: user?.company || "",
        rut: "",
        address: "",
        city: "",
        message: ""
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // --- REDIRECT IF EMPTY CART ---
    if (quoteCart.length === 0) {
        if (typeof window !== 'undefined') router.push("/empresa/catalogo");
        return null; // Don't render anything while redirecting
    }

    // --- REQUIRE AUTH VIEW ---
    if (!isAuthenticated) {
        return (
            <div className="container flex min-h-[60vh] items-center justify-center py-12 px-4">
                <div className="w-full max-w-lg rounded-2xl border bg-card p-8 shadow-xl text-center dark:bg-slate-900 dark:border-slate-800">
                    <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-primary/10">
                        <User className="h-10 w-10 text-primary" />
                    </div>
                    <h1 className="mb-3 text-2xl font-bold font-heading">Inicia Sesión para Cotizar</h1>
                    <p className="mb-8 text-muted-foreground">
                        Para generar una cotización formal y enviarla a nuestro equipo de ventas, necesitamos tener tus datos de contacto registrados.
                    </p>

                    <div className="grid gap-4">
                        <Link href={`/login?redirect=/cotizacion/solicitar`}>
                            <Button size="lg" className="w-full font-bold">
                                Iniciar Sesión Existente
                            </Button>
                        </Link>
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <span className="w-full border-t border-muted"></span>
                            </div>
                            <div className="relative flex justify-center text-xs uppercase">
                                <span className="bg-card px-2 text-muted-foreground">O si eres nuevo</span>
                            </div>
                        </div>
                        <Link href={`/registro?redirect=/cotizacion/solicitar`}>
                            <Button variant="outline" size="lg" className="w-full">
                                Crear Cuenta de Empresa
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    // --- SUBMIT HANDLER ---
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        const orderData = {
            payment_method: "b2b_quote",
            payment_method_title: "Solicitud de Cotización Formal",
            set_paid: false,
            status: "on-hold",
            billing: {
                first_name: formData.firstName,
                last_name: formData.lastName,
                company: formData.company,
                email: formData.email,
                phone: formData.phone,
                address_1: formData.address,
                city: formData.city,
            },
            shipping: {
                first_name: formData.firstName,
                last_name: formData.lastName,
                company: formData.company,
                address_1: formData.address,
                city: formData.city,
            },
            line_items: quoteCart.map(item => ({
                product_id: parseInt(item.id),
                quantity: item.quantity,
            })),
            meta_data: [
                { key: "order_type", value: "B2B_QUOTE" },
                { key: "customer_rut", value: formData.rut },
                { key: "quote_message", value: formData.message }
            ]
        };

        try {
            const res = await fetch("/api/checkout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(orderData),
            });

            if (!res.ok) throw new Error("Error submitting quote");

            const result = await res.json();
            clearQuote();
            router.push(`/order-received?id=${result.id}&type=quote`);

        } catch (error) {
            console.error(error);
            alert("Hubo un error al enviar la solicitud. Intenta nuevamente.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container max-w-3xl py-12 px-4">
            <Link href="/cotizacion" className="flex items-center text-sm text-muted-foreground hover:text-primary mb-8 transition-colors">
                <ArrowLeft className="mr-2 h-4 w-4" /> Volver al resumen
            </Link>

            <div className="flex items-center gap-4 mb-8">
                <div className="h-12 w-1 bg-primary rounded-full"></div>
                <div>
                    <h1 className="text-3xl font-heading font-bold uppercase text-foreground dark:text-slate-100">
                        Finalizar Cotización
                    </h1>
                    <p className="text-muted-foreground">
                        Confirma los datos de tu empresa para la emisión formal del documento.
                    </p>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8 rounded-xl border bg-card p-8 shadow-lg dark:bg-slate-900 dark:border-slate-800">

                {/* Contact Info Section */}
                <div>
                    <h3 className="text-lg font-bold flex items-center gap-2 mb-4 text-foreground dark:text-slate-200">
                        <User className="h-5 w-5 text-primary" /> Datos de Contacto
                    </h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Nombre</label>
                            <Input required name="firstName" value={formData.firstName} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Apellido</label>
                            <Input required name="lastName" value={formData.lastName} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                        </div>
                    </div>
                    <div className="grid gap-4 sm:grid-cols-2 mt-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Email Corporativo</label>
                            <Input required type="email" name="email" value={formData.email} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Teléfono / Celular</label>
                            <Input required type="tel" name="phone" value={formData.phone} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                        </div>
                    </div>
                </div>

                <div className="border-t border-border dark:border-slate-800"></div>

                {/* Company Info Section */}
                <div>
                    <h3 className="text-lg font-bold flex items-center gap-2 mb-4 text-foreground dark:text-slate-200">
                        <Briefcase className="h-5 w-5 text-primary" /> Información de Facturación
                    </h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Razón Social</label>
                            <Input required name="company" placeholder="Nombre Fantasía SpA" value={formData.company} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">RUT Empresa</label>
                            <Input required name="rut" placeholder="76.123.456-K" value={formData.rut} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                        </div>
                    </div>
                    <div className="space-y-2 mt-4">
                        <label className="text-sm font-medium">Dirección Comercial</label>
                        <Input required name="address" placeholder="Av. Industrial #123, Oficina 404" value={formData.address} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                    </div>
                    <div className="space-y-2 mt-4">
                        <label className="text-sm font-medium">Ciudad / Comuna</label>
                        <Input required name="city" placeholder="Santiago" value={formData.city} onChange={handleChange} className="bg-background dark:bg-slate-950" />
                    </div>
                </div>

                <div className="border-t border-border dark:border-slate-800"></div>

                {/* Additional Info */}
                <div className="space-y-2">
                    <label className="text-sm font-medium flex items-center gap-2">
                        <FileText className="h-4 w-4" /> Comentarios Adicionales (Opcional)
                    </label>
                    <textarea
                        name="message"
                        rows={3}
                        className="flex w-full rounded-md border border-input bg-background dark:bg-slate-950 px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        placeholder="Necesito adjuntar OC, especificaciones técnicas, etc."
                        onChange={handleChange}
                        value={formData.message}
                    />
                </div>

                <Button type="submit" size="lg" className="w-full text-lg h-14 font-bold shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-shadow" disabled={loading}>
                    {loading ? <Loader2 className="animate-spin mr-2" /> : "Enviar Solicitud"}
                    {!loading && <ArrowRight className="ml-2 h-5 w-5" />}
                </Button>
            </form>
        </div>
    );
}
