from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ModelA(models.Model):
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="model_a_statuses"
    )


class ModelB(models.Model):
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="model_b_statuses"
    )
