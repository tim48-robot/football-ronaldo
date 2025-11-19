import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [ # seharusnya kiri tuple untuk database, kanan untuk display
        ('jerseys', 'Football Jerseys'),
        ('equipment', 'Football Equipment and Accessories'),
        ('balls', 'Footballs'),
        ('goalkeeper', 'Goalkeeper Gear'),
        ('casual', 'Casual Wear and Merchandise')
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jerseys')
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name
    
    @property
    def is_featured_bool(self):
        return self.views > 20
        
    def increment_views(self):
        self.views += 1
        self.save()

##bikn model baru employee fields(255 character) name age(bilangan bulat) persona(textpanjang)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=1)
    personality = models.TextField() 

    def __str__(self):
        return self.name

##membuat model book id uuid title charfield max_length 255 
## author field bio textfield, biography. BOOKS one to many, 
## user? one to one realtion ke satu author? 

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)

class Author(models.Model):
    bio = models.TextField()
    books = models.ManyToManyField(Book)   
    user = models.OneToOneField(User, on_delete=models.CASCADE)

