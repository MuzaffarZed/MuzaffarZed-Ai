"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import { ExpenseTracker } from "@/components/expense-tracker"
import { ThemeProvider } from "@/components/theme-provider"

export default function Home() {
  return (
    <ThemeProvider>
      <ExpenseTracker />
    </ThemeProvider>
  )
}
