from django.db import models

from django.core.exceptions import ValidationError

# Create your models here
class Company(models.Model):
    company_id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False)
    compay_name = models.CharField(max_length=200)
    company_about = models.TextField(max_length=1000)
    company_email = models.EmailField()
    mobile_number = models.IntegerField(max_length=15)
    company_website = models.CharField(max_length=100)
    
    class CompanyType(models.Choices):
        PROFIT = "Profit"
        NON_PROFIT = "Non-Profit" 
    company_type = models.CharField(max_length=20, choices=CompanyType.choices)
    size = models.IntegerField()
    headquaters = models.CharField(max_length=200)
    company_image = models.ImageField(upload_to='company_images/')
    industry = models.CharField(max_length=200)
    founded_year = models.DateField()


    def clean(self):
        number = self.mobile_number.strip()

        # Only digits allowed in mobile number field
        if not number.isdigit():
            raise ValidationError({
                "mobile_number": "Enter digits only."
            })

        required_length = rules.get(self.country_code)

        if required_length and len(number) != required_length:
            raise ValidationError({
                "mobile_number": f"For {self.country_code}, enter exactly {required_length} digits."
            })

    def save(self, *args, **kwargs):
        self.full_clean()   # Run validation before saving
        super().save(*args, **kwargs)