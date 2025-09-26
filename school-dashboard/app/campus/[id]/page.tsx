import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, MapPin, Phone, Calendar, Users } from "lucide-react"
import { mockCampuses } from "@/lib/mock-data"
import { notFound } from "next/navigation"

interface CampusDetailPageProps {
  params: {
    id: string
  }
}

export default function CampusDetailPage({ params }: CampusDetailPageProps) {
  const campus = mockCampuses.find((c) => c.id === Number.parseInt(params.id))

  if (!campus) {
    notFound()
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto">
        <Link href="/campus">
          <Button variant="outline" className="mb-6 bg-transparent">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Campus List
          </Button>
        </Link>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl text-balance">Campus Details - {campus.name}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Campus Information</h3>
                <div className="space-y-3">
                  <div>
                    <span className="font-medium">Campus Name:</span>
                    <p className="text-muted-foreground">{campus.name}</p>
                  </div>
                  <div>
                    <span className="font-medium">Campus Code:</span>
                    <p className="text-muted-foreground">{campus.code}</p>
                  </div>
                  <div className="flex items-start gap-2">
                    <MapPin className="w-4 h-4 mt-1" />
                    <span>{campus.address}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="w-4 h-4" />
                    <span>{campus.contactNumber}</span>
                  </div>
                  <div>
                    <span className="font-medium">Status:</span>
                    <div className="mt-1">
                      <Badge variant={campus.status === "active" ? "default" : "secondary"}>{campus.status}</Badge>
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Administration</h3>
                <div className="space-y-3">
                  <div>
                    <span className="font-medium">Principal:</span>
                    <p className="text-muted-foreground">{campus.principal}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4" />
                    <span>Established: {campus.establishedYear}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="border-t pt-6">
              <h3 className="font-semibold text-lg mb-4">Capacity & Facilities</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  <div>
                    <span className="font-medium">Total Capacity:</span>
                    <p className="text-muted-foreground">{campus.capacity} students</p>
                  </div>
                </div>
                <div>
                  <span className="font-medium">Current Students:</span>
                  <p className="text-muted-foreground">{campus.currentStudents}</p>
                </div>
                <div>
                  <span className="font-medium">Available Seats:</span>
                  <p className="text-muted-foreground">{campus.capacity - campus.currentStudents}</p>
                </div>
              </div>
              <div>
                <span className="font-medium">Facilities:</span>
                <p className="text-muted-foreground mt-1">{campus.facilities}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
