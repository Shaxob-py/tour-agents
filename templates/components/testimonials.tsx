import { Card, CardContent } from "@/components/ui/card"
import { Star, Quote } from "lucide-react"

const testimonials = [
  {
    id: 1,
    name: "Sarah Johnson",
    location: "New York, USA",
    rating: 5,
    text: "WanderLux made our honeymoon in Santorini absolutely magical. Every detail was perfectly planned, and the memories will last a lifetime.",
    avatar: "/professional-woman-smiling-headshot.png",
  },
  {
    id: 2,
    name: "Michael Chen",
    location: "Toronto, Canada",
    rating: 5,
    text: "The Swiss Alps adventure exceeded all expectations. Professional guides, stunning locations, and seamless organization. Highly recommended!",
    avatar: "/professional-smiling-man-headshot.png",
  },
  {
    id: 3,
    name: "Emma Rodriguez",
    location: "Madrid, Spain",
    rating: 5,
    text: "Bali was a dream come true! The cultural experiences and natural beauty were incredible. WanderLux truly knows how to create perfect trips.",
    avatar: "/professional-woman-smiling-headshot.png",
  },
]

export function Testimonials() {
  return (
    <section className="py-20 bg-muted">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4 text-balance">What Our Travelers Say</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
            Don't just take our word for it. Here's what our satisfied customers have to say about their experiences.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial) => (
            <Card
              key={testimonial.id}
              className="bg-background border-border hover:shadow-lg transition-shadow duration-300"
            >
              <CardContent className="p-6">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>

                <div className="relative mb-6">
                  <Quote className="h-8 w-8 text-accent/20 absolute -top-2 -left-2" />
                  <p className="text-muted-foreground italic text-pretty pl-6">"{testimonial.text}"</p>
                </div>

                <div className="flex items-center gap-4">
                  <img
                    src={testimonial.avatar || "/placeholder.svg"}
                    alt={testimonial.name}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                  <div>
                    <h4 className="font-semibold text-foreground">{testimonial.name}</h4>
                    <p className="text-sm text-muted-foreground">{testimonial.location}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
