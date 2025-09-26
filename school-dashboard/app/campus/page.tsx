import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Eye } from "lucide-react"
import { mockCampuses } from "@/lib/mock-data"

export default function CampusPage() {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-6xl mx-auto">
        <Link href="/">
          <Button variant="outline" className="mb-6 bg-transparent">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Button>
        </Link>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl text-balance">Campus Management</CardTitle>
            <CardDescription>Manage and view detailed information for all campuses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockCampuses.map((campus) => (
                <Card key={campus.id} className="border border-border">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="space-y-1">
                        <h3 className="font-semibold">{campus.name}</h3>
                        <div className="text-sm text-muted-foreground">
                          <span>
                            {campus.code} • {campus.currentStudents}/{campus.capacity} students
                          </span>
                        </div>
                        <Badge variant={campus.status === "active" ? "default" : "secondary"}>{campus.status}</Badge>
                      </div>
                      <Link href={`/campus/${campus.id}`}>
                        <Button variant="outline" size="sm">
                          <Eye className="w-4 h-4 mr-2" />
                          View Details
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
