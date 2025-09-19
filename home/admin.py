from django.contrib import admin
from .models import AttaCarousel, Category, Product, Cart, Wishlist, Booking, UserProfile

# Register your models here.
admin.site.register(AttaCarousel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Booking)
admin.site.register(UserProfile)
