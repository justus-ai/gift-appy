from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required

from django.views import View

from django.http import HttpResponseRedirect
from .models import Item, UserProfile
from .forms import WishForm, ProfileForm


# Create your views here.
@login_required
def friends(request):
    """Renders the friends list page"""
    me = get_object_or_404(UserProfile, user=request.user)
    follows = me.followed_by.all()
    context = {
        'me': me,
        'follows': follows,
    }

    return render(request, 'profiles/friends.html', context)


@login_required
def edit_profile(request):
    """Renders the edit profile page"""

    profile = UserProfile.objects.get(user=request.user)

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
        )
    if form.is_valid():
        form.save()
        return redirect('friends')

    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'profiles/edit_profile.html', context)


@login_required
def wishlist(request):
    """Renders the profile page"""
    user = request.user
    wishlist = Item.objects.filter(user=user)

    if request.method == 'POST':
        wish_form = WishForm(request.POST, request.FILES)
        if wish_form.is_valid():
            form = wish_form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(reverse('wishlist'))
        else:
            messages.error(request, 'Error adding the product. \
                Verify that all fields are filled in accurately.')
    else:
        wish_form = WishForm()

    template_name = 'profiles/wishlist.html'
    context = {
        'wishlist': wishlist,
        'wish_form': wish_form,
    }
    return render(request, template_name, context)


@login_required
def edit_wish(request, item_id):
    """ Render the Edit_wish template"""

    wish = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        wish_form = WishForm(request.POST, request.FILES, instance=wish)
        if wish_form.is_valid():
            wish_form.save()
            return redirect(reverse('wishlist'))
    else:
        wish_form = WishForm(instance=wish)

    template_name = 'profiles/edit_wish.html'
    context = {
        'wish_form': wish_form,
        'wish': wish,
    }
    return render(request, template_name, context)


class Follows(View):
    """This view follows and unfollow users"""
    def post(self, request, follow_id):
        that_user = get_object_or_404(UserProfile, pk=follow_id)
        # print("THIS IS:", that_user)
        # if user.follows.filter(id=request.user.id).exists():
        #     user.follows.remove(request.user)
        # else:
        #     user.follows.add(request.user)

        if that_user.followed_by.filter(user=request.user).exists():
            print("HEY THIS IS EXISTING", that_user.followed_by.filter(user=request.user).exists())
            that_user.followed_by.remove(self.request.user)
        else:
            that_user.follows.add(request.user)

        return HttpResponseRedirect(reverse('friends'))



@login_required
def delete_wish(request, item_id):
    """This function deletes a selected wish"""
    wish = get_object_or_404(Item, pk=item_id)
    wish.delete()
    return redirect('wishlist')
