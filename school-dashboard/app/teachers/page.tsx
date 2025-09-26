"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Eye } from "lucide-react"
import { GraphQLClient, gql } from "graphql-request"

type TeacherListItem = {
  id: string
  fullName: string
  gender: string
  roles: {
    campus: { name: string }
  }[]
}

export default function TeachersPage() {
  const [teachers, setTeachers] = useState<TeacherListItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        const client = new GraphQLClient("http://localhost:8000/graphql/")
        const query = gql`
          query {
            teachers {
              id
              fullName
              gender
              roles {
                campus {
                  name
                }
              }
            }
          }
        `
        const data = await client.request<{ teachers: TeacherListItem[] }>(query)
        setTeachers(data.teachers)
      } catch (error) {
        console.error("Error fetching teachers:", error)
      } finally {
        setLoading(false)
      }
    }
    fetchTeachers()
  }, [])

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
            <CardTitle className="text-2xl">Teachers Management</CardTitle>
            <CardDescription>List of all teachers with basic info</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p>Loading teachers...</p>
            ) : (
              <div className="space-y-4">
                {teachers.map((teacher) => (
                  <Card key={teacher.id} className="border border-border">
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-semibold">{teacher.fullName}</h3>
                          <p className="text-sm text-muted-foreground">
                            {teacher.gender} •{" "}
                            {teacher.roles[0]?.campus?.name || "No campus"}
                          </p>
                        </div>
                        <Link href={`/teachers/${teacher.id}`}>
                          <Button variant="outline" size="sm">
                            <Eye className="w-4 h-4 mr-2" /> View Details
                          </Button>
                        </Link>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
