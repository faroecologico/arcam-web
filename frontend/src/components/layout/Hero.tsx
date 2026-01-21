"use client";

import { useCallback, useEffect } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import Autoplay from 'embla-carousel-autoplay';
import Link from 'next/link';
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react';
import { Button } from '../ui/button';
import { motion } from 'framer-motion';

const slides = [
    {
        id: 1,
        title: "Ropa Corporativa y EPP",
        subtitle: "Para faena agrícola y packaging",
        description: "Especialistas en uniformes de trabajo y equipos de protección personal desde hace más de 20 años.",
        cta: "Ver Catálogo",
        ctaLink: "/catalogo",
        bgGradient: "from-blue-600 to-blue-800",
        image: "/images/hero-1.png"
    },
    {
        id: 2,
        title: "Personalización Total",
        subtitle: "Bordados y estampados",
        description: "Personaliza tus uniformes con el logo de tu empresa. Servicio rápido y profesional.",
        cta: "Cotizar Ahora",
        ctaLink: "/cotizacion",
        bgGradient: "from-green-600 to-green-800",
        image: "/images/hero-2.png"
    },
    {
        id: 3,
        title: "Soluciones B2B",
        subtitle: "Para empresas y organizaciones",
        description: "Precios especiales por volumen y servicio personalizado para tu negocio.",
        cta: "Modo Empresa",
        ctaLink: "/empresa",
        bgGradient: "from-slate-700 to-slate-900",
        image: "/images/hero-3.png"
    }
];

export default function Hero() {
    const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true }, [
        Autoplay({ delay: 5000, stopOnInteraction: false })
    ]);

    const scrollPrev = useCallback(() => {
        if (emblaApi) emblaApi.scrollPrev();
    }, [emblaApi]);

    const scrollNext = useCallback(() => {
        if (emblaApi) emblaApi.scrollNext();
    }, [emblaApi]);

    return (
        <section className="relative overflow-hidden group">
            <div ref={emblaRef} className="overflow-hidden">
                <div className="flex">
                    {slides.map((slide, index) => (
                        <div key={slide.id} className="flex-[0_0_100%] min-w-0">
                            <div className={`relative bg-gradient-to-r ${slide.bgGradient} text-white`}>
                                <div className="absolute inset-0 bg-black/20"></div>

                                <div className="container relative px-4 py-24 md:py-32 lg:py-40">
                                    <motion.div
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.2 }}
                                        className="max-w-3xl"
                                    >
                                        <p className="text-sm md:text-base font-medium mb-2 uppercase tracking-wider text-blue-200">
                                            {slide.subtitle}
                                        </p>
                                        <h1 className="text-4xl md:text-5xl lg:text-6xl font-heading font-bold mb-4 leading-tight">
                                            {slide.title}
                                        </h1>
                                        <p className="text-lg md:text-xl mb-8 text-blue-50 max-w-2xl">
                                            {slide.description}
                                        </p>
                                        <Link href={slide.ctaLink}>
                                            <Button
                                                size="lg"
                                                className="bg-white text-blue-600 hover:bg-blue-50 font-bold text-base md:text-lg px-8 py-6 shadow-xl hover:shadow-2xl transition-all"
                                            >
                                                {slide.cta}
                                                <ArrowRight className="ml-2 h-5 w-5" />
                                            </Button>
                                        </Link>
                                    </motion.div>
                                </div>

                                {/* Decorative Pattern */}
                                <div className="absolute bottom-0 right-0 w-1/2 h-full opacity-10">
                                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white via-transparent to-transparent"></div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Navigation Arrows */}
            <Button
                variant="ghost"
                size="icon"
                onClick={scrollPrev}
                className="absolute left-4 top-1/2 -translate-y-1/2 h-14 w-14 rounded-full bg-white/90 hover:bg-white text-slate-900 shadow-2xl backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10"
            >
                <ChevronLeft className="h-8 w-8" />
            </Button>

            <Button
                variant="ghost"
                size="icon"
                onClick={scrollNext}
                className="absolute right-4 top-1/2 -translate-y-1/2 h-14 w-14 rounded-full bg-white/90 hover:bg-white text-slate-900 shadow-2xl backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10"
            >
                <ChevronRight className="h-8 w-8" />
            </Button>

            {/* Slide Indicators */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2 z-10">
                {slides.map((_, index) => (
                    <button
                        key={index}
                        onClick={() => emblaApi?.scrollTo(index)}
                        className="h-2 w-8 rounded-full bg-white/40 hover:bg-white/70 transition-all"
                        aria-label={`Go to slide ${index + 1}`}
                    />
                ))}
            </div>
        </section>
    );
}
