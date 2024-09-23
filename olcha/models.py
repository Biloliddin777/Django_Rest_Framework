from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Group(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')
    image = models.ImageField(upload_to='category/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Groups'


class Product(BaseModel):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField(blank=True)
    discount = models.PositiveIntegerField(default=0, blank=True)
    quantity = models.PositiveIntegerField(default=0, blank=True)

    @property
    def discounted_price(self):
        return self.price * (1 - self.discount / 100) if self.discount else self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'


class Image(BaseModel):
    image = models.ImageField(upload_to='products/images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)

    @property
    def is_primary_image(self):
        return self.image if self.is_primary else None

    def __str__(self):
        return f"Image {self.id} for {self.product.name}"


class Attribute(BaseModel):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class AttributeValue(BaseModel):
    value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.value


class ProductAttribute(BaseModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attribute.name}: {self.value.value} for {self.product.name}"
