import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from company.models import Department, Employee


class Command(BaseCommand):

    def handle(self, *args, **options):

        with transaction.atomic():
            departments = self.create_departments()
            self.create_employees(departments)

    def create_departments(self):
        Department.objects.all().delete()

        created = []

        root = Department(name='Компания', level=1)
        created.append(root)

        level_2 = [
            Department(name='Разработка', parent=root, level=2),
            Department(name='Продажи', parent=root, level=2),
            Department(name='Администрация', parent=root, level=2),
        ]
        created.extend(level_2)

        level_3 = [
            Department(name='Backend', parent=level_2[0], level=3),
            Department(name='Frontend', parent=level_2[0], level=3),
            Department(name='QA', parent=level_2[0], level=3),

            Department(name='B2B', parent=level_2[1], level=3),
            Department(name='B2C', parent=level_2[1], level=3),

            Department(name='HR', parent=level_2[2], level=3),
        ]
        created.extend(level_3)

        level_4 = [
            Department(name='API', parent=level_3[0], level=4),
            Department(name='Integrations', parent=level_3[0], level=4),

            Department(name='Web', parent=level_3[1], level=4),
            Department(name='Mobile', parent=level_3[1], level=4),

            Department(name='Manual QA', parent=level_3[2], level=4),

            Department(name='Key Accounts', parent=level_3[3], level=4),

            Department(name='Recruitment', parent=level_3[5], level=4),
            Department(name='Payroll', parent=level_3[5], level=4),
        ]
        created.extend(level_4)

        level_5 = [
            Department(name='Payments', parent=level_4[0], level=5),
            Department(name='Users', parent=level_4[0], level=5),

            Department(name='iOS', parent=level_4[3], level=5),
            Department(name='Android', parent=level_4[3], level=5),

            Department(name='Automation QA', parent=level_4[4], level=5),

            Department(name='Hiring IT', parent=level_4[6], level=5),
            Department(name='Hiring Sales', parent=level_4[6], level=5),
        ]
        created.extend(level_5)

        Department.objects.bulk_create(created)

        return level_5

    def create_employees(self, departments):
        Employee.objects.all().delete()

        employees = []
        today = date.today()

        for i in range(50_000):
            employees.append(
                Employee(
                    surname=f'Surname{i}',
                    first_name=f'Name{i}',
                    middle_name=f'Middle{i}',
                    position=random.choice(
                        ['Developer', 'Manager', 'QA', 'HR', 'Analyst']
                    ),
                    hiring_date=today - timedelta(days=random.randint(0, 3650)),
                    salary=random.randint(50_000, 300_000),
                    department=random.choice(departments),
                )
            )

            # батчами по 5k — чтобы не раздувать память
            if len(employees) == 5_000:
                Employee.objects.bulk_create(employees)
                employees.clear()

        if employees:
            Employee.objects.bulk_create(employees)
