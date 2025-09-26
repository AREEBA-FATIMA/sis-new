import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Users, MapPin, BookOpen } from "lucide-react"
import { mockGrades } from "@/lib/mock-data"
import { notFound } from "next/navigation"

interface GradeDetailPageProps {
  params: {
    id: string
  }
}

export default function GradeDetailPage({ params }: GradeDetailPageProps) {
  const grade = mockGrades.find((g) => g.id === Number.parseInt(params.id))

  if (!grade) {
    notFound()
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto">
        <Link href="/grades">
          <Button variant="outline" className="mb-6 bg-transparent">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Grades List
          </Button>
        </Link>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl text-balance">
              Grade Details - {grade.name} {grade.section}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Class Information</h3>
                <div className="space-y-3">
                  <div>
                    <span className="font-medium">Grade:</span>
                    <p className="text-muted-foreground">{grade.name}</p>
                  </div>
                  <div>
                    <span className="font-medium">Section:</span>
                    <p className="text-muted-foreground">{grade.section}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4" />
                    <span>{grade.campus}</span>
                  </div>
                  <div>
                    <span className="font-medium">Class Teacher:</span>
                    <p className="text-muted-foreground">{grade.classTeacher}</p>
                  </div>
                  <div>
                    <span className="font-medium">Classroom:</span>
                    <p className="text-muted-foreground">{grade.classRoom}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Enrollment Details</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    <div>
                      <span className="font-medium">Total Capacity:</span>
                      <p className="text-muted-foreground">{grade.capacity} students</p>
                    </div>
                  </div>
                  <div>
                    <span className="font-medium">Current Students:</span>
                    <p className="text-muted-foreground">{grade.currentStudents}</p>
                  </div>
                  <div>
                    <span className="font-medium">Available Seats:</span>
                    <p className="text-muted-foreground">{grade.capacity - grade.currentStudents}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="border-t pt-6">
              <h3 className="font-semibold text-lg mb-4">Curriculum</h3>
              <div className="flex items-start gap-2">
                <BookOpen className="w-4 h-4 mt-1" />
                <div>
                  <span className="font-medium">Subjects:</span>
                  <p className="text-muted-foreground mt-1">{grade.subjects}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
