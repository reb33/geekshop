from django import forms
from django.forms import ModelForm, CharField, TextInput, DecimalField, IntegerField, ChoiceField, FileField, \
    ModelChoiceField

from authapp.forms import ShopUserRegistrationForm, UserProfileForm
from authapp.models import ShopUser
from authapp.validators import check_size_file
from products.models import ProductCategory, Product


class AdminUserRegistrationForm(ShopUserRegistrationForm):
    avatar = forms.FileField(widget=forms.FileInput, required=False, validators=[check_size_file])

    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'avatar', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-label'


class AdminUserEditForm(UserProfileForm):
    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class CategoryForm(ModelForm):
    name = CharField(widget=TextInput())
    description = CharField(widget=TextInput(), required=False)

    class Meta:
        model = ProductCategory
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class ProductForm(ModelForm):
    name = CharField(max_length=100)
    img = FileField(widget=forms.FileInput, required=False)
    price = DecimalField(decimal_places=2, max_digits=7)
    desc = CharField(max_length=100)
    quality = IntegerField()
    category = ModelChoiceField(queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'img', 'price', 'desc', 'quantity', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['category'].widget.attrs['class'] = 'form-control py-2'
        self.fields['img'].widget.attrs['class'] = 'custom-file-label'
        # if self.category:
        #     self.fields['category'].widget.choices = self.category
