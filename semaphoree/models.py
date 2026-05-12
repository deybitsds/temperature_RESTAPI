from django.db import models


class SemaphoreState(models.Model):
    red = models.BooleanField(default=False)
    yellow = models.BooleanField(default=False)
    green = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'semaphore_state'

    def __str__(self):
        active = []
        if self.red: active.append('red')
        if self.yellow: active.append('yellow')
        if self.green: active.append('green')
        return ','.join(active) if active else 'off'
