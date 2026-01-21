import type { Metadata } from "next";
import { Inter, Oswald } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { FloatingDock } from "@/components/layout/FloatingDock";
import { CartDrawer } from "@/components/cart/CartDrawer";
import WhatsAppButton from "@/components/common/WhatsAppButton";
import EmailButton from "@/components/common/EmailButton";
import Footer from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const oswald = Oswald({ subsets: ["latin"], variable: "--font-oswald" });

export const metadata: Metadata = {
  title: {
    template: "%s | ARCAM",
    default: "ARCAM - Ropa Corporativa y EPP",
  },
  description: "Especialistas en ropa de trabajo para faena agrícola y packaging.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          inter.variable,
          oswald.variable
        )}
      >
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
        <FloatingDock />
        <CartDrawer />
        <WhatsAppButton />
        <EmailButton />
      </body>
    </html>
  );
}
