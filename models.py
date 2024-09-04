from tkinter.constants import CASCADE

from django.db import models



# Create your models here.
class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date',)