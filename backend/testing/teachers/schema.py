# import graphene
# from graphene_django import DjangoObjectType
# from .models import Teacher, TeacherEducation, TeacherExperience, TeacherSummary


# # ================== TYPES ==================

# class TeacherEducationType(DjangoObjectType):
#     class Meta:
#         model = TeacherEducation
#         fields = "__all__"


# class TeacherExperienceType(DjangoObjectType):
#     class Meta:
#         model = TeacherExperience
#         fields = "__all__"


# class TeacherSummaryType(DjangoObjectType):
#     class Meta:
#         model = TeacherSummary
#         fields = "__all__"


# class TeacherType(DjangoObjectType):
#     class Meta:
#         model = Teacher
#         fields = "__all__"


# # ================== QUERIES ==================

# class Query(graphene.ObjectType):
#     teachers = graphene.List(TeacherType)
#     teacher = graphene.Field(TeacherType, id=graphene.Int(required=True))

#     teacher_educations = graphene.List(TeacherEducationType, teacher_id=graphene.Int())
#     teacher_experiences = graphene.List(TeacherExperienceType, teacher_id=graphene.Int())
#     teacher_summary = graphene.Field(TeacherSummaryType, teacher_id=graphene.Int(required=True))

#     def resolve_teachers(root, info):
#         return Teacher.objects.all()

#     def resolve_teacher(root, info, id):
#         return Teacher.objects.get(id=id)

#     def resolve_teacher_educations(root, info, teacher_id=None):
#         qs = TeacherEducation.objects.all()
#         if teacher_id:
#             qs = qs.filter(teacher_id=teacher_id)
#         return qs

#     def resolve_teacher_experiences(root, info, teacher_id=None):
#         qs = TeacherExperience.objects.all()
#         if teacher_id:
#             qs = qs.filter(teacher_id=teacher_id)
#         return qs

#     def resolve_teacher_summary(root, info, teacher_id):
#         return TeacherSummary.objects.filter(teacher_id=teacher_id).first()


# # ================== MUTATIONS ==================

# class CreateTeacher(graphene.Mutation):
#     class Arguments:
#         full_name = graphene.String(required=True)
#         date_of_birth = graphene.Date(required=True)
#         gender = graphene.String(required=True)
#         email = graphene.String(required=True)
#         contact_number = graphene.String()
#         permanent_address = graphene.String(required=True)
#         current_address = graphene.String()
#         marital_status = graphene.String()

#     teacher = graphene.Field(TeacherType)

#     @classmethod
#     def mutate(cls, root, info, full_name, date_of_birth, gender, email,
#                permanent_address, contact_number=None, current_address=None, marital_status=None):
#         teacher = Teacher(
#             full_name=full_name,
#             date_of_birth=date_of_birth,
#             gender=gender,
#             email=email,
#             permanent_address=permanent_address,
#             contact_number=contact_number,
#             current_address=current_address,
#             marital_status=marital_status
#         )
#         teacher.save()
#         return CreateTeacher(teacher=teacher)


# class UpdateTeacher(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         full_name = graphene.String()
#         contact_number = graphene.String()
#         current_address = graphene.String()
#         marital_status = graphene.String()

#     teacher = graphene.Field(TeacherType)

#     @classmethod
#     def mutate(cls, root, info, id, **kwargs):
#         teacher = Teacher.objects.get(pk=id)
#         for field, value in kwargs.items():
#             setattr(teacher, field, value)
#         teacher.save()
#         return UpdateTeacher(teacher=teacher)


# class DeleteTeacher(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)

#     ok = graphene.Boolean()

#     @classmethod
#     def mutate(cls, root, info, id):
#         teacher = Teacher.objects.get(pk=id)
#         teacher.delete()
#         return DeleteTeacher(ok=True)


# class Mutation(graphene.ObjectType):
#     create_teacher = CreateTeacher.Field()
#     update_teacher = UpdateTeacher.Field()
#     delete_teacher = DeleteTeacher.Field()


# # ================== ROOT SCHEMA ==================
# schema = graphene.Schema(query=Query, mutation=Mutation)
import graphene
from graphene_django.types import DjangoObjectType
from students.models import Student
from campus.models import Campus
from teachers.models import Teacher

# ================= Types =================

class CampusType(DjangoObjectType):
    class Meta:
        model = Campus
        fields = ("id", "name")


class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("id", "name", "gender", "campus")


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = (
            "id",
            "full_name",
            "dob",
            "gender",
            "contact_number",
            "email",
            "permanent_address",
            "current_address",
            "marital_status",
            "save_status",
        )

# Optional aggregate types
class CampusDistributionType(graphene.ObjectType):
    campus = graphene.String()
    count = graphene.Int()


class GenderRatioType(graphene.ObjectType):
    male = graphene.Int()
    female = graphene.Int()


# ================= Query =================

class Query(graphene.ObjectType):
    # Students
    students = graphene.List(StudentType)
    total_students = graphene.Int()
    gender_ratio = graphene.Field(GenderRatioType)
    campus_distribution = graphene.List(CampusDistributionType)

    # Teachers
    teachers = graphene.List(TeacherType)
    teacher = graphene.Field(TeacherType, id=graphene.ID(required=True))
    total_teachers = graphene.Int()

    # ===== Resolvers =====
    def resolve_students(root, info):
        return Student.objects.all()

    def resolve_total_students(root, info):
        return Student.objects.count()

    def resolve_gender_ratio(root, info):
        return GenderRatioType(
            male=Student.objects.filter(gender__iexact="male").count(),
            female=Student.objects.filter(gender__iexact="female").count(),
        )

    def resolve_campus_distribution(root, info):
        data = []
        for campus in Campus.objects.all():
            count = Student.objects.filter(campus=campus).count()
            data.append(CampusDistributionType(campus=campus.name, count=count))
        return data

    def resolve_teachers(root, info):
        return Teacher.objects.all()

    def resolve_teacher(root, info, id):
        try:
            return Teacher.objects.get(pk=id)
        except Teacher.DoesNotExist:
            return None

    def resolve_total_teachers(root, info):
        return Teacher.objects.count()


class Mutation(graphene.ObjectType):
    pass


# ================= Schema =================
schema = graphene.Schema(query=Query)

