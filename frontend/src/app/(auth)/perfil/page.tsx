"use client";

import { useAppStore } from "@/store/useStore";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function ProfilePage() {
    const { mode } = useAppStore();
    const router = useRouter();
    const [loading, setLoading] = useState(true);

    // Mock Login Check
    useEffect(() => {
        const timer = setTimeout(() => {
            setLoading(false);
        }, 500);
        return () => clearTimeout(timer);
    }, []);

    if (loading) {
        return (
            <div className="flex h-64 items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <>
            <h1 className="text-3xl font-heading font-bold">Bienvenido, Usuario</h1>
            <p className="text-muted-foreground">Gestiona tus pedidos y datos personales desde tu panel de control.</p>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <div className="rounded-lg border bg-card p-6 shadow-sm">
                    <h3 className="font-semibold mb-2">Pedidos Recientes</h3>
                    <p className="text-2xl font-bold text-primary">0</p>
                    <p className="text-xs text-muted-foreground">Últimos 30 días</p>
                </div>
                <div className="rounded-lg border bg-card p-6 shadow-sm">
                    <h3 className="font-semibold mb-2">Cotizaciones {mode === 'empresa' ? 'Activas' : ''}</h3>
                    <p className="text-2xl font-bold text-primary">0</p>
                    <p className="text-xs text-muted-foreground">En revisión</p>
                </div>
            </div>
        </>
    );
}
