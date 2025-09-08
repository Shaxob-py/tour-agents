import Link from "next/link"
import { MapPin, Phone, Mail, Facebook, Instagram, Twitter } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-primary text-primary-foreground">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-2xl font-bold mb-4">WanderLux</h3>
            <p className="text-primary-foreground/80 mb-6 text-pretty">
              Creating extraordinary travel experiences and unforgettable memories since 2010. Your adventure starts
              here.
            </p>
            <div className="flex space-x-4">
              <Facebook className="h-6 w-6 hover:text-accent cursor-pointer transition-colors" />
              <Instagram className="h-6 w-6 hover:text-accent cursor-pointer transition-colors" />
              <Twitter className="h-6 w-6 hover:text-accent cursor-pointer transition-colors" />
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/destinations" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Destinations
                </Link>
              </li>
              <li>
                <Link href="/tours" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Tours
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Services</h4>
            <ul className="space-y-2">
              <li>
                <Link href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Adventure Tours
                </Link>
              </li>
              <li>
                <Link href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Cultural Experiences
                </Link>
              </li>
              <li>
                <Link href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Luxury Travel
                </Link>
              </li>
              <li>
                <Link href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Group Tours
                </Link>
              </li>
              <li>
                <Link href="#" className="text-primary-foreground/80 hover:text-accent transition-colors">
                  Custom Packages
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Info</h4>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <MapPin className="h-5 w-5 text-accent" />
                <span className="text-primary-foreground/80">123 Travel Street, Adventure City, AC 12345</span>
              </div>
              <div className="flex items-center gap-3">
                <Phone className="h-5 w-5 text-accent" />
                <span className="text-primary-foreground/80">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center gap-3">
                <Mail className="h-5 w-5 text-accent" />
                <span className="text-primary-foreground/80">info@wanderlux.com</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-primary-foreground/20 mt-12 pt-8 text-center">
          <p className="text-primary-foreground/60">
            © 2024 WanderLux Travel Agency. All rights reserved. | Privacy Policy | Terms of Service
          </p>
        </div>
      </div>
    </footer>
  )
}
