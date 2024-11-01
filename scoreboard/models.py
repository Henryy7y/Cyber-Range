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

class ExInfo(models.Model):
    exName = models.CharField(max_length=255)
    exCriteriaDesc1 = models.CharField(max_length=255)
    exCriteriaDesc2 = models.CharField(max_length=255)
    exCriteriaDesc3 = models.CharField(max_length=255)
    exCriteriaDesc4 = models.CharField(max_length=255)
    exCriteriaDesc5 = models.CharField(max_length=255)
    exCriteriaDesc6 = models.CharField(max_length=255)
    exDifficulty = models.IntegerField()
    exType = models.CharField(max_length=255)

    def __str__(self):
        return self.exName
    
class ExLog(models.Model):
    exLogID = models.AutoField(primary_key=True)
    exPlayerName = models.CharField(max_length=20)
    exCriteria1 = models.BooleanField(default=False)
    exCriteria2 = models.BooleanField(default=False)
    exCriteria3 = models.BooleanField(default=False)
    exCriteria4 = models.BooleanField(default=False)
    exCriteria5 = models.BooleanField(default=False)
    exCriteria6 = models.BooleanField(default=False)
    exDateTime = models.DateTimeField(default=timezone.now)
    exComment = models.CharField(max_length=255, default="")
    exName = models.ForeignKey(ExInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.exPlayerName
    
    @property
    def exScore(self):
        criteria = [self.exCriteria1, self.exCriteria2, self.exCriteria3,
                    self.exCriteria4, self.exCriteria5, self.exCriteria6]
        return 10 * sum(criteria)

    