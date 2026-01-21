"use client";

import { useEffect } from "react";
import { useAppStore } from "@/store/useStore";

export function ModeSync({ mode }: { mode: "persona" | "empresa" }) {
    const { setMode } = useAppStore();

    useEffect(() => {
        setMode(mode);
    }, [mode, setMode]);

    return null;
}
