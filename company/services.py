from django.db.models import Prefetch
from company.models import Department, Employee


def build_company_tree_with_top10_employees():
    employees_qs = Employee.objects.all()

    employees_prefetch = Prefetch(
        'employee_set',
        queryset=employees_qs.order_by('surname')[:10],
        to_attr='top10_employees'
    )
    departments = Department.objects.all().select_related('parent').prefetch_related(employees_prefetch)

    children_map = {}
    root_nodes = []
    for dept in departments:
        children_map.setdefault(dept.parent_id, []).append(dept)
        if dept.parent is None:
            root_nodes.append(dept)

    def build_node(dept, parent_node_id=None):
        node_id = f'{parent_node_id}-{dept.id}' if parent_node_id else str(dept.id)

        node = {'id': dept.id, 'node_id': node_id, 'name': dept.name}

        if dept.level == 5:
            node['employees'] = [
                {
                    'surname': emp.surname,
                    'first_name': emp.first_name,
                    'middle_name': emp.middle_name,
                    'position': emp.position,
                    'salary': float(emp.salary),
                }
                for emp in getattr(dept, 'top10_employees', [])
            ]

        children = children_map.get(dept.id, [])
        for child in children:
            child_node = build_node(child, node_id)
            node[child_node['node_id']] = child_node

        return node

    return {node['node_id']: node for node in (build_node(dept) for dept in root_nodes)}
