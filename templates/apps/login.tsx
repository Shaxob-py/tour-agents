"use client"

import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Image from "next/image"
import { useState } from "react"

export default function LoginPage() {
  const [phoneNumber, setPhoneNumber] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSendCode = async () => {
    if (!phoneNumber) return

    setIsLoading(true)
    try {
      // Here you would integrate with your Telegram bot API
      console.log("[v0] Sending phone number to Telegram bot:", phoneNumber)
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      alert("Verification code sent to your Telegram! Please check your messages.")
    } catch (error) {
      console.error("[v0] Error sending code:", error)
      alert("Failed to send code. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left side - Login Form */}
            <div className="space-y-8">
              <div className="text-center lg:text-left">
                <h2 className="text-3xl font-bold tracking-tight text-foreground">Welcome back</h2>
                <p className="mt-2 text-muted-foreground">
                  Enter your phone number to receive a login code via Telegram
                </p>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Sign In with Telegram</CardTitle>
                  <CardDescription>
                    Enter your phone number and we'll send you a verification code through our Telegram bot
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone Number</Label>
                    <Input
                      id="phone"
                      type="tel"
                      placeholder="+1 (555) 123-4567"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      required
                    />
                  </div>

                  <Button
                    className="w-full bg-secondary hover:bg-secondary/90"
                    onClick={handleSendCode}
                    disabled={!phoneNumber || isLoading}
                  >
                    {isLoading ? "Sending Code..." : "Send Verification Code"}
                  </Button>

                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <span className="w-full border-t" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                      <span className="bg-background px-2 text-muted-foreground">How it works</span>
                    </div>
                  </div>

                  <div className="bg-muted/50 p-4 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <svg className="h-6 w-6 text-primary" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
                      </svg>
                      <div>
                        <p className="text-sm font-medium">Secure Login via Telegram</p>
                        <p className="text-xs text-muted-foreground">
                          Our bot will send you a verification code instantly
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="text-center text-sm">
                    <span className="text-muted-foreground">Don't have an account? </span>
                    <a
                      href="https://t.me/your_tour_agency_bot"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline"
                    >
                      Register here
                    </a>
                    <span className="text-muted-foreground"> with our Telegram bot</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="hidden lg:block">
              <div className="relative h-[600px] w-full rounded-lg overflow-hidden">
                <Image
                  src="/modern-airplane-flying-through-clouds-with-blue-sk.png"
                  alt="Airplane flying through clouds representing travel and adventure"
                  fill
                  className="object-cover"
                  priority
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
                <div className="absolute bottom-6 left-6 text-white">
                  <h3 className="text-2xl font-bold mb-2">Welcome back, traveler!</h3>
                  <p className="text-lg opacity-90">Continue your journey with WanderLux</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
