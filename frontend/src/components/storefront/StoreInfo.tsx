import { Clock, Mail, MapPin, Phone } from 'lucide-react';

export default function StoreInfo() {
    return (
        <section className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-950 py-16 border-y">
            <div className="container px-4">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-heading font-bold tracking-tight mb-3">Visítanos</h2>
                    <p className="text-muted-foreground max-w-2xl mx-auto">
                        Encuéntranos en nuestra tienda física en Curicó. Nuestro equipo está listo para atenderte.
                    </p>
                </div>

                <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
                    {/* Map */}
                    <div className="rounded-xl overflow-hidden shadow-xl border bg-white dark:bg-slate-950 h-[400px]">
                        <iframe
                            src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d2010.7932532025136!2d-71.199954!3d-34.998269!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9664570aaeff919b%3A0xf1b97212ef813bc8!2sARCAM%20FERRETER%C3%8DA%20Y%20MAT.%20DE%20CONSTRUCCI%C3%93N!5e1!3m2!1ses!2scl!4v1768944748671!5m2!1ses!2scl"
                            width="100%"
                            height="100%"
                            style={{ border: 0 }}
                            allowFullScreen
                            loading="lazy"
                            referrerPolicy="no-referrer-when-downgrade"
                            title="Ubicación ARCAM - Camino a Zapallar Km 2.2, Curicó"
                        ></iframe>
                    </div>

                    {/* Info Cards */}
                    <div className="space-y-6">
                        {/* Address */}
                        <div className="bg-white dark:bg-slate-950 rounded-xl p-6 shadow-md border">
                            <div className="flex items-start gap-4">
                                <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                                    <MapPin className="h-6 w-6 text-primary" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-lg mb-1">Dirección</h3>
                                    <p className="text-muted-foreground">
                                        Camino a Zapallar, Kilómetro 2,2<br />
                                        Curicó, Chile
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Hours */}
                        <div className="bg-white dark:bg-slate-950 rounded-xl p-6 shadow-md border">
                            <div className="flex items-start gap-4">
                                <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                                    <Clock className="h-6 w-6 text-primary" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="font-bold text-lg mb-3">Horario de Atención</h3>
                                    <div className="space-y-1 text-sm">
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Lunes a Jueves</span>
                                            <span className="font-medium">8:30 - 18:30</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Viernes</span>
                                            <span className="font-medium">8:30 - 17:30</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-muted-foreground">Sábado</span>
                                            <span className="font-medium">8:30 - 13:00</span>
                                        </div>
                                        <div className="flex justify-between text-red-600 dark:text-red-400">
                                            <span>Domingo</span>
                                            <span className="font-medium">Cerrado</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Contact */}
                        <div className="bg-white dark:bg-slate-950 rounded-xl p-6 shadow-md border">
                            <div className="flex items-start gap-4">
                                <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                                    <Phone className="h-6 w-6 text-primary" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-lg mb-2">Contacto</h3>
                                    <div className="space-y-1 text-sm">
                                        <div className="flex items-center gap-2">
                                            <Phone className="h-4 w-4 text-muted-foreground" />
                                            <a href="tel:+56932522462" className="hover:text-primary transition-colors">
                                                +569 3252 2462
                                            </a>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Mail className="h-4 w-4 text-muted-foreground" />
                                            <a href="mailto:ventas@arcam.cl" className="hover:text-primary transition-colors">
                                                ventas@arcam.cl
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
