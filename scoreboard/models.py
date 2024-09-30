from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class SMBExercise(models.Model):
    exName = models.CharField(max_length=255, default="SMB Exploitation Exercise (Win7 SP1)")
    exDate = models.DateTimeField(default=timezone.now)
    exPlayer = models.CharField(max_length=20, default="John_Doe")
    exCriteria1 = models.BooleanField(default=False)
    exCriteria2 = models.BooleanField(default=False)
    exCriteria3 = models.BooleanField(default=False)
    exCriteria4 = models.BooleanField(default=False)
    exCriteria5 = models.BooleanField(default=False)
    exCriteria6 = models.BooleanField(default=False)

    def __str__(self):
        return self.exName

    @property
    def exScore(self):
        criteria = [self.exCriteria1, self.exCriteria2, self.exCriteria3,
                    self.exCriteria4, self.exCriteria5, self.exCriteria6]
        return 10 * sum(criteria)
