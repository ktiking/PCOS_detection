# stuff we need to make the database work
from django.db import models
from django.contrib.auth.models import User

# this is where we store all the predictions we make
class Prediction(models.Model):
    # who made this prediction
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # all the info we collect from the form
    age = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    cycle = models.CharField(max_length=1, choices=[('R', 'Regular'), ('I', 'Irregular')])
    cycle_length = models.FloatField()
    lh_fsh_ratio = models.FloatField()
    weight_gain = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
    hair_growth = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
    follicle_no_l = models.FloatField()
    follicle_no_r = models.FloatField()
    hip = models.FloatField()
    skin_darkening = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
    lifestyle_score = models.FloatField()
    
    # what our model predicted
    prediction = models.IntegerField(choices=[(0, 'Low Risk'), (1, 'High Risk')])
    probability = models.FloatField()
    
    # when they made this prediction
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # show newest predictions first
        ordering = ['-created_at']

    def __str__(self):
        # this is what shows up in the admin panel
        return f"Prediction for {self.user.username} - {self.created_at}"
