from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='my_login')
def software_engineer_dashboard(request):

    return render(request, 'software_engineer/software_engineer-dashboard.html')