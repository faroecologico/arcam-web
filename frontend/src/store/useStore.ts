import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export type AppMode = 'persona' | 'empresa';

interface AppState {
    mode: AppMode;
    toggleMode: () => void;
    setMode: (mode: AppMode) => void;
}

interface CartItem {
    id: string; // WooCommerce ID or SKU
    name: string;
    price: number;
    quantity: number;
    image: string;
}

interface CartState {
    cart: CartItem[]; // Shopping Cart (B2C)
    quoteCart: CartItem[]; // Quote Cart (B2B)
    addToCart: (item: CartItem) => void;
    removeFromCart: (id: string) => void;
    updateCartQuantity: (id: string, quantity: number) => void;
    addToQuote: (item: CartItem) => void;
    removeFromQuote: (id: string) => void;
    updateQuoteQuantity: (id: string, quantity: number) => void;
    clearCart: () => void;
    clearQuote: () => void;

    // --- UI State ---
    isCartOpen: boolean;
    openCart: () => void;
    closeCart: () => void;
}

interface UserState {
    isAuthenticated: boolean;
    user: any | null; // Replace with proper user type
    login: (user: any) => void;
    logout: () => void;
}

interface WishlistState {
    wishlist: number[];
    toggleWishlist: (id: number) => void;
}

export const useAppStore = create<AppState & CartState & UserState & WishlistState>()(
    persist(
        (set) => ({
            // --- UI Mode ---
            mode: 'persona',
            toggleMode: () =>
                set((state) => {
                    const newMode = state.mode === 'persona' ? 'empresa' : 'persona';
                    // Update DOM class for Tailwind Dark Mode
                    if (typeof document !== 'undefined') {
                        if (newMode === 'empresa') {
                            document.documentElement.classList.add('dark');
                        } else {
                            document.documentElement.classList.remove('dark');
                        }
                        // Set cookie for Server Logic
                        document.cookie = `arcam-mode=${newMode}; path=/; max-age=31536000`;
                    }
                    return { mode: newMode };
                }),
            setMode: (mode) => set({ mode }),

            // --- Cart (B2C) ---
            cart: [],
            addToCart: (item) =>
                set((state) => {
                    const existing = state.cart.find((i) => i.id === item.id);
                    if (existing) {
                        return {
                            cart: state.cart.map((i) =>
                                i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
                            ),
                        };
                    }
                    return { cart: [...state.cart, item] };
                }),
            removeFromCart: (id) =>
                set((state) => ({ cart: state.cart.filter((i) => i.id !== id) })),
            updateCartQuantity: (id, quantity) =>
                set((state) => ({
                    cart: state.cart.map((i) => (i.id === id ? { ...i, quantity } : i))
                })),
            clearCart: () => set({ cart: [] }),

            // --- Quote (B2B) ---
            quoteCart: [],
            addToQuote: (item) =>
                set((state) => {
                    const existing = state.quoteCart.find((i) => i.id === item.id);
                    if (existing) {
                        return {
                            quoteCart: state.quoteCart.map((i) =>
                                i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
                            ),
                        };
                    }
                    return { quoteCart: [...state.quoteCart, item] };
                }),
            removeFromQuote: (id) =>
                set((state) => ({ quoteCart: state.quoteCart.filter((i) => i.id !== id) })),
            updateQuoteQuantity: (id, quantity) =>
                set((state) => ({
                    quoteCart: state.quoteCart.map((i) => (i.id === id ? { ...i, quantity } : i))
                })),
            clearQuote: () => set({ quoteCart: [] }),

            // --- User ---
            isAuthenticated: false,
            user: null,
            login: (user) => set({ isAuthenticated: true, user }),
            logout: () => set({ isAuthenticated: false, user: null }),

            // --- UI ---
            // --- UI ---
            isCartOpen: false,
            openCart: () => set({ isCartOpen: true }),
            closeCart: () => set({ isCartOpen: false }),

            // --- Wishlist (FR-07) ---
            wishlist: [],
            toggleWishlist: (id: number) =>
                set((state) => {
                    const exists = state.wishlist.includes(id);
                    return {
                        wishlist: exists
                            ? state.wishlist.filter((i) => i !== id)
                            : [...state.wishlist, id],
                    };
                }),

        }),
        {
            name: 'arcam-storage',
            storage: createJSONStorage(() => localStorage),
            partialize: (state) => ({
                mode: state.mode,
                cart: state.cart,
                quoteCart: state.quoteCart,
                wishlist: state.wishlist, // Persist wishlist
                isAuthenticated: state.isAuthenticated
            }),
        }
    )
);
