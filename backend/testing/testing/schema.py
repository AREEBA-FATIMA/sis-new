# testing/schema.py
import graphene
import students.schema
import teachers.schema
import campus.schema
import classes.schema

class Query(
    students.schema.Query,
    teachers.schema.Query,
    campus.schema.Query,
    classes.schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    students.schema.Mutation,
    teachers.schema.Mutation,
    campus.schema.Mutation,
    classes.schema.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
