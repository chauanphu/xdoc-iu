import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "flex h-9 w-full rounded-md px-3 py-1 text-base md:text-sm transition-all",
        "bg-gray-800/50 border border-gray-700/50 text-gray-200",
        "placeholder:text-gray-500",
        "hover:border-[#00BFFF]/50 hover:bg-gray-700/50",
        "focus:outline-none focus:ring-2 focus:ring-[#00BFFF]/30 focus:border-[#00BFFF]",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        className
      )}
      {...props}
    />
  )
}

export { Input }
