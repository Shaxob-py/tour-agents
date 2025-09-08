"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Menu, X } from "lucide-react"

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-background border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/" className="text-2xl font-bold text-primary">
              WanderLux
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-8">
              <Link href="/" className="text-foreground hover:text-accent transition-colors">
                Home
              </Link>
              <Link href="/destinations" className="text-foreground hover:text-accent transition-colors">
                Destinations
              </Link>
              <Link href="/tours" className="text-foreground hover:text-accent transition-colors">
                Tours
              </Link>
              <Link href="/about" className="text-foreground hover:text-accent transition-colors">
                About
              </Link>
              <Link href="/contact" className="text-foreground hover:text-accent transition-colors">
                Contact
              </Link>
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            <Link href="/login">
              <Button className="bg-secondary hover:bg-secondary/90">Login</Button>
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button variant="ghost" size="sm" onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-card border-t border-border">
              <Link href="/" className="block px-3 py-2 text-foreground hover:text-accent transition-colors">
                Home
              </Link>
              <Link
                href="/destinations"
                className="block px-3 py-2 text-foreground hover:text-accent transition-colors"
              >
                Destinations
              </Link>
              <Link href="/tours" className="block px-3 py-2 text-foreground hover:text-accent transition-colors">
                Tours
              </Link>
              <Link href="/about" className="block px-3 py-2 text-foreground hover:text-accent transition-colors">
                About
              </Link>
              <Link href="/contact" className="block px-3 py-2 text-foreground hover:text-accent transition-colors">
                Contact
              </Link>
              <div className="px-3 py-2">
                <Link href="/login">
                  <Button className="w-full bg-secondary hover:bg-secondary/90">Login</Button>
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
