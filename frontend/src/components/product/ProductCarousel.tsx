"use client";

import React, { useCallback } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import ProductCard from '@/components/product/ProductCard';
import Link from 'next/link';

interface ProductCarouselProps {
    title: string;
    products: any[];
    viewAllLink?: string;
}

export default function ProductCarousel({ title, products, viewAllLink }: ProductCarouselProps) {
    const [emblaRef, emblaApi] = useEmblaCarousel({
        align: 'start',
        slidesToScroll: 1, // Smoother scroll
        dragFree: true // Native feel
    });

    const scrollPrev = useCallback(() => {
        if (emblaApi) emblaApi.scrollPrev();
    }, [emblaApi]);

    const scrollNext = useCallback(() => {
        if (emblaApi) emblaApi.scrollNext();
    }, [emblaApi]);

    if (!products || products.length === 0) return null;

    return (
        <section className="py-8 relative group">
            <div className="container px-4">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold font-heading uppercase tracking-tight">{title}</h2>
                    {viewAllLink && (
                        <Link href={viewAllLink} className="text-sm font-medium text-primary hover:underline flex items-center gap-1">
                            Ver todo <ArrowRight className="h-4 w-4" />
                        </Link>
                    )}
                </div>

                <div className="relative">
                    {/* Carousel Viewport */}
                    <div className="overflow-hidden -mx-4 px-4 py-4" ref={emblaRef}>
                        <div className="flex gap-4 sm:gap-6 touch-pan-y">
                            {products.map((product) => (
                                <div key={product.id} className="flex-[0_0_80%] min-w-0 sm:flex-[0_0_45%] md:flex-[0_0_30%] lg:flex-[0_0_22%] pl-4 first:pl-0">
                                    <ProductCard product={product} />
                                </div>
                            ))}

                            {/* "View More" Card at the end */}
                            {viewAllLink && (
                                <div className="flex-[0_0_40%] sm:flex-[0_0_20%] flex items-center justify-center">
                                    <Link href={viewAllLink} className="flex flex-col items-center justify-center h-full w-full min-h-[300px] gap-4 rounded-xl border-2 border-dashed border-muted hover:border-primary hover:bg-muted/30 transition-all group/more">
                                        <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center text-primary group-hover/more:scale-110 transition-transform">
                                            <ArrowRight className="h-6 w-6" />
                                        </div>
                                        <span className="font-medium text-muted-foreground group-hover/more:text-primary">Ver más productos</span>
                                    </Link>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Navigation Buttons (Visible on larger screens) */}
                    <Button
                        variant="ghost"
                        size="icon"
                        className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 h-12 w-12 rounded-full bg-background/80 shadow-lg backdrop-blur-sm border hidden md:flex opacity-0 group-hover:opacity-100 transition-opacity z-10 hover:bg-background"
                        onClick={scrollPrev}
                    >
                        <ChevronLeft className="h-6 w-6" />
                    </Button>

                    <Button
                        variant="ghost"
                        size="icon"
                        className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 h-12 w-12 rounded-full bg-background/80 shadow-lg backdrop-blur-sm border hidden md:flex opacity-0 group-hover:opacity-100 transition-opacity z-10 hover:bg-background"
                        onClick={scrollNext}
                    >
                        <ChevronRight className="h-6 w-6" />
                    </Button>
                </div>
            </div>
        </section>
    );
}
