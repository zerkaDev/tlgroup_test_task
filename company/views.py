from django.shortcuts import render
from company.services import build_company_tree_with_top10_employees


def index(request):
    company_tree = build_company_tree_with_top10_employees()
    return render(request, 'index.html', {
        'company_tree': company_tree,
    })
