import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
  {
    variants: {
      variant: {
        default:
          "bg-[#00BFFF] text-white shadow-[0_0_10px_rgba(0,191,255,0.3)] hover:bg-[#00BFFF]/80 hover:shadow-[0_0_15px_rgba(0,191,255,0.5)] transition-all",
        destructive:
          "bg-red-500 text-white shadow-xs hover:bg-red-600 focus-visible:ring-red-500/20",
        outline:
          "border border-gray-700/50 bg-gray-800/50 text-gray-200 hover:border-[#00BFFF]/50 hover:text-[#00BFFF] hover:bg-gray-700/50 transition-all",
        secondary:
          "bg-gray-700/50 text-[#00BFFF] hover:bg-gray-600/50 hover:text-[#00BFFF] transition-all",
        ghost:
          "text-gray-200 hover:bg-[#00BFFF]/10 hover:text-[#00BFFF] transition-all",
        link: "text-[#00BFFF] underline-offset-4 hover:underline hover:text-[#00BFFF]/80 transition-colors",
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3",
        sm: "h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5",
        lg: "h-10 rounded-md px-6 has-[>svg]:px-4",
        icon: "size-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot : "button"

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
