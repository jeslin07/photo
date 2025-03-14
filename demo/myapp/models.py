from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class SaveTheDate(models.Model):
    PHOTOGRAPHY_STYLE_CHOICES = [
        ('traditional', 'Traditional'),
        ('photojournalistic', 'Photojournalistic'),
        ('artistic', 'Artistic'),
        ('aerial', 'Aerial'),
        ('portrait', 'Portrait-focused'),
        ('black_and_white', 'Black & White'),
    ]
    
    BUDGET_CHOICES = [
        ('1000-2000', '$1,000 - $2,000'),
        ('2000-3000', '$2,000 - $3,000'),
        ('3000-4000', '$3,000 - $4,000'),
        ('4000-5000', '$4,000 - $5,000'),
        ('5000+', '$5,000+'),
    ]
    
    couples_names = models.CharField(max_length=100, verbose_name="Couple's Names")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone Number",
        validators=[phone_validator],
        help_text="Enter your phone number in the format: '+999999999'. Up to 15 digits allowed."
    )
    wedding_date = models.DateField(verbose_name="Wedding Date")
    venue = models.CharField(max_length=255, blank=True, null=True, verbose_name="Wedding Venue")
    photography_style = models.CharField(
        max_length=50,
        choices=PHOTOGRAPHY_STYLE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Preferred Photography Style"
    )
    budget = models.CharField(
        max_length=50,
        choices=BUDGET_CHOICES,
        blank=True,
        null=True,
        verbose_name="Approximate Budget"
    )
    message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Additional Details",
        help_text="Please provide any additional details about your wedding."
    )
    submitted_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Submission Date")
    is_contacted = models.BooleanField(default=False, verbose_name="Has Been Contacted")
    contacted_at = models.DateTimeField(blank=True, null=True, verbose_name="Contacted At")
    
    def __str__(self):
        return f"{self.couples_names} - {self.wedding_date}"
    
    def clean(self):
        super().clean()
        # Validate wedding date
        if self.wedding_date and self.wedding_date < timezone.now().date():
            raise ValidationError({'wedding_date': 'Wedding date cannot be in the past. Please select a future date.'})
        # Validate message length
        if self.message and len(self.message) < 10:
            raise ValidationError({'message': 'Additional details must be at least 10 characters long.'})
    
    class Meta:
        verbose_name = "Wedding Booking"
        verbose_name_plural = "Wedding Bookings"
        ordering = ['-wedding_date']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(
        default='https://example.com/default-image.jpg',  # Placeholder image URL
        blank=True,
        null=True,
        help_text="URL of the product image."
    )

    def __str__(self):
        return self.name