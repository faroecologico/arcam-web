import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

// GET: Recuperar últimas búsquedas de un usuario
export async function GET(request: Request) {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get("user_id");

    if (!userId) {
        return NextResponse.json([]);
    }

    const { data, error } = await supabase
        .from('search_history')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
        .limit(6);

    if (error) {
        console.error("Error fetching search history:", error);
        return NextResponse.json([]);
    }

    // Deduplicate logic in backend or frontend? Let's assume DB might have dupes, but distinct query is better
    // For now simple select.
    return NextResponse.json(data);
}

// POST: Guardar una nueva búsqueda
export async function POST(request: Request) {
    const body = await request.json();
    const { query, user_id } = body;

    if (!query || query.length < 3) {
        return NextResponse.json({ message: "Query too short" }, { status: 400 });
    }

    // Insertar búsqueda
    const { error } = await supabase
        .from('search_history')
        .insert([
            {
                query: query.trim(),
                user_id: user_id || null, // Permitir anónimos? Sí, para analítica
            }
        ]);

    if (error) {
        console.error("Error saving search:", error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ success: true });
}
