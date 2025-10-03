import graphene
from graphene_django import DjangoObjectType
from .models import Principal

class PrincipalType(DjangoObjectType):
    class Meta:
        model = Principal
        fields = "__all__"

class Query(graphene.ObjectType):
    all_principals = graphene.List(PrincipalType)
    principal_by_id = graphene.Field(PrincipalType, id=graphene.Int(required=True))

    def resolve_all_principals(root, info):
        return Principal.objects.all()

    def resolve_principal_by_id(root, info, id):
        try:
            return Principal.objects.get(id=id)
        except Principal.DoesNotExist:
            return None

class Mutation(graphene.ObjectType):
    pass  # baad me create/update mutations bhi bana sakti ho
