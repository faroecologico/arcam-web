import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

// Only create client if URL is present to avoid runtime errors on empty URL
export const supabase = supabaseUrl
    ? createClient(supabaseUrl, supabaseKey)
    : {
        from: () => ({ select: () => ({ eq: () => ({ order: () => ({ limit: () => ({ data: [], error: null }) }) }) }), insert: () => ({ error: null }) })
    } as any;
