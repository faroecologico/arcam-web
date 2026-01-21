"use client"

import * as React from "react"
import { Check } from "lucide-react"

import { cn } from "@/lib/utils"

const Checkbox = React.forwardRef<
    HTMLInputElement,
    Omit<React.InputHTMLAttributes<HTMLInputElement>, "onCheckedChange"> & {
        onCheckedChange?: (checked: boolean) => void
    }
>(({ className, onCheckedChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        props.onChange?.(e)
        onCheckedChange?.(e.target.checked)
    }

    return (
        <div className="relative flex items-center">
            <input
                type="checkbox"
                ref={ref}
                className={cn(
                    "peer h-4 w-4 appearance-none shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 checked:bg-primary checked:text-primary-foreground",
                    className
                )}
                onChange={handleChange}
                {...props}
            />
            <Check className="absolute left-0 top-0 h-4 w-4 text-primary-foreground pointer-events-none opacity-0 peer-checked:opacity-100" />
        </div>
    )
})
Checkbox.displayName = "Checkbox"

export { Checkbox }
