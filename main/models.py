from django.contrib.auth.models import AbstractUser
from django.db import models


class DepartmentModel(models.Model):
    name = models.CharField(max_length=80, db_index=True)
    slug = models.SlugField(max_length=80, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Подразделение предприятия"
        verbose_name_plural = "Подразделения предприятия"


class PositionModel(models.Model):
    name = models.CharField(max_length=80, db_index=True)
    slug = models.SlugField(max_length=80, db_index=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("name",)
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class EmployeeModel(models.Model):
    department = models.ForeignKey(
        DepartmentModel,
        related_name="employeed",
        on_delete=models.PROTECT,
        verbose_name="Отдел",
    )
    position = models.ForeignKey(
        PositionModel,
        related_name="employeep",
        on_delete=models.PROTECT,
        verbose_name="Должность",
    )
    name = models.CharField(
        max_length=80, db_index=True, verbose_name="Имя Отчество сотрудника"
    )
    surname = models.CharField(
        max_length=50, db_index=True, verbose_name="Фамилия сотрудника"
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_index=True,
        unique=True,
        verbose_name="Номер телефона",
    )
    email = models.CharField(
        max_length=30, db_index=True, null=True, verbose_name="Email"
    )
    hiring_date = models.DateField(
        blank=True, null=True, db_index=True, verbose_name="Дата трудоустройства"
    )
    termination_date = models.DateField(
        blank=True, null=True, db_index=True, verbose_name="Дата увольнения"
    )
    experience = models.PositiveIntegerField(
        blank=True, null=True, db_index=True, verbose_name="Стаж работы"
    )
    birthday = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Дата рождения"
    )
    description = models.TextField(blank=True, null=True, verbose_name="О сотруднике")

    def __str__(self):
        return f"{self.surname}"

    class Meta:
        ordering = ("surname",)
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class DataModelUser(models.Model):
    login = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=150)


class ExtendUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name="Прошел активацию?"
    )

    class Meta(AbstractUser.Meta):
        pass
