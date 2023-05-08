import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class CommonInfo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='%(app_label)s_%(class)s_related',
        null=True,
    )

    class Meta:
        abstract = True


class Course(CommonInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    full_description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)


class CourseLinks(CommonInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access_code = models.CharField(max_length=255, unique=True, db_index=True)
    use_access_code = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    active = models.BooleanField(default=True)


class StudentsCourse(CommonInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name='students')
    join_link = models.ForeignKey(CourseLinks, on_delete=models.RESTRICT)
    student = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='courses_students_related',
        null=True,
    )


class Lecture(CommonInfo):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name='lectures')
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    full_description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
