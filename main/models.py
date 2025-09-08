from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [ # seharusnya kiri tuple untuk database, kanan untuk display
        ('jerseys', 'Football Jerseys'),
        ('equipment', 'Football Equipment and Accessories'),
        ('balls', 'Footballs'),
        ('goalkeeper', 'Goalkeeper Gear'),
        ('casual', 'Casual Wear and Merchandise')
    ]
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
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