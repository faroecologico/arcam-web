import Link from 'next/link';
import Image from 'next/image';
import { Mail, Phone, MapPin, Facebook, Instagram, Linkedin } from 'lucide-react';

export default function Footer() {
    return (
        <footer className="bg-slate-950 text-slate-200 border-t border-slate-800">
            <div className="container px-4 py-12">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {/* Column 1: Company Info */}
                    <div>
                        <div className="relative h-12 w-32 mb-4">
                            <Image
                                src="/images/logo-arcam.png"
                                alt="ARCAM Logo"
                                fill
                                className="object-contain brightness-0 invert"
                            />
                        </div>
                        <p className="text-sm text-slate-400 leading-relaxed">
                            Especialistas en ropa corporativa y EPP para faena agrícola y packaging desde hace más de 20 años.
                        </p>
                    </div>

                    {/* Column 2: Quick Links */}
                    <div>
                        <h3 className="font-bold text-white mb-4">Enlaces Rápidos</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link href="/" className="text-sm hover:text-primary transition-colors">
                                    Inicio
                                </Link>
                            </li>
                            <li>
                                <Link href="/catalogo" className="text-sm hover:text-primary transition-colors">
                                    Catálogo
                                </Link>
                            </li>
                            <li>
                                <Link href="/nosotros" className="text-sm hover:text-primary transition-colors">
                                    Nosotros
                                </Link>
                            </li>
                            <li>
                                <Link href="/cotizacion" className="text-sm hover:text-primary transition-colors">
                                    Cotizar
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Column 3: Contact Info */}
                    <div>
                        <h3 className="font-bold text-white mb-4">Contacto</h3>
                        <ul className="space-y-3">
                            <li className="flex items-start gap-2">
                                <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0 text-primary" />
                                <span className="text-sm">
                                    Camino a Zapallar, Km 2,2<br />
                                    Curicó, Chile
                                </span>
                            </li>
                            <li className="flex items-center gap-2">
                                <Phone className="h-4 w-4 flex-shrink-0 text-primary" />
                                <a href="tel:+56932522462" className="text-sm hover:text-primary transition-colors">
                                    +569 3252 2462
                                </a>
                            </li>
                            <li className="flex items-center gap-2">
                                <Mail className="h-4 w-4 flex-shrink-0 text-primary" />
                                <a href="mailto:ventas@arcam.cl" className="text-sm hover:text-primary transition-colors">
                                    ventas@arcam.cl
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Column 4: Hours & Social */}
                    <div>
                        <h3 className="font-bold text-white mb-4">Horario de Atención</h3>
                        <ul className="space-y-2 text-sm text-slate-400 mb-6">
                            <li>Lun - Jue: 8:30 - 18:30</li>
                            <li>Viernes: 8:30 - 17:30</li>
                            <li>Sábado: 8:30 - 13:00</li>
                            <li>Domingo: Cerrado</li>
                        </ul>

                        <div className="flex gap-3">
                            <a href="#" className="h-9 w-9 rounded-full bg-slate-800 hover:bg-primary flex items-center justify-center transition-colors" aria-label="Facebook">
                                <Facebook className="h-4 w-4" />
                            </a>
                            <a href="#" className="h-9 w-9 rounded-full bg-slate-800 hover:bg-primary flex items-center justify-center transition-colors" aria-label="Instagram">
                                <Instagram className="h-4 w-4" />
                            </a>
                            <a href="#" className="h-9 w-9 rounded-full bg-slate-800 hover:bg-primary flex items-center justify-center transition-colors" aria-label="LinkedIn">
                                <Linkedin className="h-4 w-4" />
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Bar */}
            <div className="border-t border-slate-800 bg-slate-950/50">
                <div className="container px-4 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
                    <p className="text-xs text-slate-500">
                        © {new Date().getFullYear()} ARCAM. Todos los derechos reservados.
                    </p>
                    <div className="flex gap-6 text-xs text-slate-500">
                        <Link href="/terminos" className="hover:text-primary transition-colors">
                            Términos y Condiciones
                        </Link>
                        <Link href="/privacidad" className="hover:text-primary transition-colors">
                            Política de Privacidad
                        </Link>
                    </div>
                </div>
            </div>
        </footer>
    );
}
