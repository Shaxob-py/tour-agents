import {Navigation} from "@/components/navigation"
import {Footer} from "@/components/footer"
import {Card, CardContent} from "@/components/ui/card"
import {Button} from "@/components/ui/button"
import {Clock, Star, Users} from "lucide-react"

const destinations = [
  {
    id: 1,
    name: "Santorini, Greece",
    description: "Experience the magic of white-washed buildings and stunning sunsets over the Aegean Sea.",
    image: "/santorini-greece-white-buildings-blue-domes-sunset.png",
    rating: 4.9,
    price: "From $1,299",
    duration: "7 days",
    groupSize: "2-12 people",
    category: "Romantic",
  },
  {
    id: 2,
    name: "Bali, Indonesia",
    description: "Discover tropical paradise with pristine beaches, ancient temples, and lush rice terraces.",
    image: "/bali-indonesia-rice-terraces-temple-tropical-parad.png",
    rating: 4.8,
    price: "From $899",
    duration: "10 days",
    groupSize: "4-16 people",
    category: "Adventure",
  },
  {
    id: 3,
    name: "Swiss Alps",
    description: "Adventure awaits in the majestic mountains with world-class skiing and breathtaking views.",
    image: "/swiss-alps-mountains-snow-peaks-alpine-village.png",
    rating: 4.9,
    price: "From $1,599",
    duration: "5 days",
    groupSize: "6-20 people",
    category: "Adventure",
  },
  {
    id: 4,
    name: "Tokyo, Japan",
    description: "Immerse yourself in the perfect blend of ancient traditions and cutting-edge modernity.",
    image: "/tokyo-japan-cherry-blossoms-temple-modern-city.png",
    rating: 4.7,
    price: "From $1,199",
    duration: "8 days",
    groupSize: "4-14 people",
    category: "Cultural",
  },
  {
    id: 5,
    name: "Machu Picchu, Peru",
    description: "Trek through the Andes to discover the lost city of the Incas in this unforgettable journey.",
    image: "/machu-picchu-peru-ancient-ruins-mountains-clouds.png",
    rating: 4.8,
    price: "From $1,399",
    duration: "6 days",
    groupSize: "8-16 people",
    category: "Adventure",
  },
  {
    id: 6,
    name: "Maldives",
    description: "Relax in overwater bungalows surrounded by crystal-clear waters and pristine coral reefs.",
    image: "/maldives-overwater-bungalows-crystal-clear-water-c.png",
    rating: 4.9,
    price: "From $2,299",
    duration: "7 days",
    groupSize: "2-8 people",
    category: "Luxury",
  },
]

export default function DestinationsPage() {
  return (
    <main className="min-h-screen">
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-32 bg-gradient-to-r from-primary to-primary/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-primary-foreground mb-6 text-balance">
            Explore Amazing Destinations
          </h1>
          <p className="text-xl text-primary-foreground/90 max-w-2xl mx-auto text-pretty">
            From tropical paradises to mountain adventures, discover your perfect getaway with our curated collection of
            world-class destinations.
          </p>
        </div>
      </section>

      {/* Destinations Grid */}
      <section className="py-20 bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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
                  <div className="absolute top-4 left-4 bg-accent text-accent-foreground px-3 py-1 rounded-full text-sm font-medium">
                    {destination.category}
                  </div>
                  <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1">
                    <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm font-medium">{destination.rating}</span>
                  </div>
                </div>

                <CardContent className="p-6">
                  <h3 className="text-xl font-bold text-foreground mb-2">{destination.name}</h3>

                  <p className="text-muted-foreground mb-4 text-pretty">{destination.description}</p>

                  <div className="flex items-center gap-4 mb-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      <span>{destination.duration}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Users className="h-4 w-4" />
                      <span>{destination.groupSize}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xl font-bold text-foreground">{destination.price}</span>
                      <span className="text-sm text-muted-foreground ml-1">per person</span>
                    </div>
                    <Button className="bg-secondary hover:bg-secondary/90">View Details</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  )
}
