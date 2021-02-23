from graphene_django import DjangoObjectType
import graphene
from .models import *
from .upload import Upload
from graphene_file_upload.scalars import Upload
from .forms import CategoryForm
import json

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class CategoryQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.ID())
    child_categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, id):
        return Category.objects.get(id=id)
    
    def resolve_child_categories(self, info, **kwargs):
        return Category.objects.filter(parent__isnull=True).get_descendants(include_self=True)



# ******************* 😎 CATEGORY-MUTATIONS 😎 *************************#
class CreateCategory(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String()
        parent = graphene.Int()
    
    success = graphene.Boolean()
    category = graphene.Field(CategoryType)
    errors = graphene.String()

    @classmethod
    def mutate(cls, root, info, **data):
        form = CategoryForm(data)
        if form.is_valid():
            category = Category.objects.create(
                name=form.cleaned_data['name'], parent=form.cleaned_data['parent']
            )
            # We've done this so many times, it no longer feels weird 😃
            return CreateCategory( success=True, category=category, errors=None)
        else:
            error =  eval(form.errors.as_json())
            if '__all__' in error:
                error = error['__all__'][0]['message']
            return CreateCategory(success=False, errors=error)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()
        name = graphene.String()
        parent = graphene.Int()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name, parent=None):
        category = Category.objects.get(pk=id)
        category.name = name if name is not None else category.name
        category.parent = Category.objects.get(id=parent) if parent else None
        category.save()
        # Notice we return an instance of this mutation 🤷‍♀️
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.ID()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    def mutate(self, info, id):
        category = Category.objects.get(pk=id)
        if category is not None:
            # Notice we don't do category.delete()? Thats because we must not 😓
            category.delete()
        # Notice we return an instance of this mutation 🤷‍♀️
        return DeleteCategory(category=category)


# ***************** 🔥🔥🔥 Wiring up the mutations 🔥🔥🔥 *******************#
class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()


