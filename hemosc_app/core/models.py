from django.db import models

# Create your models here.
from djongo.models.fields import ModelField, Model

from questionarie.models import Questionnaire, Questions, Options


class Address:
    street = models.CharField(max_length=255)
    number_address = models.CharField(max_length=20)
    neighborhood = models.CharField(max_length=100)
    complement = models.CharField(
        max_length=255, blank=True
    )  # Optional address complement
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.number_address} - {self.city}, {self.state}"


from django.contrib.auth import get_user_model

User = get_user_model()  # Using get_user_model for flexibility


class DataUser(Model):
    user_id = models.CharField(
        max_length=255, unique=True
    )  # Assuming user_id is a unique identifier
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    profession = models.CharField(max_length=250)
    blood_type = models.CharField(max_length=10)
    last_donation = models.DateField(blank=True, null=True)  # Allows for null values
    address = ModelField(Address, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to User model

    def __str__(self):
        return str(self.user_id)


class ResponseAnswer(models.Model):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE
    )  # Link to ResponseQuestionnaire
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE
    )  # Link to the Question model
    answer_select = models.ForeignKey(
        Options, blank=True, null=True, on_delete=models.SET_NULL
    )  # Optional selected answer (ForeignKey to Answer)
    answer_text = models.TextField(
        blank=True
    )  # Optional answer text (for Short Answer questions)
    weight = models.PositiveIntegerField(blank=True, null=True)


class Donation(Model):
    user = models.ForeignKey(DataUser, on_delete=models.CASCADE)  # Links to User model
    donation_amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Monetary amount
    donation_date = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set on creation
    donation_status = models.CharField(
        max_length=50,
        choices=[  # Donation status options
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Refused", "Refused"),
        ],
        default="Pending",
    )
    refused_reason = models.TextField(blank=True)  # Optional reason for refusal
    response_questionarie = models.ForeignKey(
        ResponseAnswer, on_delete=models.SET_NULL, null=True, blank=True
    )  # Optional questionnaire reference
    answer_set = models.ManyToManyField(
        "Answer", through="DonationAnswer"
    )  # ManyToMany relation with answers (through model)

    class Meta:
        ordering = [
            "-donation_date"
        ]  # Order donations by newest first (default descending)

    def __str__(self):
        return f"Donation by {self.user.full_name} on {self.donation_date:%Y-%m-%d}"
