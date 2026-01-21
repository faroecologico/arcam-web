"use client";

import { useAppStore } from "@/store/useStore";
import { motion } from "framer-motion";
import { Briefcase, User, Repeat } from "lucide-react";

export function DualToggle() {
    const mode = useAppStore((state) => state.mode);
    const toggleMode = useAppStore((state) => state.toggleMode);
    const isEmpresa = mode === "empresa";

    return (
        <button
            onClick={toggleMode}
            className={`
                group relative flex items-center justify-center gap-2 overflow-hidden rounded-full 
                px-3 py-2 md:px-5 md:py-2.5 
                text-sm font-medium transition-all duration-500
                focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2
                ${isEmpresa
                    ? "bg-slate-900 text-white shadow-lg shadow-slate-900/20 ring-1 ring-slate-700 hover:bg-slate-800"
                    : "bg-white text-slate-700 shadow-lg shadow-slate-200/50 ring-1 ring-slate-200 hover:bg-slate-50"}
            `}
            aria-label={isEmpresa ? "Cambiar a modo Persona" : "Cambiar a modo Empresa"}
        >
            {/* Animated Icon Container */}
            <div className="relative h-5 w-5">
                <motion.div
                    initial={false}
                    animate={{
                        opacity: isEmpresa ? 1 : 0,
                        rotate: isEmpresa ? 0 : -90,
                        scale: isEmpresa ? 1 : 0.5
                    }}
                    transition={{ duration: 0.3 }}
                    className="absolute inset-0 flex items-center justify-center"
                >
                    <Briefcase className="h-5 w-5" />
                </motion.div>
                <motion.div
                    initial={false}
                    animate={{
                        opacity: isEmpresa ? 0 : 1,
                        rotate: isEmpresa ? 90 : 0,
                        scale: isEmpresa ? 0.5 : 1
                    }}
                    transition={{ duration: 0.3 }}
                    className="absolute inset-0 flex items-center justify-center"
                >
                    <User className="h-5 w-5" />
                </motion.div>
            </div>

            {/* Text Label with sliding effect - HIDDEN ON MOBILE */}
            <div className="relative hidden h-5 w-[3.5rem] overflow-hidden text-left md:block">
                <motion.span
                    className="absolute left-0 flex items-center h-full"
                    animate={{ y: isEmpresa ? "-150%" : "0%" }}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                >
                    Persona
                </motion.span>
                <motion.span
                    className="absolute left-0 flex items-center h-full"
                    animate={{ y: isEmpresa ? "0%" : "150%" }}
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                >
                    Empresa
                </motion.span>
            </div>

            {/* Switch Icon Indicator - HIDDEN ON MOBILE */}
            <motion.div
                animate={{ rotate: isEmpresa ? 180 : 0 }}
                transition={{ duration: 0.5, ease: "easeInOut" }}
                className="ml-1 hidden text-slate-400 group-hover:text-primary transition-colors md:block"
            >
                <Repeat className="h-3.5 w-3.5" />
            </motion.div>
        </button>
    );
}
export default DualToggle;
