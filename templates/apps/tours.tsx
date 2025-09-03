"use client"

import {Navigation} from "@/components/navigation"
import {Footer} from "@/components/footer"
import {Card, CardContent} from "@/components/ui/card"
import {Button} from "@/components/ui/button"
import {Badge} from "@/components/ui/badge"
import {Input} from "@/components/ui/input"
import {Label} from "@/components/ui/label"
import {ArrowLeft, Calendar, Clock, MapPin, Star, Users} from "lucide-react"
import {useRouter} from "next/navigation"

const tours = [
  {
    id: 1,
    name: "Mediterranean Odyssey",
    destination: "Greece & Italy",
    description: "A 14-day journey through ancient civilizations, stunning coastlines, and world-renowned cuisine.",
    image: "/mediterranean-coast-greece-italy-ancient-ruins-blu.png",
    rating: 4.9,
    price: "$2,499",
    originalPrice: "$2,899",
    duration: "14 days",
    groupSize: "12-20 people",
    difficulty: "Easy",
    includes: ["Accommodation", "Meals", "Transportation", "Guide"],
    highlights: ["Acropolis of Athens", "Santorini Sunset", "Roman Colosseum", "Amalfi Coast"],
    nextDeparture: "May 15, 2024",
  },
  {
    id: 2,
    name: "Himalayan Adventure",
    destination: "Nepal & Tibet",
    description: "Experience the roof of the world with breathtaking mountain views and spiritual encounters.",
    image: "/himalayan-mountains-nepal-tibet-prayer-flags-monas.png",
    rating: 4.8,
    price: "$3,299",
    originalPrice: "$3,699",
    duration: "16 days",
    groupSize: "8-14 people",
    difficulty: "Challenging",
    includes: ["Accommodation", "Meals", "Permits", "Sherpa Guide"],
    highlights: ["Everest Base Camp", "Potala Palace", "Tibetan Monasteries", "Mountain Views"],
    nextDeparture: "April 20, 2024",
  },
  {
    id: 3,
    name: "African Safari Experience",
    destination: "Kenya & Tanzania",
    description: "Witness the Great Migration and encounter Africa's Big Five in their natural habitat.",
    image: "/african-safari-lions-elephants-savanna-sunset-keny.png",
    rating: 4.9,
    price: "$4,199",
    originalPrice: "$4,599",
    duration: "12 days",
    groupSize: "6-12 people",
    difficulty: "Moderate",
    includes: ["Luxury Lodges", "All Meals", "Game Drives", "Expert Guide"],
    highlights: ["Serengeti Plains", "Ngorongoro Crater", "Masai Mara", "Big Five Safari"],
    nextDeparture: "June 10, 2024",
  },
  {
    id: 4,
    name: "Northern Lights Quest",
    destination: "Iceland & Norway",
    description: "Chase the Aurora Borealis while exploring ice caves, geysers, and fjords.",
    image: "/northern-lights-aurora-borealis-iceland-norway-fjo.png",
    rating: 4.7,
    price: "$2,899",
    originalPrice: "$3,299",
    duration: "10 days",
    groupSize: "10-16 people",
    difficulty: "Easy",
    includes: ["Hotels", "Breakfast", "Transportation", "Aurora Guide"],
    highlights: ["Northern Lights", "Blue Lagoon", "Geyser Park", "Norwegian Fjords"],
    nextDeparture: "March 5, 2024",
  },
]

export default function ToursPage() {
  const router = useRouter()

  const handleGoBack = () => {
    router.back()
  }

  return (
    <main className="min-h-screen">
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-32 bg-gradient-to-r from-secondary to-secondary/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-secondary-foreground mb-6 text-balance">
            Unforgettable Tour Packages
          </h1>
          <p className="text-xl text-secondary-foreground/90 max-w-2xl mx-auto text-pretty">
            Carefully crafted itineraries that combine adventure, culture, and comfort for the ultimate travel
            experience.
          </p>
        </div>
      </section>

      {/* Search Form Section */}
      <section className="py-12 bg-background border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-card rounded-lg border p-6 shadow-sm">
            <div className="flex items-center gap-4 mb-6">
              <Button
                variant="outline"
                size="sm"
                className="flex items-center gap-2 bg-transparent"
                onClick={handleGoBack}
              >
                <ArrowLeft className="h-4 w-4" />
                Go back
              </Button>
              <h2 className="text-2xl font-semibold text-foreground">Search Tours</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <Label htmlFor="from" className="text-sm font-medium text-foreground">
                  From
                </Label>
                <Input id="from" placeholder="Departure city" className="w-full" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="to" className="text-sm font-medium text-foreground">
                  To
                </Label>
                <Input id="to" placeholder="Destination" className="w-full" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="when" className="text-sm font-medium text-foreground">
                  When
                </Label>
                <Input id="when" type="date" className="w-full" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="when-back" className="text-sm font-medium text-foreground">
                  When back
                </Label>
                <Input id="when-back" type="date" className="w-full" />
              </div>
            </div>

            <div className="mt-4 flex justify-center">
              <Button className="px-8 bg-primary hover:bg-primary/90">Search Tours</Button>
            </div>
          </div>
        </div>
      </section>

      {/* Tours Grid */}
      <section className="py-20 bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {tours.map((tour) => (
              <Card
                key={tour.id}
                className="group overflow-hidden hover:shadow-xl transition-all duration-300 border-border"
              >
                <div className="md:flex">
                  <div className="md:w-2/5 relative overflow-hidden">
                    <img
                      src={tour.image || "/placeholder.svg"}
                      alt={tour.name}
                      className="w-full h-64 md:h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute top-4 left-4">
                      <Badge variant="secondary" className="bg-accent text-accent-foreground">
                        {tour.difficulty}
                      </Badge>
                    </div>
                    <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1">
                      <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="text-sm font-medium">{tour.rating}</span>
                    </div>
                  </div>

                  <CardContent className="md:w-3/5 p-6">
                    <div className="flex items-center gap-2 text-accent mb-2">
                      <MapPin className="h-4 w-4" />
                      <span className="text-sm font-medium">{tour.destination}</span>
                    </div>

                    <h3 className="text-2xl font-bold text-foreground mb-2">{tour.name}</h3>

                    <p className="text-muted-foreground mb-4 text-pretty">{tour.description}</p>

                    <div className="grid grid-cols-2 gap-4 mb-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>{tour.duration}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="h-4 w-4" />
                        <span>{tour.groupSize}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        <span>{tour.nextDeparture}</span>
                      </div>
                    </div>

                    <div className="mb-4">
                      <h4 className="font-semibold text-foreground mb-2">Tour Highlights:</h4>
                      <div className="flex flex-wrap gap-2">
                        {tour.highlights.slice(0, 3).map((highlight, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {highlight}
                          </Badge>
                        ))}
                        {tour.highlights.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{tour.highlights.length - 3} more
                          </Badge>
                        )}
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-2xl font-bold text-foreground">{tour.price}</span>
                          <span className="text-lg text-muted-foreground line-through">{tour.originalPrice}</span>
                        </div>
                        <span className="text-sm text-muted-foreground">per person</span>
                      </div>
                      <Button className="bg-primary hover:bg-primary/90">Book Now</Button>
                    </div>
                  </CardContent>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  )
}
