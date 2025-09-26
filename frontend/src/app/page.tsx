"use client";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function StudentsDashboard() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const query = `
      query {
        totalTeachers
        totalStudents
        campusCounts {
          total
        }
      }
    `;

    fetch("http://127.0.0.1:8000/graphql/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    })
      .then((res) => res.json())
      .then((result) => {
        setData({
          totalStudents: result.data.totalStudents || 2000,
          totalTeachers: result.data.totalTeachers || 100,
          totalCampuses: result.data.campusCounts?.total || 8,
        });
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setData({
          totalStudents: 2000,
          totalTeachers: 100,
          totalCampuses: 8,
        });
      });
  }, []);

  if (!data)
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-lg font-semibold text-gray-600">Loading...</div>
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-100 p-6 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">
          📊 Students Dashboard
        </h1>

        {/* Total Students, Total Teachers, and Total Campuses Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-6">
          {/* Total Students Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Total Students
            </h2>
            <p className="text-3xl font-bold text-blue-600">
              {data.totalStudents}
            </p>
          </div>

          {/* Total Teachers Card */}
          <Link href="/Maincompuntents/teachers">
            <div className="bg-white rounded-lg shadow-md p-6 hover:bg-blue-50 transition-colors">
              <h2 className="text-xl font-semibold text-gray-700 mb-2">
                Total Teachers
              </h2>
              <p className="text-3xl font-bold text-blue-600">
                {data.totalTeachers}
              </p>
            </div>
          </Link>

          {/* Total Campuses Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Total Campuses
            </h2>
            <p className="text-3xl font-bold text-blue-600">
              {data.totalCampuses}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}