import graphene
import dummy.schema


# Our Project Level Schema 🚒 🔥
# If we had multiple apps, we'd import them here ✈
# Then, inherit from their Queries and Mutations 👦
# And, finally return them as one object 💧

class Query(dummy.schema.CategoryQuery,
            graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(dummy.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
