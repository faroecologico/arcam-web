"use client";

import { useEffect } from "react";
import { useAppStore } from "@/store/useStore";
import { ModeSync } from "@/components/layout/ModeSync";

export default function CotizacionLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    // Force B2B mode on all Quote pages
    return (
        <div className="dark">
            <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
                <ModeSync mode="empresa" />
                {children}
            </div>
        </div>
    );
}
