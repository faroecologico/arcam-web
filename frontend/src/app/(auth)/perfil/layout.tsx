"use client";

import { DashboardSidebar } from "@/components/dashboard/Sidebar";

export default function PerfilLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="container min-h-screen py-8">
            <div className="grid grid-cols-1 md:grid-cols-[250px_1fr] gap-8">
                <aside className="hidden md:block">
                    <DashboardSidebar />
                </aside>
                <main className="space-y-6">
                    {children}
                </main>
            </div>
        </div>
    );
}
