"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { CheckCircle, FileText } from "lucide-react";
import { Suspense } from 'react';

function OrderReceivedContent() {
    const params = useSearchParams();
    const id = params.get("id");
    const type = params.get("type"); // 'order' or 'quote'

    const isQuote = type === "quote";

    return (
        <div className="container flex min-h-[60vh] flex-col items-center justify-center text-center">
            <div className="mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400">
                {isQuote ? <FileText className="h-12 w-12" /> : <CheckCircle className="h-12 w-12" />}
            </div>

            <h1 className="text-3xl font-bold font-heading uppercase text-foreground">
                {isQuote ? "¡Solicitud Recibida!" : "¡Gracias por tu compra!"}
            </h1>

            <p className="mt-4 max-w-md text-muted-foreground">
                {isQuote
                    ? `Hemos recibido tu solicitud de cotización #${id}. Nuestro equipo comercial se comunicará contigo a la brevedad.`
                    : `Tu pedido #${id} ha sido ingresado correctamente. Recibirás un correo con los detalles y la confirmación.`
                }
            </p>

            <div className="mt-8 flex gap-4">
                <Link href="/">
                    <Button variant="outline">Volver al Inicio</Button>
                </Link>
                <Link href={isQuote ? "/empresa/catalogo" : "/catalogo"}>
                    <Button>Seguir Comprando</Button>
                </Link>
            </div>
        </div>
    );
}

export default function OrderReceivedPage() {
    return (
        <Suspense fallback={<div>Cargando...</div>}>
            <OrderReceivedContent />
        </Suspense>
    );
}
