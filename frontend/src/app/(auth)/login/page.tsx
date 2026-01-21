"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        // Soft login mock for now. TODO: Connect to WP JWT Auth
        setTimeout(() => {
            setLoading(false);
            router.push("/perfil");
        }, 1500);
    };

    return (
        <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-4 bg-muted/20">
            <div className="w-full max-w-sm space-y-6 rounded-lg border bg-card p-6 shadow-sm">
                <div className="text-center">
                    <h1 className="text-2xl font-bold">Iniciar Sesión</h1>
                    <p className="text-sm text-muted-foreground">Accede a tu historial y seguimiento</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Email</label>
                        <Input
                            type="email"
                            placeholder="nombre@ejemplo.com"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="space-y-2">
                        <div className="flex items-center justify-between">
                            <label className="text-sm font-medium">Contraseña</label>
                            <Link href="/recuperar" className="text-xs text-primary hover:underline">
                                ¿Olvidaste tu contraseña?
                            </Link>
                        </div>
                        <Input
                            type="password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? <Loader2 className="animate-spin" /> : "Ingresar"}
                    </Button>
                </form>

                <div className="text-center text-sm">
                    ¿No tienes cuenta?{" "}
                    <Link href="/registro" className="text-primary hover:underline font-medium">
                        Regístrate
                    </Link>
                </div>
            </div>
        </div>
    );
}
