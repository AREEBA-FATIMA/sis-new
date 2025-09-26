"use client"

import Link from "next/link"
import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Users, GraduationCap, Building2, BookOpen, UserCheck } from "lucide-react"
import GenderPieChart from "@/components/GenderPieChart"

type DashboardData = {
  students: number
  teachers: number
  campuses: number
  grades: number
  genderRatio: { male: number; female: number }
  campusDistribution: { campus: string; count: number }[]
}

export default function SchoolDashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData>({
    students: 0,
    teachers: 0,
    campuses: 0,
    grades: 0,
    genderRatio: { male: 0, female: 0 },
    campusDistribution: [],
  })

  useEffect(() => {
    const fetchData = async () => {
      const query = `
        query {
          totalTeachers
          totalStudents
          genderRatio {
            male
            female
          }
          campusDistribution {
            campus
            count
          }
        }
      `

      try {
        const res = await fetch("http://127.0.0.1:8000/graphql/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        })

        const result = await res.json()
        console.log("Dashboard Data:", result.data)

        setDashboardData({
          students: result.data?.totalStudents || 0,
          teachers: result.data?.totalTeachers || 0,
          campuses: result.data?.campusDistribution?.length || 0,
          grades: 0, // agar tumhare API me `totalGrades` ho to yaha use karo
          genderRatio: result.data?.genderRatio || { male: 0, female: 0 },
          campusDistribution: result.data?.campusDistribution || [],
        })
      } catch (error) {
        console.error("GraphQL Fetch Error:", error)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-balance mb-2">School Management Dashboard</h1>
          <p className="text-muted-foreground text-pretty">
            Comprehensive overview of your educational institution&apos;s key metrics and data
          </p>
        </div>

        {/* ✅ Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Link href="/students">
            <Card className="cursor-pointer hover:shadow-lg transition-shadow border border-border">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Students</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">{dashboardData.students}</div>
                <p className="text-xs text-muted-foreground">Active enrolled students</p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/teachers">
            <Card className="cursor-pointer hover:shadow-lg transition-shadow border border-border">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Teachers</CardTitle>
                <GraduationCap className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">{dashboardData.teachers}</div>
                <p className="text-xs text-muted-foreground">Active faculty members</p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/campus">
            <Card className="cursor-pointer hover:shadow-lg transition-shadow border border-border">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Campuses</CardTitle>
                <Building2 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">{dashboardData.campuses}</div>
                <p className="text-xs text-muted-foreground">Active campus locations</p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/grades">
            <Card className="cursor-pointer hover:shadow-lg transition-shadow border border-border">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Grades</CardTitle>
                <BookOpen className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">{dashboardData.grades}</div>
                <p className="text-xs text-muted-foreground">Active class sections</p>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* ✅ Quick Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-balance">Quick Stats</CardTitle>
              <CardDescription>Key performance indicators</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Male Students</span>
                  <Badge variant="default">{dashboardData.genderRatio.male}</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Female Students</span>
                  <Badge variant="secondary">{dashboardData.genderRatio.female}</Badge>
                </div>
                {dashboardData.campusDistribution.map((campus, idx) => (
                  <div key={idx} className="flex justify-between items-center">
                    <span className="text-sm font-medium">{campus.campus}</span>
                    <Badge variant="default">{campus.count}</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
        <Card className="mb-6">
  <CardHeader>
    <CardTitle>Gender Ratio</CardTitle>
    <CardDescription>Male vs Female Students</CardDescription>
  </CardHeader>
  <CardContent>
    <GenderPieChart
      male={dashboardData.genderRatio.male}
      female={dashboardData.genderRatio.female}
    />
  </CardContent>
</Card>
      </div>
    </div>
  )
}
