from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        db_table = 'categories'


class Group(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ManyToManyField(Category, related_name='groups')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Groups'
        db_table = 'groups'


class Product(BaseModel):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField(blank=True, null=True)
    discount = models.IntegerField(default=0, blank=True)
    quantity = models.PositiveIntegerField(default=0, blank=True)

    @property
    def discounted_price(self):
        if self.price and self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'products'


class Image(BaseModel):
    image = models.ImageField(upload_to='products/images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)

    @property
    def is_primary_image(self):
        return self.image if self.is_primary else None

    def __str__(self):
        return f'Image of {self.product.name}'

    class Meta:
        db_table = 'images'


class Attribute(BaseModel):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'attributes'


class AttributeValue(BaseModel):
    value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'attribute_values'


class ProductAttribute(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'value', 'product')
        db_table = 'product_attributes'
