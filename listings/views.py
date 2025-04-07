from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Review
from .forms import ItemForm, ReviewForm
from .models import Item, Exchange
from django.contrib.auth.decorators import login_required
from .models import Exchange
from .forms import MessageForm
from .models import Exchange
from .models import Review, Exchange
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    return render(request, 'listings/home.html')

def item_list(request):
    items = Item.objects.all()
    return render(request, 'listings/item_list.html', {'items': items})

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
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'listings/delete_item.html', {'item': item})


@login_required
def create_exchange(request, sender_item_id, receiver_item_id):
    sender_item = Item.objects.get(id=sender_item_id)
    receiver_item = Item.objects.get(id=receiver_item_id)

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
    exchange = Exchange.objects.get(id=exchange_id)
    exchange.status = 'accepted'
    exchange.save()
    return redirect('item_list')

@login_required
def reject_exchange(request, exchange_id):
    exchange = Exchange.objects.get(id=exchange_id)
    exchange.status = 'rejected'
    exchange.save()
    return redirect('item_list')


@login_required
def send_message(request, exchange_id):
    exchange = Exchange.objects.get(id=exchange_id)
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
    exchange = Exchange.objects.get(id=exchange_id)
    messages = exchange.messages.all().order_by('timestamp')
    return render(request, 'listings/view_exchange.html', {'exchange': exchange, 'messages': messages})


@login_required
def leave_review(request, exchange_id):
    exchange = Exchange.objects.get(id=exchange_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = exchange.receiver if request.user == exchange.sender else exchange.sender
            review.exchange = exchange
            review.save()
            return redirect('view_exchange', exchange_id=exchange_id)
    else:
        form = ReviewForm()
    return render(request, 'listings/leave_review.html', {'form': form, 'exchange': exchange})

@login_required
def view_reviews(request, user_id):
    user = user.objects.get(id=user_id)
    reviews = Review.objects.filter(reviewed_user=user).order_by('-created_at')
    return render(request, 'listings/view_reviews.html', {'user': user, 'reviews': reviews})

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
            return redirect('view_exchange', exchange_id=exchange_id)
    else:
        form = ReviewForm()
    return render(request, 'listings/leave_review.html', {'form': form, 'exchange': exchange})

@login_required
def view_reviews(request, user_id):
    user = get_object_or_404(user, id=user_id)
    reviews = Review.objects.filter(reviewed_user=user).order_by('-created_at')
    return render(request, 'listings/view_reviews.html', {'user': user, 'reviews': reviews})
