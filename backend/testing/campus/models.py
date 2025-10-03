import graphene
from graphene_django import DjangoObjectType
from .models import Campus

# ---------------------
# GraphQL Type
# ---------------------
class CampusType(DjangoObjectType):
    class Meta:
        model = Campus
        fields = "__all__"

# ---------------------
# Queries
# ---------------------
class Query(graphene.ObjectType):
    all_campuses = graphene.List(CampusType, description="Get all campuses")
    campus_by_id = graphene.Field(
        CampusType,
        id=graphene.Int(required=True),
        description="Get a campus by ID"
    )

    def resolve_all_campuses(root, info, **kwargs):
        return Campus.objects.all()

    def resolve_campus_by_id(root, info, id):
        try:
            return Campus.objects.get(id=id)
        except Campus.DoesNotExist:
            return None

# ---------------------
# Mutations
# ---------------------
class CreateCampus(graphene.Mutation):
    class Arguments:
        campus_name = graphene.String(required=True)
        campus_code = graphene.String(required=True)
        campus_type = graphene.String(required=False)
        city = graphene.String(required=True)
        address = graphene.String(required=True)
        primary_phone = graphene.String(required=False)
        official_email = graphene.String(required=False)
        student_capacity = graphene.Int(required=False)
        status = graphene.String(required=False)

    campus = graphene.Field(CampusType)

    def mutate(
        self,
        info,
        campus_name,
        campus_code,
        city,
        address,
        campus_type="main",
        primary_phone=None,
        official_email=None,
        student_capacity=0,
        status="active"
    ):
        campus = Campus(
            campus_name=campus_name,
            campus_code=campus_code,
            campus_type=campus_type,
            city=city,
            address=address,
            primary_phone=primary_phone,
            official_email=official_email,
            student_capacity=student_capacity,
            status=status,
        )
        campus.save()
        return CreateCampus(campus=campus)

class Mutation(graphene.ObjectType):
    create_campus = CreateCampus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
