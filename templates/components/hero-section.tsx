import { Button } from "@/components/ui/button"
import { ArrowRight, Play } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/stunning-mountain-landscape-with-crystal-clear-lak.png')`,
        }}
      >
        <div className="absolute inset-0 bg-black/40" />
      </div>

      {/* Content */}
      <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 text-balance">
          Discover Your Next
          <span className="block text-accent">Adventure</span>
        </h1>
        <p className="text-xl md:text-2xl mb-8 text-pretty max-w-2xl mx-auto opacity-90">
          Explore breathtaking destinations and create unforgettable memories with our expertly crafted travel
          experiences.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button size="lg" className="bg-secondary hover:bg-secondary/90 text-white px-8 py-3 text-lg">
            Explore Destinations
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="border-white text-white hover:bg-white hover:text-foreground px-8 py-3 text-lg bg-transparent"
          >
            <Play className="mr-2 h-5 w-5" />
            Watch Video
          </Button>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white rounded-full mt-2 animate-pulse" />
        </div>
      </div>
    </section>
  )
}
