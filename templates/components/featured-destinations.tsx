import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { MapPin, Star } from "lucide-react"

const destinations = [
  {
    id: 1,
    name: "Santorini, Greece",
    description: "Experience the magic of white-washed buildings and stunning sunsets over the Aegean Sea.",
    image: "/santorini-greece-white-buildings-blue-domes-sunset.png",
    rating: 4.9,
    price: "From $1,299",
    duration: "7 days",
  },
  {
    id: 2,
    name: "Bali, Indonesia",
    description: "Discover tropical paradise with pristine beaches, ancient temples, and lush rice terraces.",
    image: "/bali-indonesia-rice-terraces-temple-tropical-parad.png",
    rating: 4.8,
    price: "From $899",
    duration: "10 days",
  },
  {
    id: 3,
    name: "Swiss Alps",
    description: "Adventure awaits in the majestic mountains with world-class skiing and breathtaking views.",
    image: "/swiss-alps-mountains-snow-peaks-alpine-village.png",
    rating: 4.9,
    price: "From $1,599",
    duration: "5 days",
  },
]

export function FeaturedDestinations() {
  return (
    <section className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">Featured Destinations</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
            Handpicked destinations that offer extraordinary experiences and unforgettable memories.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {destinations.map((destination) => (
            <Card
              key={destination.id}
              className="group overflow-hidden hover:shadow-xl transition-all duration-300 border-border"
            >
              <div className="relative overflow-hidden">
                <img
                  src={destination.image || "/placeholder.svg"}
                  alt={destination.name}
                  className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm font-medium">{destination.rating}</span>
                </div>
              </div>

              <CardContent className="p-6">
                <div className="flex items-center gap-2 text-accent mb-2">
                  <MapPin className="h-4 w-4" />
                  <span className="text-sm font-medium">{destination.duration}</span>
                </div>

                <h3 className="text-xl font-bold text-foreground mb-2">{destination.name}</h3>

                <p className="text-muted-foreground mb-4 text-pretty">{destination.description}</p>

                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-2xl font-bold text-foreground">{destination.price}</span>
                    <span className="text-sm text-muted-foreground ml-1">per person</span>
                  </div>
                  <Button className="bg-primary hover:bg-primary/90">Explore</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-12">
          <Button
            variant="outline"
            size="lg"
            className="border-primary text-primary hover:bg-primary hover:text-primary-foreground bg-transparent"
          >
            View All Destinations
          </Button>
        </div>
      </div>
    </section>
  )
}
