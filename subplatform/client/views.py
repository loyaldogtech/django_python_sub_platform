from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from software_engineer.models import Article
from . models import Subscription

@login_required(login_url='my_login')
def client_dashboard(request):

    try:

        subDetails = Subscription.objects.get(user=request.user.id)

        subscription_plan = subDetails.subscription_plan

        context = {'SubPlan':subscription_plan}

        return render(request, 'client/client-dashboard.html', context)

    except:

        subscription_plan = 'None'
        context = {'SubPlan':subscription_plan}

        return render(request, 'client/client-dashboard.html', context)


@login_required(login_url='my_login')
def browse_articles(request):

    try:

        subDetails = Subscription.objects.get(user=request.user.id, is_active=True)

    except:

        return render(request, 'client/subscription-locked.html')
    
    current_subscription_plan = subDetails.subscription_plan
    
    if current_subscription_plan == 'Standard':

        articles = Article.objects.all().filter(is_premium=False)
    
    elif current_subscription_plan == 'Premium':

        articles = Article.objects.all()
    
    context = {'AllClientArticles': articles}
    return render(request, 'client/browse-articles.html', context)

@login_required(login_url='my_login')
def subscription_locked(request):

    return render(request, 'client/subscription-locked.html')

@login_required(login_url='my_login')
def subscription_plans(request):

    return render(request, 'client/subscription-plans.html')

@login_required(login_url='my_login')
def account_management(request):

    return render(request, 'client/account-management.html')

       

