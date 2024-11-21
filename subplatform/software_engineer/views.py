from django.shortcuts import render

def software_engineer_dashboard(request):

    return render(request, 'software_engineer/software_engineer-dashboard.html')