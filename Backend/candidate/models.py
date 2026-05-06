from django.db import models

from django.core.exceptions import ValidationError
from ..utils.countryCode import *


# Create your models here.
class Candidate(models.Model):

    class Gender(models.gender_choices):
        MALE = 'male','Male'
        FEMALE = 'female','Female'
        OTHERS = 'others','Others'
        PREFER_NOT_TO_SAY = 'prefer_not_to_say','Prefer Not To Say'


    candidate_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200) 
    gender = models.CharField(max_length=10, choices = Gender.gender_choice, default=Gender.PREFER_NOT_TO_SAY)
    mobile_number = models.CharField(max_length=15)
    candidate_image = models.ImageField(upload_to='candidate_images/')
    candidate_bio = models.CharField(max_length=200)
    candidate_about = models.CharField(max_length=1500)
    candidate_website = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    is_active = models.BooleanField(default = True)

    

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



    def save(self, *args, **kwargs):
            if not self.candidate_id:
                last_candidate = Candidate.objects.order_by('-id').first()

                if last_candidate:
                    last_id = int(last_candidate.candidate_id.replace('CAN', ''))
                    new_id = last_id + 1
                else:
                    new_id = 1001

                self.candidate_id = f"CAN{new_id}"

            super().save(*args, **kwargs)

    
    
class Education(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educations')
    institute_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    start_date = models.CharField(max_length=5)
    end_date = models.CharField(max_length=5)
    course = models.CharField(max_length=50)
    class Grades(models.grade_choice):
        CGPA = 'CGPA'
        PERCENTAGE = 'Percentage'
    grade = models.CharField(max_length=5, choices=Grades.grade_choice)
    