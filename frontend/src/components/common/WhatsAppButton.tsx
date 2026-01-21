"use client";

import { useAppStore } from "@/store/useStore";
import Link from "next/link";
import { MessageCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function WhatsAppButton() {
    return (
        <Link
            href="https://wa.me/56932522462"
            target="_blank"
            rel="noopener noreferrer"
            className={cn(
                "fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-green-500 text-white shadow-lg transition-transform hover:scale-110 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2",
                "animate-bounce-subtle" // Custom subtle bounce if needed
            )}
            aria-label="Contactar por WhatsApp"
        >
            <MessageCircle className="h-8 w-8" />
        </Link>
    );
}
