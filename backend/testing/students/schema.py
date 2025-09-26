import graphene
from graphene_django.types import DjangoObjectType
from .models import Student
from campus.models import Campus


# CampusType
class CampusType(DjangoObjectType):
    class Meta:
        model = Campus
        fields = ("id", "name")


# StudentType
class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = "__all__"   # 👈 abhi ke liye saare fields expose kar do


# Campus distribution type
class CampusDistributionType(graphene.ObjectType):
    campus = graphene.String()
    count = graphene.Int()


# Gender ratio type
class GenderRatioType(graphene.ObjectType):
    male = graphene.Int()
    female = graphene.Int()


# Main Query
class Query(graphene.ObjectType):
    students = graphene.List(StudentType)
    student = graphene.Field(StudentType, id=graphene.Int(required=True))
    students_by_campus_name = graphene.List(
        StudentType, campus_name=graphene.String(required=True)
    )
    students_by_campus_id = graphene.List(
        StudentType, campus_id=graphene.Int(required=True)
    )

    # 👇 New: filter by campus, gender, grade
    students_filtered = graphene.List(
        StudentType,
        campus_name=graphene.String(),
        gender=graphene.String(),
        grade=graphene.String(),
    )

    total_students = graphene.Int()
    gender_ratio = graphene.Field(GenderRatioType)
    campus_distribution = graphene.List(CampusDistributionType)

    # --- All students
    def resolve_students(root, info):
        return Student.objects.all()

    # --- Student by ID
    def resolve_student(root, info, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist:
            return None

    # --- Students by campus name
    def resolve_students_by_campus_name(root, info, campus_name):
        return Student.objects.filter(campus__name__iexact=campus_name)

    # --- Students by campus ID
    def resolve_students_by_campus_id(root, info, campus_id):
        return Student.objects.filter(campus__id=campus_id)

    # --- Students filtered by campus, gender, grade
    def resolve_students_filtered(root, info, campus_name=None, gender=None, grade=None):
        qs = Student.objects.all()
        if campus_name and campus_name.lower() != "all":
            qs = qs.filter(campus__name__iexact=campus_name)
        if gender and gender.lower() != "all":
            qs = qs.filter(gender__iexact=gender)
        if grade and grade.lower() != "all":
            qs = qs.filter(current_grade__iexact=grade)
        return qs

    # --- Total students
    def resolve_total_students(root, info):
        return Student.objects.count()

    # --- Gender ratio
    def resolve_gender_ratio(root, info):
        return GenderRatioType(
            male=Student.objects.filter(gender__iexact="male").count(),
            female=Student.objects.filter(gender__iexact="female").count(),
        )

    # --- Campus distribution
    def resolve_campus_distribution(root, info):
        data = []
        for campus in Campus.objects.all():
            count = Student.objects.filter(campus=campus).count()
            data.append(CampusDistributionType(campus=campus.name, count=count))
        return data


# Mutation (abhi blank)
class Mutation(graphene.ObjectType):
    pass


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
