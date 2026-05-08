from django.db import models


class Temperature(models.Model):

    id = models.AutoField(
            db_column='id',
            primary_key=True
            )

    temperature = models.FloatField()
    humidity = models.FloatField()
    heat_index = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'temperature'

    def __str__(self):
        return f"{self.temperature}°C / {self.humidity}%"
