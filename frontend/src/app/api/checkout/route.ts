import { NextResponse } from "next/server";
import { createOrder, getCustomerByEmail, createCustomer } from "@/lib/woocommerce";

export async function POST(request: Request) {
    try {
        const data = await request.json();

        // --- SMART CHECKOUT LOGIC (FR-11) ---
        const email = data.billing?.email;
        let customerId = 0;

        if (email) {
            // 1. Try to find existing customer
            const existingCustomer = await getCustomerByEmail(email);

            if (existingCustomer) {
                customerId = existingCustomer.id;
            } else {
                // 2. Auto-create customer if not exists
                // Generate a username from email (part before @) + random suffix or just email
                const username = email.split('@')[0] + Math.floor(Math.random() * 1000);

                try {
                    const newCustomer = await createCustomer({
                        email: email,
                        first_name: data.billing.first_name,
                        last_name: data.billing.last_name,
                        username: username,
                        password: Math.random().toString(36).slice(-8) + "Aa1!", // Auto-gen password
                        billing: data.billing,
                        shipping: data.shipping
                    });
                    customerId = newCustomer.id;
                } catch (err) {
                    console.error("Failed to auto-create customer:", err);
                    // Fallback to Guest checkout if creation fails
                    customerId = 0;
                }
            }
        }

        // Assign Customer ID to Order
        data.customer_id = customerId;

        const order = await createOrder(data);
        return NextResponse.json(order);
    } catch (error: any) {
        console.error("Checkout Error:", error);
        return NextResponse.json(
            { message: error.message || "Internal Error" },
            { status: 500 }
        );
    }
}
