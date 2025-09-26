"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, MapPin, Calendar } from "lucide-react";
import { GraphQLClient, gql } from "graphql-request";
import { notFound } from "next/navigation";

interface StudentDetailPageProps {
  params: { id: string };
}

type Student = {
  id: string;
  name: string;
  dob: string;
  gender: string;
  address: string;
  fatherName: string;
  currentGrade: string;
  section: string;
  campus: { id: string; name: string };
};

export default function StudentDetailPage({ params }: StudentDetailPageProps) {
  const [student, setStudent] = useState<Student | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStudent = async () => {
      try {
        const client = new GraphQLClient("http://localhost:8000/graphql/");
        const query = gql`
          query GetStudent($id: Int!) {
            student(id: $id) {
              id
              name
              dob
              gender
              address
              fatherName
              currentGrade
              section
              campus {
                id
                name
              }
            }
          }
        `;
        const data = await client.request<{ student: Student }>(query, {
          id: Number(params.id),
        });
        setStudent(data.student);
      } catch (err) {
        console.error("Error fetching student:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStudent();
  }, [params.id]);

  if (loading) return <p className="p-6">Loading student details...</p>;
  if (!student) return notFound();

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto">
        <Link href="/students">
          <Button variant="outline" className="mb-6 bg-transparent">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Students List
          </Button>
        </Link>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">
              Student Details - {student.name}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-lg">Personal Information</h3>
                <p>
                  <b>Full Name:</b> {student.name}
                </p>
                <p>
                  <b>GR Number:</b> {student.id}
                </p>
                <p>
                  <b>Date of Birth:</b> {student.dob}
                </p>
                <p>
                  <b>Gender:</b> {student.gender}
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-lg">Contact Information</h3>
                <p className="flex items-start gap-2">
                  <MapPin className="w-4 h-4 mt-1" /> {student.address}
                </p>
                <p>
                  <b>Father's Name:</b> {student.fatherName}
                </p>
              </div>
            </div>

            <div className="border-t pt-6">
              <h3 className="font-semibold text-lg mb-4">Academic Information</h3>
              <p>
                <b>Current Grade:</b> {student.currentGrade}
              </p>
              <p>
                <b>Section:</b> {student.section}
              </p>
              <p>
                <b>Campus:</b> {student.campus?.name}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
