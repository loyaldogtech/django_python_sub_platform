from django.shortcuts import render, redirect
from django.http import HttpResponse
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

        subDetails = Subscription.objects.get(user=request.user)
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

@login_required(login_url='my_login')
def update_subscription(request, subID):
    
    access_token = get_access_token()

    # approve_link = Hateoas link from PayPal
    approve_link = update_subscription_paypal(access_token, subID)

    if approve_link:

        return redirect(approve_link)

    else:

        return HttpResponse("Unable to obtain update link")

    
@login_required(login_url='my_login')
def paypal_update_sub_confirmed(request):

    try:

        subDetails = Subscription.objects.get(user=request.user)

        subscriptionID = subDetails.paypal_subscription_id

        context = {'SubscriptionID': subscriptionID}

        return render(request, 'client/paypal-update-sub-confirmed.html', context)
    
    except:

        return render(request, 'client/paypal-update-sub-confirmed.html')
    
@login_required(login_url='my_login')
def django_update_sub_confirmed(request, subID):

    access_token = get_access_token()
    current_plan_id = get_current_subscription(access_token, subID)

    if current_plan_id == "P-5UT79485E39960225M5YJQEA": # Standard

       new_plan_name = "Standard"
       new_cost = "4.99"

       Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name, subscription_cost=new_cost)

    elif current_plan_id == "P-9ST26449M6579211PM5YJRFI": # Premium

       new_plan_name = "Premium"
       new_cost = "9.99"

       Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name, subscription_cost=new_cost)

    return render(request, 'client/django-update-sub-confirmed.html')


    
    
    






    

       

