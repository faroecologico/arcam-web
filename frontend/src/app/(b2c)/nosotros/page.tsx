import Image from "next/image";

export default function AboutPage() {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero Nosotros */}
            <section className="relative h-[400px] w-full bg-secondary flex items-center justify-center overflow-hidden">
                <div className="absolute inset-0 bg-black/50 z-10" />
                {/* Placeholder for About Hero Image if available */}
                <div className="relative z-20 text-center px-4">
                    <h1 className="text-4xl md:text-6xl font-bold font-heading text-white uppercase tracking-wider mb-4">
                        Nuestra Historia
                    </h1>
                    <p className="text-xl text-gray-200 max-w-2xl mx-auto">
                        Más de una década construyendo confianza en la región del Maule.
                    </p>
                </div>
            </section>

            {/* Quiénes Somos */}
            <section className="py-20 container mx-auto px-4">
                <div className="grid md:grid-cols-2 gap-12 items-center">
                    <div className="space-y-6">
                        <h2 className="text-3xl font-bold font-heading text-primary uppercase">Quiénes Somos</h2>
                        <div className="space-y-4 text-muted-foreground leading-relaxed">
                            <p>
                                En <strong>Arcam</strong> somos una empresa curicana con más de una década de experiencia dedicada a brindar soluciones integrales en ferretería, materiales de construcción, seguridad industrial y vestuario corporativo.
                            </p>
                            <p>
                                Desde nuestros inicios, hemos crecido junto a la región del Maule, fortaleciendo vínculos con empresas, maestros y particulares que confían en nuestra atención cercana, asesoría técnica y compromiso constante con la calidad.
                            </p>
                            <p>
                                Creemos que construir no es solo levantar estructuras, sino también relaciones duraderas basadas en la confianza, el cumplimiento y el trabajo bien hecho. Por eso, más que una ferretería, somos un aliado para quienes día a día impulsan el desarrollo local.
                            </p>
                        </div>
                    </div>
                    <div className="relative h-[400px] rounded-2xl overflow-hidden shadow-xl bg-gray-100">
                        {/* Replace with actual team/store photo */}
                        <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                            <span className="text-lg">Foto Equipo / Tienda</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Misión / Visión */}
            <section className="py-20 bg-muted/30">
                <div className="container mx-auto px-4 grid md:grid-cols-2 gap-8">
                    {/* Misión */}
                    <div className="bg-card p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="h-12 w-12 bg-primary/10 rounded-lg flex items-center justify-center mb-6">
                            <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                        </div>
                        <h3 className="text-2xl font-bold font-heading mb-4 uppercase">Nuestra Misión</h3>
                        <p className="text-muted-foreground">
                            Brindar atención cercana, asesoría técnica y un servicio integral, respaldado por marcas líderes y por nuestra propia línea de confección y vestuario corporativo, contribuyendo así al desarrollo y la seguridad de quienes construyen el progreso de nuestra región.
                        </p>
                    </div>

                    {/* Visión */}
                    <div className="bg-card p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                        <div className="h-12 w-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-6">
                            <svg className="w-6 h-6 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                        </div>
                        <h3 className="text-2xl font-bold font-heading mb-4 uppercase">Nuestra Visión</h3>
                        <p className="text-muted-foreground">
                            Ser reconocidos como una empresa líder en soluciones integrales para la construcción y la industria, destacando por la calidad de nuestros productos, la confianza de nuestros clientes y el compromiso con el desarrollo local.
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
}
