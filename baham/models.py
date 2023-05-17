from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from uuid import uuid4

from baham.constants import COLOURS, TOWNS
from baham.enum_types import VehicleType, VehicleStatus, UserType

class VehicleModel(models.Model):
    type = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleType],
                            help_text="Select the vehicle chassis type")
    capacity = models.PositiveSmallIntegerField(null=False, default=2)
    #Audit Fields
    date_created = models.DateTimeField(default=timezone.now, null=True, editable=False, related_name='vehiclemodel_creator')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    date_updated = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='vehiclemodel_updater')
    isVoided = models.BooleanField(default=False, null=True)
    date_voided = models.DateTimeField(null=True)
    voided_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='vehiclemodel_voided')
    void_reason = models.CharField(max_length=1024)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:
        db_table = "baham_vehicle_model"

    def __str__(self):
        return f"{self.vendor} {self.model}"

    def update(self, updated_by=None, *args, **kwargs):
        self.date_updated = timezone.now
        self.updated_by = updated_by
        if not updated_by:
            updated_by = User.objects.get(pk=1)
        self.updated_by = updated_by
        self.save()

    def delete(self, voided_by=None, *args, **kwargs):
        self.isVoided = True
        self.date_voided = timezone.now
        if not self.void_reason:
            self.void_reason = 'Voided without reason'
        if not voided_by:
            voided_by = User.objects.get(pk=1)
        self.voided_by = voided_by
        self.save()

    def undelete(self, *args, **kwargs):
        if self.isVoided:
            self.isVoided = False
            self.date_voided = None
            self.void_reason = None
            self.save()
    def purge(self, *args, **kwargs):
        self.delete()

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True, db_column='id')
    status = models.CharField(max_length=50, choices=[(t.name, t.value) for t in VehicleStatus])
    picture1 = models.ImageField(upload_to='pictures', null=True)
    picture2 = models.ImageField(upload_to='pictures', null=True)
    #Audit Fields
    date_created = models.DateTimeField(default=timezone.now, null=True, editable=False, related_name='vehicle_creator')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    date_updated = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='vehcile_updater')
    isVoided = models.BooleanField(default=False, null=True)
    date_voided = models.DateTimeField(null=True)
    voided_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='vehicle_voided')
    void_reason = models.CharField(null=True, max_length=1024)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.model.vendor} {self.model.model} {self.colour}"

    def update(self, updated_by = None, *args, **kwargs):
        self.date_updated = timezone.now
        self.updated_by = updated_by
        if not updated_by:
            updated_by = User.objects.get(pk=1)
        self.updated_by = updated_by
        self.save()

    def delete(self, voided_by = None, *args, **kwargs):
        self.isVoided = True
        self.date_voided = timezone.now
        if not self.void_reason:
            self.void_reason = 'Voided without reason'
        if not voided_by:
            voided_by = User.objects.get(pk=1)
        self.voided_by = voided_by
        self.save()

    def undelete(self, *args, **kwargs):
        if self.isVoided:
            self.isVoided = False
            self.date_voided = None
            self.void_reason = None
            self.save()
    def purge(self, *args, **kwargs):
        self.delete()

    # Should have one-to-one relationship with a Django user
class UserProfile(models.Model):
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    landmark = models.CharField(max_length=255, null=False)
    town = models.CharField(max_length=50, null=False, choices=[(c, c) for c in TOWNS])
    active = models.BooleanField(default=True, editable=False)
    date_deactivated = models.DateTimeField(editable=False, null=True)
    bio = models.TextField()
    #Audit Fields
    date_created = models.DateTimeField(default=timezone.now, null=True, editable=False, related_name='userprofile_creator')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    date_updated = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='userprofile_updater')
    isVoided = models.BooleanField(default=False, null=True)
    date_voided = models.DateTimeField(null=True)
    voided_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='userprofile_voided')
    void_reason = models.CharField(null=True, max_length=1024)
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def update(self, updated_by = None, *args, **kwargs):
        self.date_updated = timezone.now
        self.updated_by = updated_by
        if not updated_by:
            updated_by = User.objects.get(pk=1)
        self.updated_by = updated_by
        self.save()

    def delete(self, voided_by = None, *args, **kwargs):
        self.isVoided = True
        self.date_voided = timezone.now
        if not self.void_reason:
            self.void_reason = 'Voided without reason'
        if not voided_by:
            voided_by = User.objects.get(pk=1)
        self.voided_by = voided_by
        self.save()

    def undelete(self, *args, **kwargs):
        if self.isVoided:
            self.isVoided = False
            self.date_voided = None
            self.void_reason = None
            self.save()
    def purge(self, *args, **kwargs):
        self.delete()