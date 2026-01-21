"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        // Register mock
        setTimeout(() => {
            setLoading(false);
            router.push("/perfil");
        }, 1500);
    };

    return (
        <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-4 bg-muted/20">
            <div className="w-full max-w-sm space-y-6 rounded-lg border bg-card p-6 shadow-sm">
                <div className="text-center">
                    <h1 className="text-2xl font-bold">Crear Cuenta</h1>
                    <p className="text-sm text-muted-foreground">Únete a ARCAM para gestionar tus pedidos</p>
                </div>

                <form onSubmit={handleRegister} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Nombre</label>
                            <Input placeholder="Juan" required />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Apellido</label>
                            <Input placeholder="Pérez" required />
                        </div>
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Email</label>
                        <Input type="email" placeholder="nombre@ejemplo.com" required />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Contraseña</label>
                        <Input type="password" required />
                    </div>
                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? <Loader2 className="animate-spin" /> : "Registrarse"}
                    </Button>
                </form>

                <div className="text-center text-sm">
                    ¿Ya tienes cuenta?{" "}
                    <Link href="/login" className="text-primary hover:underline font-medium">
                        Identifícate
                    </Link>
                </div>
            </div>
        </div>
    );
}
