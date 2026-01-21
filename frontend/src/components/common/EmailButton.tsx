"use client";

import Link from "next/link";
import { Mail } from "lucide-react";
import { cn } from "@/lib/utils";

export default function EmailButton() {
    return (
        <Link
            href="mailto:ventas@arcam.cl"
            className={cn(
                "fixed bottom-24 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-blue-500 text-white shadow-lg transition-transform hover:scale-110 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
            )}
            aria-label="Enviar correo electrónico"
        >
            <Mail className="h-8 w-8" />
        </Link>
    );
}
