from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Code Citation: https://www.youtube.com/watch?v=eCeRC7E8Z7Y


class AccountManager(BaseUserManager):
    def create_user(self, email, username, display_name, age, password=None):
        if not email:
            raise ValueError("Users must provide an email address!")
        if not username:
            raise ValueError("Users must provide a username!")
        if not display_name:
            raise ValueError("Users must provide a display name!")
        if not age:
            raise ValueError("Users must provide their age!")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name,
            age=age,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, display_name, age, password):
        if not email:
            raise ValueError("Superusers must provide an email address!")
        if not username:
            raise ValueError("Superusers must provide a username!")
        if not display_name:
            raise ValueError("Superusers must provide a display name!")
        if not age:
            raise ValueError("Superusers must provide their age!")

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name,
            age=age,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=25, unique=True)
    display_name = models.CharField(max_length=25, unique=True)
    homepage = models.URLField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(
        verbose_name='date-joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last-login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'display_name', 'age']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class BugTicket(models.Model):
    NEW = 'NEW'
    IN_PROGRESS = 'INP'
    DONE = 'DNE'
    INVALID = 'INV'

    TICKET_STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid'),
    ]
    title = models.CharField(max_length=50)
    date_filed = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    ticket_status = models.CharField(
        max_length=3,
        choices=TICKET_STATUS_CHOICES,
        default=NEW,
    )
    assigned_to = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        default=None
    )
    completed_by = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        default=None
    )
