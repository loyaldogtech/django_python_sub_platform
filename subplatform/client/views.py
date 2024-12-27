from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from software_engineer.models import Article
from . models import Subscription
from account.models import CustomUser
from . paypal import *

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

    try:

        subDetails = Subscription.objects.get(user=request.user.id)
        subscription_id = subDetails.paypal_subscription_id
        context = {'SubscriptionID': subscription_id}

        return render(request, 'client/account-management.html', context)

    except:

        return render(request, 'client/account-management.html')












@login_required(login_url='my_login')
def create_subscription(request, subID, plan):

    custom_user = CustomUser.objects.get(email=request.user)
    firstName = custom_user.first_name
    lastName = custom_user.last_name
    fullName = firstName + ' ' + lastName
    selected_sub_plan = plan

    if selected_sub_plan == 'Standard':
        amount = "4.99"
    elif selected_sub_plan == 'Premium':
        amount = "9.99"

    subscription = Subscription.objects.create(subscriber_name=fullName, subscription_plan=selected_sub_plan, subscription_cost=amount, user=request.user, paypal_subscription_id=subID, is_active=True)

    context = {'SubscriptionPlan': selected_sub_plan}
    return render(request, 'client/create-subscription.html', context)

@login_required(login_url='my_login')
def delete_subscription(request, subID):

    # Delete subscription from PayPal
    access_token = get_access_token()
    cancel_subscription_paypal(access_token, subID)

    # Delete subscription from Django (application side)
    subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subID)
    subscription.delete()

    return render(request, 'client/delete-subscription.html')






    

       

