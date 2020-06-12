import uuid
from django.db import models
from django.core.validators import RegexValidator


class MappedSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    account = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class SyncBag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class SyncItem(models.Model):
    GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    syncBag = models.ForeignKey(SyncBag, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)


class HistoryData(models.Model):
    class Status(models.IntegerChoices):
        DISCARDED = -1
        CURRENT = 0
        READONLY = 1

    id_dataString6 = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    status = models.IntegerField(choices=Status.choices, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    dataString0 = models.URLField(blank=True, null=True)
    dataString1 = models.DateTimeField(blank=True, null=True)
    dataString2 = models.TextField(blank=True, null=True)
    dataString3 = models.CharField(max_length=255, validators=
    [RegexValidator('[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[A-Za-z][ ]*[A-Za-z]')], blank=True, null=True)
    dataString4 = models.CharField(blank=True, max_length=40, null=True)
    dataString5 = models.IntegerField(blank=True, null=True)
    syncItem = models.ForeignKey(SyncItem, on_delete=models.CASCADE)


class CurrentData(models.Model):
    class Status(models.IntegerChoices):
        DISCARDED = -1
        CURRENT = 0
        READONLY = 1

    id_dataString6 = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    status = models.IntegerField(choices=Status.choices)
    created = models.DateTimeField()
    dataString0 = models.URLField()
    dataString1 = models.DateTimeField()
    dataString2 = models.TextField(blank=True)
    dataString3 = models.CharField(max_length=255, validators=
    [RegexValidator('[0-9][ ]*[0-9][ ]*[0-9][ ]*[0-9][ ]*[A-Za-z][ ]*[A-Za-z]')], )
    dataString4 = models.CharField(blank=True, max_length=40)
    dataString5 = models.IntegerField(blank=True)
    syncItem = models.OneToOneField(SyncItem, on_delete=models.CASCADE, verbose_name="current data")

