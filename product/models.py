from django.db import models
import mptt
from mptt.admin import DraggableMPTTAdmin
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import Avg, Count
# Create your models here.
class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    short_description=models.TextField(max_length=255)
    long_description=RichTextUploadingField()
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})    

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<div class="single-slider overlay" style="background-image: {}">'.format(self.image))
        else:
            return ""    

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    SIZE = (
        ('None', 'None'),
        ('Size', 'Small'),
        ('Medium','Medium'),
        ('Large','Large'),
    )
    GENDER=(
        ('Men','Men'),
        ('Women','Women'),
    )
    WOMEN_BRAND=(
        ('None','None'),
        ('Nishat','Nishat'),
        ('Bareeze','Bareeze'),
        ('Khaadi','Khaadi'),
        ('Limelight','Limelight'),
        ('Maria B','Maria B'),
        ('Gul Ahmed','Gul Ahmed'),
        ('Junaid Jamshed','Junaid Jamshed'),
    )
    MEN_BRAND=(
        ('None','None'),
        ('Levi','Levi'),
        ('People Jeans','People Jeans'),
        ('Lee','Lee'),
        ('Adidas','Adidas'),
        ('Flying Machine','Flying Machine'),
    )
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'), 
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    long_description=RichTextUploadingField(default='Write Your long Description here')
    image=models.ImageField(upload_to='images/',null=False)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    quantity=models.IntegerField(default=0)
    women_brand=models.CharField(max_length=100,choices=WOMEN_BRAND,default='None')
    men_brand=models.CharField(max_length=100,choices=MEN_BRAND,default='None')
    gender=models.CharField(max_length=100, choices=GENDER,default='None')
    size=models.CharField(max_length=100,choices=SIZE, default='None')
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    num_of_visits=models.IntegerField(default=0)
    last_visit=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return "" 

    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt        

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    email = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate','email','name']

