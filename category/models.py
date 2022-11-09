from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from autoslug import AutoSlugField


# Create your models here.


# Category
class Category(models.Model):
    category_name   = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)



    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.category_name


# Sub Category
class SubCategory(models.Model):
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    slug            = AutoSlugField(populate_from='category',max_length=255,unique=True,null=True)
    sub_category    = models.CharField(max_length = 100)

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub categories'

    def __str__(self):
        return self.category.category_name +' - '+ self.sub_category


# Brands

class Brand(models.Model):

    # sub_category    = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
    name            = models.CharField(max_length = 100)
    slug            = AutoSlugField(populate_from='name',max_length=255,unique=True,null=True)
    image           = models.ImageField(upload_to = "photos/brands")


    def get_url(self):
        return reverse('product_by_brand', args=[self.slug])

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.name


# colors

class Color(models.Model):

    # sub_category    = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name            = models.CharField(max_length = 100)
    color_code      = models.CharField(max_length = 100)
    slug            =   AutoSlugField(populate_from='name',unique_with=('color_code'),max_length=255,unique=True,null=True)


    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s" ></div>' % (self.color_code))


    def __str__(self):
        return self.name


# size

class Size(models.Model):
    # sub_category    = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    size            = models.CharField(max_length = 100)
    slug            = AutoSlugField(populate_from='size',max_length=255,unique=True,null=True)



    def __str__(self):
        return self.size
