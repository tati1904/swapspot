from django.contrib import admin
from .models import Item, Exchange, Review  # Import models that definitely work

# Register models separately to avoid circular import issues
admin.site.register(Item)
admin.site.register(Exchange)
admin.site.register(Review)

# ✅ Now try importing Message separately
try:
    from .models import Message
    admin.site.register(Message)
except ImportError:
    print("Error importing Message model")
