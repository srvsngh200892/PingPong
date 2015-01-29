from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    role = models.CharField(max_length=20, null=True, blank=True)
    

    def __str__(self): 
        return self.role

class GameDetail(models.Model):
    user = models.ForeignKey(UserProfile)
    status = models.CharField(max_length=20, null=True, blank=True)
    result = models.PositiveSmallIntegerField(default=0, blank=True, null=True)   
    game_id = models.CharField(max_length=20, null=True, blank=True)
    game_round = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    game_role = models.CharField(max_length=20, null=True, blank=True)
    game_result = models.CharField(max_length=20, null=True, blank=True)
    dvalue = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    def __str__(self): 
    	return self.game_id   
			
