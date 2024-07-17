from django.db import models

# Create your models here.
from djongo.models.fields import ArrayField, Model


class Questions(Model):
    question_text = models.CharField(max_length=255)
    answer = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.question


class Options(Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    option_text = models.CharField(max_length=255)
    weigth = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.option_text


# Create your models here.
class Questionnaire(Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    version_number = models.PositiveIntegerField(
        default=1
    )  # Version number, starts at 1
    deactivate_at = models.DateTimeField(
        blank=True, null=True
    )  # Optional deactivation time
    questions = ArrayField(Quesitons)

    class Meta:
        ordering = ["-version_number"]  # Order by newest version first

    def __str__(self):
        return f"Questionnaire (v{self.version_number}) - {self.status}"
