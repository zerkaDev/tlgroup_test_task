from django.db import models


class AutoDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DepartmentQuerySet(models.QuerySet):
    def bulk_create(self, objs, *args, **kwargs):
        for obj in objs:
            if obj.level is None:
                raise ValueError(
                    'bulk_create запрещён без явного указания level '
                    '(для каждого Department)'
                )
            if obj.level > 5:
                raise ValueError('level не может быть больше 5')

        return super().bulk_create(objs, *args, **kwargs)


class DepartmentManager(models.Manager):
    def get_queryset(self):
        return DepartmentQuerySet(self.model, using=self._db)


class Department(AutoDateMixin):
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=255)
    level = models.PositiveSmallIntegerField(null=True, blank=True)

    objects = DepartmentManager()

    class Meta:
        verbose_name = 'Структура'
        verbose_name_plural = 'Структуры'

        constraints = [
            models.CheckConstraint(condition=models.Q(level__lte=5), name='max_level_5')
        ]

    def save(self, *args, **kwargs):
        # Жертвуем на каждый сейв +1 запрос но гарантируем требование.
        parent = self.parent
        if not parent:
            self.level = 1
        else:
            self.level = parent.level + 1
        super().save(*args, **kwargs)


class Employee(AutoDateMixin):
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hiring_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
