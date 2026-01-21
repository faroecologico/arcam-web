"use client";

import { cn } from "@/lib/utils";
import { User, Package, FileText, MapPin, Heart, LogOut } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarProps {
    className?: string;
}

export function DashboardSidebar({ className }: SidebarProps) {
    const pathname = usePathname();

    const items = [
        { name: "Mi Perfil", href: "/perfil", icon: User },
        { name: "Mis Pedidos", href: "/perfil/pedidos", icon: Package },
        { name: "Cotizaciones", href: "/perfil/cotizaciones", icon: FileText },
        { name: "Direcciones", href: "/perfil/direcciones", icon: MapPin },
        { name: "Lista de Deseos", href: "/favoritos", icon: Heart },
    ];

    return (
        <div className={cn("pb-12 h-full border-r bg-card", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        Mi Cuenta
                    </h2>
                    <div className="space-y-1">
                        {items.map((item) => (
                            <Link key={item.href} href={item.href}>
                                <span
                                    className={cn(
                                        "flex items-center rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground",
                                        pathname === item.href ? "bg-accent" : "transparent"
                                    )}
                                >
                                    <item.icon className="mr-2 h-4 w-4" />
                                    {item.name}
                                </span>
                            </Link>
                        ))}
                        <button className="w-full flex items-center rounded-md px-3 py-2 text-sm font-medium text-destructive hover:bg-destructive/10">
                            <LogOut className="mr-2 h-4 w-4" />
                            Cerrar Sesión
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
