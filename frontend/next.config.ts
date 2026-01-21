import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.arcam.cl',
      },
      {
        protocol: 'http',
        hostname: '**.arcam.cl',
      },
      {
        protocol: 'https',
        hostname: 'arcam.cl',
      },
      {
        protocol: 'http',
        hostname: 'arcam.cl',
      },
      {
        protocol: 'https',
        hostname: 'placehold.co',
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
    ],
    formats: ['image/webp', 'image/avif'],
  },
  compress: true,
  experimental: {
    optimizePackageImports: ['lucide-react', 'framer-motion'],
  },
  reactStrictMode: true,
};

export default nextConfig;
