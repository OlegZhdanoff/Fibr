from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from article.models import Article, Comment
from authapp.models import User
from complaint.models import Complaint
from notification.models import Notification


@login_required
@user_passes_test(lambda u: u.is_not_blocked(), login_url=reverse_lazy('auth:access_error'))
def create(request, pk):
    """Пользователь создает жалобу"""

    type_of = {
        '1': Complaint.USER,
        '2': Complaint.ARTICLE,
        '3': Complaint.COMMENT,
    }
    if request.method == 'POST':
        type_of = type_of[request.POST.get('type_of')]

        # проверка на существование объекта жалобы
        if type_of == Complaint.USER:
            target = get_object_or_404(User, id=pk)
        elif type_of == Complaint.ARTICLE:
            target = get_object_or_404(Article, id=pk)
        else:
            target = get_object_or_404(Comment, id=pk)

        complaint = Complaint.create(owner=request.user, target=target, type_of=type_of,
                                     text=request.POST.get('text'))

        Notification.add_notice(user=request.user, complaint=complaint, type_of=Notification.NEW_COMPLAINT)
        print(complaint, type_of)
    return redirect(request.META['HTTP_REFERER'])

