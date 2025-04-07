from django.db import models
from django.contrib.auth.models import User  

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=50, choices=[('new', 'New'), ('used', 'Used')])
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Exchange(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    sender_item = models.ForeignKey('listings.Item', related_name='sent_item', on_delete=models.CASCADE)
    receiver_item = models.ForeignKey('listings.Item', related_name='received_item', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} offers {self.sender_item.name} for {self.receiver_item.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    exchange = models.ForeignKey('Exchange', related_name='messages', on_delete=models.CASCADE)  # ✅ String reference
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(User, related_name='received_reviews', on_delete=models.CASCADE)
    exchange = models.ForeignKey('Exchange', on_delete=models.CASCADE, related_name='reviews')  # ✅ String reference
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings from 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} rated {self.reviewed_user.username} {self.rating}/5"
