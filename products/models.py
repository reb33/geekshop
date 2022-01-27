from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='products_uploads/', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    desc = models.TextField(max_length=100)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def get_items():
        # закоментил так как при редактировании заказа удаленные не показываются
        # return Product.objects.filter(is_active=True).order_by('category', 'name')
        return Product.objects.all().order_by('category', 'name')

    def __str__(self):
        return f'{self.name} | {self.category}'
