from django import forms
from .models import Category


class CategoryForm(forms.Form):
    name = forms.CharField(required=True)
    parent = forms.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'parent')

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        if cleaned_data['parent']:
            if not Category.objects.filter(id=cleaned_data['parent']).exists():
                raise forms.ValidationError(f"Parent I`d {cleaned_data['parent']} is not Exists !!")
            else:
                cleaned_data['parent'] = Category.objects.get(id=cleaned_data['parent'])
        return cleaned_data