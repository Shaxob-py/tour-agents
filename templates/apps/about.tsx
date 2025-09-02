import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Award, Users, Globe, Heart } from "lucide-react"

const stats = [
  { icon: Users, label: "Happy Travelers", value: "50,000+" },
  { icon: Globe, label: "Destinations", value: "120+" },
  { icon: Award, label: "Awards Won", value: "25+" },
  { icon: Heart, label: "Years of Experience", value: "15+" },
]

const team = [
  {
    name: "Sarah Mitchell",
    role: "Founder & CEO",
    image: "/professional-woman-ceo-travel-industry.png",
    bio: "With over 20 years in the travel industry, Sarah founded WanderLux to create extraordinary travel experiences.",
  },
  {
    name: "David Chen",
    role: "Head of Operations",
    image: "/professional-man-operations-manager-travel.png",
    bio: "David ensures every trip runs smoothly with his expertise in logistics and customer service excellence.",
  },
  {
    name: "Maria Rodriguez",
    role: "Lead Travel Designer",
    image: "/professional-woman-travel-designer.png",
    bio: "Maria crafts unique itineraries that blend adventure, culture, and luxury for unforgettable experiences.",
  },
]

export default function AboutPage() {
  return (
    <main className="min-h-screen">
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-32 bg-gradient-to-r from-primary to-primary/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-primary-foreground mb-6 text-balance">About WanderLux</h1>
          <p className="text-xl text-primary-foreground/90 max-w-2xl mx-auto text-pretty">
            Crafting extraordinary travel experiences and creating memories that last a lifetime since 2010.
          </p>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-20 bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-foreground mb-6 text-balance">Our Story</h2>
              <p className="text-lg text-muted-foreground mb-6 text-pretty">
                Founded in 2010 by travel enthusiast Sarah Mitchell, WanderLux began as a small boutique agency with a
                simple mission: to create travel experiences that go beyond the ordinary.
              </p>
              <p className="text-lg text-muted-foreground mb-6 text-pretty">
                What started as a passion project has grown into a trusted name in luxury travel, serving thousands of
                adventurous souls who seek authentic, transformative experiences around the globe.
              </p>
              <p className="text-lg text-muted-foreground text-pretty">
                Today, we continue to push the boundaries of what travel can be, combining expert local knowledge with
                personalized service to create journeys that inspire, educate, and transform.
              </p>
            </div>
            <div className="relative">
              <img src="/travel-agency-office-team-planning-world-map.png" alt="WanderLux team planning" className="rounded-lg shadow-xl" />
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-20 bg-muted">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4 text-balance">Our Impact in Numbers</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
              These numbers represent the trust our travelers place in us and the experiences we've created together.
            </p>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <Card key={index} className="text-center bg-background border-border">
                <CardContent className="p-8">
                  <stat.icon className="h-12 w-12 text-accent mx-auto mb-4" />
                  <div className="text-3xl font-bold text-foreground mb-2">{stat.value}</div>
                  <div className="text-muted-foreground">{stat.label}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Our Team */}
      <section className="py-20 bg-background">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4 text-balance">Meet Our Team</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
              The passionate individuals behind every extraordinary journey, dedicated to making your travel dreams come
              true.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <Card
                key={index}
                className="text-center bg-card border-border hover:shadow-lg transition-shadow duration-300"
              >
                <CardContent className="p-8">
                  <img
                    src={member.image || "/placeholder.svg"}
                    alt={member.name}
                    className="w-32 h-32 rounded-full mx-auto mb-6 object-cover"
                  />
                  <h3 className="text-xl font-bold text-foreground mb-2">{member.name}</h3>
                  <Badge variant="secondary" className="mb-4">
                    {member.role}
                  </Badge>
                  <p className="text-muted-foreground text-pretty">{member.bio}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="py-20 bg-muted">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4 text-balance">Our Values</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
              The principles that guide everything we do and every experience we create.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="bg-background border-border">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Heart className="h-8 w-8 text-accent" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-4">Passion</h3>
                <p className="text-muted-foreground text-pretty">
                  We're passionate about travel and believe every journey should be transformative and inspiring.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-background border-border">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Award className="h-8 w-8 text-accent" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-4">Excellence</h3>
                <p className="text-muted-foreground text-pretty">
                  We strive for excellence in every detail, from planning to execution, ensuring unforgettable
                  experiences.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-background border-border">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Globe className="h-8 w-8 text-accent" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-4">Authenticity</h3>
                <p className="text-muted-foreground text-pretty">
                  We create authentic experiences that connect you with local cultures and hidden gems.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  )
}
