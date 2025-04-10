from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Item, Exchange, Review
from .forms import ItemForm, MessageForm, ReviewForm


def home(request):
    return render(request, 'listings/home.html')


def item_list(request):
    items = Item.objects.all()
    return render(request, 'listings/item_list.html', {'items': items})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'listings/add_item.html', {'form': form})


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'listings/edit_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'listings/delete_item.html', {'item': item})


@login_required
def create_exchange(request, sender_item_id, receiver_item_id):
    sender_item = get_object_or_404(Item, id=sender_item_id)
    receiver_item = get_object_or_404(Item, id=receiver_item_id)

    exchange = Exchange.objects.create(
        sender=request.user,
        receiver=receiver_item.user,
        sender_item=sender_item,
        receiver_item=receiver_item
    )
    exchange.save()
    return redirect('item_list')


@login_required
def accept_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    exchange.status = 'accepted'
    exchange.save()
    return redirect('item_list')


@login_required
def reject_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    exchange.status = 'rejected'
    exchange.save()
    return redirect('item_list')


@login_required
def send_message(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = exchange.receiver if request.user == exchange.sender else exchange.sender
            message.exchange = exchange
            message.save()
            return redirect('view_exchange', exchange_id=exchange.id)
    else:
        form = MessageForm()
    return render(request, 'listings/send_message.html', {'form': form, 'exchange': exchange})


@login_required
def view_exchange(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    messages = exchange.messages.all().order_by('timestamp')
    return render(request, 'listings/view_exchange.html', {'exchange': exchange, 'messages': messages})


@login_required
def leave_review(request, exchange_id):
    exchange = get_object_or_404(Exchange, id=exchange_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = exchange.receiver if request.user == exchange.sender else exchange.sender
            review.exchange = exchange
            review.save()
            return redirect('view_exchange', exchange_id=exchange.id)
    else:
        form = ReviewForm()
    return render(request, 'listings/leave_review.html', {'form': form, 'exchange': exchange})


@login_required
def view_reviews(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(reviewed_user=profile_user).order_by('-created_at')
    return render(request, 'listings/view_reviews.html', {'user': profile_user, 'reviews': reviews})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'listings/register.html', {'form': form})


def help_contact(request):
    return render(request, 'listings/help_contact.html')


def category_items(request, category_name):
    items = Item.objects.filter(category__iexact=category_name)
    return render(request, 'listings/category_items.html', {'items': items, 'category_name': category_name})
