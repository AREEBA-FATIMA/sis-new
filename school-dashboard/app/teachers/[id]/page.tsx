"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Phone, Mail, MapPin, Calendar } from "lucide-react"
import { notFound } from "next/navigation"
import { request, gql } from "graphql-request"

interface Teacher {
  id: string
  fullName: string
  gender: string
  contactNumber: string
  email: string
  maritalStatus: string
  permanentAddress: string
  currentAddress: string
  roles: {
    roleTitle: string
    campus: { name: string }
    subjects: string[]
    startDate: string
    endDate: string
    isActive: boolean
  }[]
  educations: {
    level: string
    institutionName: string
    yearOfPassing: string
    subjects: string
    grade: string
  }[]
  experiences: {
    institutionName: string
    position: string
    fromDate: string
    toDate: string
    responsibilities: string
    totalYears: number
  }[]
}

interface TeacherDetailPageProps {
  params: { id: string }
}

export default function TeacherDetailPage({ params }: TeacherDetailPageProps) {
  const [teacher, setTeacher] = useState<Teacher | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTeacher = async () => {
      try {
        const query = gql`
          query GetTeacher($id: ID!) {
            teacher(id: $id) {
              id
              fullName
              gender
              contactNumber
              email
              maritalStatus
              permanentAddress
              currentAddress
              roles {
                roleTitle
                campus { name }
                subjects
                startDate
                endDate
                isActive
              }
              educations {
                level
                institutionName
                yearOfPassing
                subjects
                grade
              }
              experiences {
                institutionName
                position
                fromDate
                toDate
                responsibilities
                totalYears
              }
            }
          }
        `
        const data = await request<{ teacher: Teacher }>(
          "http://localhost:8000/graphql/",
          query,
          { id: params.id }
        )

        if (!data.teacher) notFound()
        setTeacher(data.teacher)
      } catch (error) {
        console.error("Error fetching teacher:", error)
      } finally {
        setLoading(false)
      }
    }
    fetchTeacher()
  }, [params.id])

  if (loading) return <p className="p-6 text-center">Loading teacher details...</p>
  if (!teacher) return <p className="p-6 text-center text-red-500">Teacher not found</p>

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto">
        <Link href="/teachers">
          <Button variant="outline" className="mb-6 bg-transparent">
            <ArrowLeft className="w-4 h-4 mr-2" /> Back to Teachers List
          </Button>
        </Link>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">
              Teacher Details - {teacher.fullName}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-8">
            {/* Basic Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-lg">Professional Info</h3>
                <p><Mail className="w-4 h-4 inline mr-2" /> {teacher.email}</p>
                <p><Phone className="w-4 h-4 inline mr-2" /> {teacher.contactNumber}</p>
                <p>Gender: {teacher.gender}</p>
                <p>Marital Status: {teacher.maritalStatus}</p>
              </div>
              <div>
                <h3 className="font-semibold text-lg">Assignment</h3>
                <p>Campus: {teacher.roles[0]?.campus?.name || "No campus"}</p>
                <p>Role: {teacher.roles[0]?.roleTitle || "No role"}</p>
                <p>Subjects: {teacher.roles[0]?.subjects?.join(", ") || "N/A"}</p>
                <p><Calendar className="w-4 h-4 inline mr-2" /> Joined: {teacher.roles[0]?.startDate || "N/A"}</p>
              </div>
            </div>

            {/* Address */}
            <div className="border-t pt-6">
              <h3 className="font-semibold text-lg mb-4">Address</h3>
              <p><MapPin className="w-4 h-4 inline mr-2" /> {teacher.currentAddress || teacher.permanentAddress}</p>
            </div>

            {/* Roles */}
            {teacher.roles.length > 0 && (
              <div className="border-t pt-6">
                <h3 className="font-semibold text-lg mb-4">Roles</h3>
                <ul className="space-y-4">
                  {teacher.roles.map((role, idx) => (
                    <li key={idx} className="p-3 border rounded-lg">
                      <p><b>Role:</b> {role.roleTitle}</p>
                      <p><b>Campus:</b> {role.campus?.name}</p>
                      <p><b>Subjects:</b> {role.subjects?.join(", ") || "N/A"}</p>
                      <p><b>Active:</b> {role.isActive ? "Yes" : "No"}</p>
                      <p><b>Duration:</b> {role.startDate} - {role.endDate || "Present"}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Education */}
            {teacher.educations.length > 0 && (
              <div className="border-t pt-6">
                <h3 className="font-semibold text-lg mb-4">Education</h3>
                <ul className="space-y-4">
                  {teacher.educations.map((edu, idx) => (
                    <li key={idx} className="p-3 border rounded-lg">
                      <p><b>Level:</b> {edu.level}</p>
                      <p><b>Institution:</b> {edu.institutionName}</p>
                      <p><b>Year of Passing:</b> {edu.yearOfPassing}</p>
                      <p><b>Subjects:</b> {edu.subjects}</p>
                      <p><b>Grade:</b> {edu.grade}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Experience */}
            {teacher.experiences.length > 0 && (
              <div className="border-t pt-6">
                <h3 className="font-semibold text-lg mb-4">Experience</h3>
                <ul className="space-y-4">
                  {teacher.experiences.map((exp, idx) => (
                    <li key={idx} className="p-3 border rounded-lg">
                      <p><b>Institution:</b> {exp.institutionName}</p>
                      <p><b>Position:</b> {exp.position}</p>
                      <p><b>From:</b> {exp.fromDate} - <b>To:</b> {exp.toDate}</p>
                      <p><b>Responsibilities:</b> {exp.responsibilities}</p>
                      <p><b>Total Years:</b> {exp.totalYears}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
