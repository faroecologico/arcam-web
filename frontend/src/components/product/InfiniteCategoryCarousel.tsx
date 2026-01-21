"use client";

import React, { useCallback, useEffect } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import Link from 'next/link';
import Image from 'next/image';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { getGenericImage } from "@/lib/imageUtils";

interface Category {
    id: number;
    name: string;
    slug: string;
    image?: { src: string };
}

interface InfiniteCategoryCarouselProps {
    categories: Category[];
}

export default function InfiniteCategoryCarousel({ categories }: InfiniteCategoryCarouselProps) {
    const [emblaRef, emblaApi] = useEmblaCarousel({
        loop: true,
        align: 'start',
        dragFree: true,
        containScroll: 'trimSnaps'
    });

    // Auto-scroll effect
    useEffect(() => {
        if (!emblaApi) return;

        const autoScroll = setInterval(() => {
            emblaApi.scrollNext();
        }, 3000); // Auto-scroll every 3 seconds

        return () => clearInterval(autoScroll);
    }, [emblaApi]);

    const scrollPrev = useCallback(() => {
        if (emblaApi) emblaApi.scrollPrev();
    }, [emblaApi]);

    const scrollNext = useCallback(() => {
        if (emblaApi) emblaApi.scrollNext();
    }, [emblaApi]);

    if (!categories || categories.length === 0) return null;

    // Generic category placeholder replaced by local logo logic

    return (
        <section className="container py-12 px-4 border-b bg-gradient-to-r from-muted/30 to-background relative group">
            <div className="overflow-hidden" ref={emblaRef}>
                <div className="flex gap-8 touch-pan-y">
                    {categories.map((cat, index) => (
                        <motion.div
                            key={cat.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05, duration: 0.3 }}
                        >
                            <Link
                                href={`/catalogo?category=${cat.slug}`}
                                className="flex flex-col items-center gap-3 min-w-[100px] group/item cursor-pointer flex-shrink-0"
                            >
                                <motion.div
                                    className="h-20 w-20 rounded-full bg-white border-2 border-transparent overflow-hidden transition-all shadow-md relative"
                                    whileHover={{ scale: 1.1, borderColor: 'hsl(var(--primary))' }}
                                    whileTap={{ scale: 0.95 }}
                                >
                                    <Image
                                        src={cat.image?.src || getGenericImage(cat.id)}
                                        alt={cat.name}
                                        width={80}
                                        height={80}
                                        className={`object-cover w-full h-full ${!cat.image?.src ? "grayscale-[0.2]" : ""}`}
                                    />
                                </motion.div>
                                <span className="text-xs font-semibold text-center tracking-tight group-hover/item:text-primary transition-colors max-w-[100px] line-clamp-2">
                                    {cat.name}
                                </span>
                            </Link>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Navigation Arrows */}
            <Button
                variant="ghost"
                size="icon"
                onClick={scrollPrev}
                className="absolute left-2 top-1/2 -translate-y-1/2 h-12 w-12 rounded-full bg-background/90 shadow-lg backdrop-blur-sm border opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-background z-10"
            >
                <ChevronLeft className="h-6 w-6" />
            </Button>

            <Button
                variant="ghost"
                size="icon"
                onClick={scrollNext}
                className="absolute right-2 top-1/2 -translate-y-1/2 h-12 w-12 rounded-full bg-background/90 shadow-lg backdrop-blur-sm border opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-background z-10"
            >
                <ChevronRight className="h-6 w-6" />
            </Button>
        </section>
    );
}
