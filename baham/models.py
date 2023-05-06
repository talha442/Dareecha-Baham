from django.db import models
from django.utils import timezone



class Vehicle(models.Model):

    VEHICLE_TYPE_CHOICES = [
        ('motorcycle', 'Motorcycle'),
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('van', 'Van'),
    ]

    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    sitting_capacity = models.IntegerField()
    color = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, default='inactive')
    front_picture = models.ImageField(upload_to='vehicle_pictures/', blank=True)
    side_picture = models.ImageField(upload_to='vehicle_pictures/', blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    updation_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='created_vehicles')
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='updated_vehicles')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    def delete(self, *args, **kwargs):
        if not self.user.is_staff:
            raise PermissionDenied("Only staff members have permission to delete")
        super().delete(*args, **kwargs)


# User Model
class User(models.Model):
    # Affiliated as choices
    AFFILIATED_AS_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    contact_numbers = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    gps_coordinates = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    affiliated_as = models.CharField(max_length=10, choices=AFFILIATED_AS_CHOICES)
    creation_date = models.DateTimeField(default=timezone.now)
    updation_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_users')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        if not self.user.is_staff:
            raise PermissionDenied("Only staff members have permission to delete users.")
        super().delete(*args, **kwargs)

# Owner Model
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)
    num_contracts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Companion Model
class Companion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currently_in_contract = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Contract(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    companion = models.ForeignKey(Companion, on_delete=models.PROTECT)
    effective_start_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    fuel_share = models.PositiveIntegerField()
    maintenance_share = models.PositiveIntegerField()
    schedule = models.JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contracts_created')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contracts_updated')
    is_active = models.BooleanField(default=True)
    schedule = models.DateTimeField()
    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.companion.user.get_full_name()}"

    def save(self, *args, **kwargs):
        total_share = self.fuel_share + self.maintenance_share
        if total_share > 100:
            raise ValueError("Total share cannot exceed 100")
        if self.expiry_date - self.effective_start_date > timezone.timedelta(days=180):
            raise ValueError("Contract must not go on for more than 6 months")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user.is_staff:
            raise PermissionDenied("Only staff members have permission to delete contracts.")
        super().delete(*args, **kwargs)

