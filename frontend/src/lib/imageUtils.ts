export const INDUSTRIAL_PLACEHOLDERS = [
    "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?q=80&w=600&auto=format&fit=crop", // Construction yellow
    "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?q=80&w=600&auto=format&fit=crop", // Welding/Sparks
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=600&auto=format&fit=crop", // Engineer laptop
    "https://images.unsplash.com/photo-1535732820275-9ffd998cac22?q=80&w=600&auto=format&fit=crop", // Safety helmet
    "https://images.unsplash.com/photo-1617191599824-c08595dc6c91?q=80&w=600&auto=format&fit=crop", // Safety vest
    "https://images.unsplash.com/photo-1517173646545-d8aa98759fb9?q=80&w=600&auto=format&fit=crop", // Fabric/Sewing
    "https://images.unsplash.com/photo-1520699049698-acd54ebdd4ee?q=80&w=600&auto=format&fit=crop", // Tools
    "https://images.unsplash.com/photo-1595856417757-d2a93911516e?q=80&w=600&auto=format&fit=crop", // Warehouse
    "https://images.unsplash.com/photo-1581092921461-eab62e97a780?q=80&w=600&auto=format&fit=crop", // Industrial Factory
    "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=600&auto=format&fit=crop", // Blueprints
];

export function getGenericImage(id: string | number): string {
    if (!id) return INDUSTRIAL_PLACEHOLDERS[0];

    const idStr = String(id);
    // Simple hash function to get a number from the string
    let hash = 0;
    for (let i = 0; i < idStr.length; i++) {
        hash = idStr.charCodeAt(i) + ((hash << 5) - hash);
    }

    // Use absolute value and modulo to pick an image index
    const index = Math.abs(hash) % INDUSTRIAL_PLACEHOLDERS.length;
    return INDUSTRIAL_PLACEHOLDERS[index];
}
