"use client";
import { useEffect, useState } from "react";
import { request, gql } from "graphql-request";

const API_URL = "http://127.0.0.1:8000/graphql/";

interface Education {
  level: string;
  institutionName: string;
  yearOfPassing: number;
  subjects: string;
  grade: string;
}

interface Experience {
  institutionName: string;
  position: string;
  fromDate: string;
  toDate: string;
  subjectsClassesTaught: string;
  responsibilities: string;
  totalYears: number;
}

interface Role {
  roleTitle: string;
  campus: { name: string };
  subjects: string;
  classesTaught: string;
  extraResponsibilities: string;
  startDate: string;
  endDate: string | null;
  isActive: boolean;
}

interface Teacher {
  id: string;
  fullName: string;
  gender: string;
  contactNumber: string;
  email: string;
  permanentAddress: string;
  currentAddress: string;
  maritalStatus: string;
  saveStatus: string;
  educations: Education[];
  experiences: Experience[];
  roles: Role[];
}

interface TeachersResponse {
  teachers: Teacher[];
}

export default function TeachersDashboard() {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [selectedTeacher, setSelectedTeacher] = useState<Teacher | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeachers = async () => {
      try {
        const query = gql`
          query {
            teachers {
              id
              fullName
              gender
              contactNumber
              email
              permanentAddress
              currentAddress
              maritalStatus
              saveStatus
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
                subjectsClassesTaught
                responsibilities
                totalYears
              }
              roles {
                roleTitle
                campus {
                  name
                }
                subjects
                classesTaught
                extraResponsibilities
                startDate
                endDate
                isActive
              }
            }
          }
        `;

        const data = await request<TeachersResponse>(API_URL, query);
        setTeachers(data.teachers);
      } catch (error) {
        console.error("Error fetching teachers:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTeachers();
  }, []);

  const handleViewDetails = (teacher: Teacher) => {
    setSelectedTeacher(teacher);
  };

  const closeModal = () => {
    setSelectedTeacher(null);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 sm:p-8 text-black">
      <div className="max-w-7xl mx-auto">
        {/* Dashboard Heading */}
        <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
          <span className="mr-2">📚</span> Teachers Dashboard
        </h1>

        {/* Stats Card */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-700">
            Total Teachers:{" "}
            <span className="text-blue-600">{teachers.length}</span>
          </h2>
        </div>

        {/* Teachers Table */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            Teachers List
          </h2>

          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-lg font-semibold text-gray-600">
                Loading...
              </div>
            </div>
          ) : teachers.length === 0 ? (
            <div className="text-center py-6 text-gray-500">
              No teachers found.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse text-sm sm:text-base">
                <thead>
                  <tr className="bg-blue-50 text-left text-gray-700">
                    <th className="px-4 py-3 font-semibold rounded-tl-lg">ID</th>
                    <th className="px-4 py-3 font-semibold">Full Name</th>
                    <th className="px-4 py-3 font-semibold">Email</th>
                    <th className="px-4 py-3 font-semibold">Gender</th>
                    <th className="px-4 py-3 font-semibold">Contact</th>
                    <th className="px-4 py-3 font-semibold">View</th>
                  </tr>
                </thead>
                <tbody>
                  {teachers.map((teacher, index) => (
                    <tr
                      key={teacher.id}
                      className={`${
                        index % 2 === 0 ? "bg-white" : "bg-gray-50"
                      } hover:bg-blue-100 transition-colors`}
                    >
                      <td className="px-4 py-3 border-b border-gray-200">
                        {teacher.id}
                      </td>
                      <td className="px-4 py-3 border-b border-gray-200">
                        {teacher.fullName}
                      </td>
                      <td className="px-4 py-3 border-b border-gray-200">
                        {teacher.email}
                      </td>
                      <td className="px-4 py-3 border-b border-gray-200">
                        {teacher.gender}
                      </td>
                      <td className="px-4 py-3 border-b border-gray-200">
                        {teacher.contactNumber}
                      </td>
                      <td className="px-4 py-3 border-b border-gray-200">
                        <button
                          onClick={() => handleViewDetails(teacher)}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          👁️ View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Modal for Teacher Details */}
        {selectedTeacher && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                {selectedTeacher.fullName} - Details
              </h2>
              <div className="space-y-4">
                {/* Basic Details */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-700">
                    Basic Information
                  </h3>
                  <p><strong>ID:</strong> {selectedTeacher.id}</p>
                  <p><strong>Gender:</strong> {selectedTeacher.gender}</p>
                  <p><strong>Contact:</strong> {selectedTeacher.contactNumber}</p>
                  <p><strong>Email:</strong> {selectedTeacher.email}</p>
                  <p><strong>Permanent Address:</strong> {selectedTeacher.permanentAddress}</p>
                  <p><strong>Current Address:</strong> {selectedTeacher.currentAddress}</p>
                  <p><strong>Marital Status:</strong> {selectedTeacher.maritalStatus}</p>
                  <p><strong>Save Status:</strong> {selectedTeacher.saveStatus}</p>
                </div>

                {/* Educations */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-700">Educations</h3>
                  {selectedTeacher.educations.length > 0 ? (
                    <ul className="list-disc pl-5">
                      {selectedTeacher.educations.map((edu, index) => (
                        <li key={index} className="mb-2">
                          <p><strong>Level:</strong> {edu.level}</p>
                          <p><strong>Institution:</strong> {edu.institutionName}</p>
                          <p><strong>Year of Passing:</strong> {edu.yearOfPassing}</p>
                          <p><strong>Subjects:</strong> {edu.subjects}</p>
                          <p><strong>Grade:</strong> {edu.grade}</p>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500">No education details available.</p>
                  )}
                </div>

                {/* Experiences */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-700">Experiences</h3>
                  {selectedTeacher.experiences.length > 0 ? (
                    <ul className="list-disc pl-5">
                      {selectedTeacher.experiences.map((exp, index) => (
                        <li key={index} className="mb-2">
                          <p><strong>Institution:</strong> {exp.institutionName}</p>
                          <p><strong>Position:</strong> {exp.position}</p>
                          <p><strong>From:</strong> {exp.fromDate}</p>
                          <p><strong>To:</strong> {exp.toDate}</p>
                          <p><strong>Subjects/Classes Taught:</strong> {exp.subjectsClassesTaught}</p>
                          <p><strong>Responsibilities:</strong> {exp.responsibilities}</p>
                          <p><strong>Total Years:</strong> {exp.totalYears}</p>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500">No experience details available.</p>
                  )}
                </div>

                {/* Roles */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-700">Roles</h3>
                  {selectedTeacher.roles.length > 0 ? (
                    <ul className="list-disc pl-5">
                      {selectedTeacher.roles.map((role, index) => (
                        <li key={index} className="mb-2">
                          <p><strong>Role Title:</strong> {role.roleTitle}</p>
                          <p><strong>Campus:</strong> {role.campus.name}</p>
                          <p><strong>Subjects:</strong> {role.subjects}</p>
                          <p><strong>Classes Taught:</strong> {role.classesTaught}</p>
                          <p><strong>Extra Responsibilities:</strong> {role.extraResponsibilities}</p>
                          <p><strong>Start Date:</strong> {role.startDate}</p>
                          <p><strong>End Date:</strong> {role.endDate || "N/A"}</p>
                          <p><strong>Active:</strong> {role.isActive ? "Yes" : "No"}</p>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500">No role details available.</p>
                  )}
                </div>
              </div>
              <button
                onClick={closeModal}
                className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}