from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Item

# Create your views here.
@login_required
def profile(request):
    """Renders the profile page"""
    context = {}
    return render(request, 'profiles/profile.html', context)


@login_required
def wishlist(request):
    """Renders the profile page"""
    user = request.user
    wishlist = Item.objects.filter(user=user)

    context = {
        'wishlist': wishlist,
    }
    return render(request, 'profiles/wishlist.html', context)
