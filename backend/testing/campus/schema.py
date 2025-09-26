# campus/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Campus


# ========== TYPES ==========
class CampusType(DjangoObjectType):
    class Meta:
        model = Campus
        fields = "__all__"


class CampusCountsType(graphene.ObjectType):
    total = graphene.Int()
    active = graphene.Int()
    inactive = graphene.Int()
    closed = graphene.Int()
    under_construction = graphene.Int()


# ========== QUERIES ==========
class Query(graphene.ObjectType):
    # List all campuses (with optional filters & pagination)
    campuses = graphene.List(
        CampusType,
        status=graphene.String(required=False),
        search=graphene.String(required=False),
        offset=graphene.Int(required=False, default_value=0),
        limit=graphene.Int(required=False, default_value=50),
    )

    # Get single campus
    campus = graphene.Field(CampusType, id=graphene.Int(required=True))

    # Campus counts (dashboard use case)
    campusCounts = graphene.Field(CampusCountsType)

    # ----- RESOLVERS -----
    def resolve_campuses(self, info, status=None, search=None, offset=0, limit=50):
        qs = Campus.objects.all()

        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(campus_name__icontains=search)

        return qs.order_by("id")[offset: offset + limit]

    def resolve_campus(self, info, id):
        try:
            return Campus.objects.get(pk=id)
        except Campus.DoesNotExist:
            return None

    def resolve_campusCounts(self, info):
        qs = Campus.objects.all()
        return CampusCountsType(
            total=qs.count(),
            active=qs.filter(status="active").count(),
            inactive=qs.filter(status="inactive").count(),
            closed=qs.filter(status="closed").count(),
            under_construction=qs.filter(status="under_construction").count(),
        )


# ========== MUTATIONS ==========
class CreateCampus(graphene.Mutation):
    class Arguments:
        campus_name = graphene.String(required=True)
        campus_code = graphene.String(required=True)
        address = graphene.String(required=True)
        languages_of_instruction = graphene.String(required=True)
        academic_year_start = graphene.types.datetime.Date(required=True)
        academic_year_end = graphene.types.datetime.Date(required=True)
        student_capacity = graphene.Int(required=True)

    campus = graphene.Field(CampusType)

    @classmethod
    def mutate(
        cls, root, info,
        campus_name, campus_code, address,
        languages_of_instruction,
        academic_year_start, academic_year_end,
        student_capacity
    ):
        campus = Campus(
            campus_name=campus_name,
            campus_code=campus_code,
            address=address,
            languages_of_instruction=languages_of_instruction,
            academic_year_start=academic_year_start,
            academic_year_end=academic_year_end,
            student_capacity=student_capacity,
        )
        campus.save()
        return CreateCampus(campus=campus)


class UpdateCampus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        campus_name = graphene.String(required=False)
        status = graphene.String(required=False)
        student_capacity = graphene.Int(required=False)

    campus = graphene.Field(CampusType)

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        try:
            campus = Campus.objects.get(pk=id)
        except Campus.DoesNotExist:
            return None

        for field, value in kwargs.items():
            setattr(campus, field, value)

        campus.save()
        return UpdateCampus(campus=campus)


class DeleteCampus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            campus = Campus.objects.get(pk=id)
            campus.delete()
            return DeleteCampus(ok=True)
        except Campus.DoesNotExist:
            return DeleteCampus(ok=False)


# ========== ROOT MUTATION ==========
class Mutation(graphene.ObjectType):
    create_campus = CreateCampus.Field()
    update_campus = UpdateCampus.Field()
    delete_campus = DeleteCampus.Field()
