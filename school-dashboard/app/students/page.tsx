"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";
import { GraphQLClient, gql } from "graphql-request";
import { Button } from "@/components/ui/button";

type StudentListItem = {
  id: string;
  name: string;
  gender: string;
  currentGrade: string;
  section: string;
  campus: { name: string };
};

export default function StudentsPage() {
  const [students, setStudents] = useState<StudentListItem[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedCampus, setSelectedCampus] = useState("all");
  const [selectedGender, setSelectedGender] = useState("all");
  const [selectedGrade, setSelectedGrade] = useState("all");

  const campuses = ["Campus 1","Campus 2","Campus 3","Campus 4","Campus 5","Campus 6","Campus 7"];
  const genders = ["all", "male", "female"];
  const grades = ["all", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"];

  const STUDENTS_FILTERED = gql`
    query GetStudents($campusName: String, $gender: String, $grade: String) {
      studentsFiltered(campusName: $campusName, gender: $gender, grade: $grade) {
        id
        name
        gender
        currentGrade
        section
        campus {
          name
        }
      }
    }
  `;

  useEffect(() => {
    const fetchStudents = async () => {
      setLoading(true);
      try {
        const client = new GraphQLClient("http://localhost:8000/graphql/");
        const data = await client.request<{ studentsFiltered: StudentListItem[] }>(
          STUDENTS_FILTERED,
          {
            campusName: selectedCampus === "all" ? null : selectedCampus,
            gender: selectedGender === "all" ? null : selectedGender,
            grade: selectedGrade === "all" ? null : selectedGrade,
          }
        );
        setStudents(data.studentsFiltered);
      } catch (error) {
        console.error("Error fetching students:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, [selectedCampus, selectedGender, selectedGrade]);

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-5xl mx-auto space-y-6">
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <h1 className="text-2xl font-bold">Students</h1>

          {/* Campus Filter */}
          <Select onValueChange={setSelectedCampus} defaultValue="all">
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select Campus" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Campuses</SelectItem>
              {campuses.map((campus) => (
                <SelectItem key={campus} value={campus}>
                  {campus}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Gender Filter */}
          <Select onValueChange={setSelectedGender} defaultValue="all">
            <SelectTrigger className="w-[150px]">
              <SelectValue placeholder="Select Gender" />
            </SelectTrigger>
            <SelectContent>
              {genders.map((g) => (
                <SelectItem key={g} value={g}>
                  {g}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* Grade Filter */}
          <Select onValueChange={setSelectedGrade} defaultValue="all">
            <SelectTrigger className="w-[150px]">
              <SelectValue placeholder="Select Grade" />
            </SelectTrigger>
            <SelectContent>
              {grades.map((gr) => (
                <SelectItem key={gr} value={gr}>
                  {gr}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex items-center gap-2">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Loading students...</span>
          </div>
        )}

        {/* Students List */}
        {!loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {students.map((student) => (
              <Card key={student.id} className="cursor-pointer hover:shadow-md transition">
                <CardHeader>
                  <CardTitle className="text-lg">{student.name}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm text-muted-foreground">
                  <p>Campus: {student.campus?.name || "N/A"}</p>
                  <p>Grade: {student.currentGrade || "-"}</p>
                  <p>Section: {student.section || "-"}</p>
                  <p>Gender: {student.gender}</p>
                  <Link href={`/students/${student.id}`}>
                    <Button className="mt-2 w-full" size="sm">
                      View Details
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
