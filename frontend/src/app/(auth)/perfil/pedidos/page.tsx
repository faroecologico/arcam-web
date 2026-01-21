"use client";

import { useEffect, useState } from "react";
import { useAppStore } from "@/store/useStore";
// import { getOrdersByCustomer } from "@/lib/woocommerce"; // Client component cannot import valid fetchWoo
import { Loader2, Package, Clock } from "lucide-react";

// Mock orders for demo purposes since we don't have Real Auth yet
const MOCK_ORDERS = [
    {
        id: 101,
        status: "processing",
        total: "150000",
        date_created: "2023-10-25",
        line_items: [{ name: "Casco de Seguridad" }, { name: "Guantes" }]
    },
    {
        id: 104,
        status: "completed",
        total: "45000",
        date_created: "2023-09-12",
        line_items: [{ name: "Zapatos Dielectricos" }]
    }
];

export default function OrderHistoryPage() {
    const { user } = useAppStore();
    const [orders, setOrders] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // In a real scenario, we would call an API route /api/orders that uses the session cookie
        // For now, allow a loading effect
        setTimeout(() => {
            setOrders(MOCK_ORDERS);
            setLoading(false);
        }, 800);
    }, []);

    if (loading) {
        return (
            <div className="flex h-64 items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold font-heading">Historial de Pedidos</h1>
            {orders.length === 0 ? (
                <div className="text-center py-12 border rounded-lg bg-card">
                    <Package className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                    <h3 className="text-lg font-medium">No tienes pedidos recientes</h3>
                    <p className="text-muted-foreground">Tus compras aparecerán aquí.</p>
                </div>
            ) : (
                <div className="grid gap-4">
                    {orders.map((order) => (
                        <div key={order.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-6 bg-card border rounded-lg shadow-sm gap-4">
                            <div>
                                <div className="flex items-center gap-2 mb-1">
                                    <span className="font-bold">#{order.id}</span>
                                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${order.status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100' :
                                            order.status === 'processing' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100' :
                                                'bg-gray-100 text-gray-800'
                                        }`}>
                                        {order.status === 'processing' ? 'En Proceso' : 'Completado'}
                                    </span>
                                </div>
                                <div className="text-sm text-muted-foreground flex items-center gap-2">
                                    <Clock className="h-3 w-3" /> {order.date_created}
                                </div>
                                <div className="mt-2 text-sm">
                                    {order.line_items.map((item: any, i: number) => (
                                        <span key={i}>{item.name}{i < order.line_items.length - 1 ? ", " : ""}</span>
                                    ))}
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="font-bold text-lg">
                                    ${parseInt(order.total).toLocaleString("es-CL")}
                                </div>
                                <button className="text-sm text-primary hover:underline font-medium">
                                    Ver Detalles
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
