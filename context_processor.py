from article.models import Article
from complaint.models import Complaint
from hub.models import Topic
from notification.models import Notification


# Добавляет в контекст меню категорий(хабов)
def topic_list(request):
    return {"topic_list": Topic.objects.all()}


def moderated_article_count(request):
    return {'moderated_articles_count': Article.get_moderated_articles().count(),
            'new_complaints_count': Complaint.get_active_complaints().count(),
            }


def notifications(request):
    if request.user.is_authenticated:

        request.user.is_not_blocked()
        """создаем отдельную структуру для определенных типов уведомлений, чтобы во фронте не заниматься сортировкой"""
        unread = {
            'moderator': [],
            'rm_article': [],
            'del_comment': [],
            'publish': [],
            'restore': [],
            'blocked': None,
        }
        for notice in Notification.get_unread(request.user.pk):
            if notice.type_of == Notification.MODERATOR:
                unread['moderator'].append(notice)
            elif notice.type_of == Notification.RM_ARTICLE:
                unread['rm_article'].append(notice)
            elif notice.type_of == Notification.DEL_COMMENT:
                unread['del_comment'].append(notice)
            elif notice.type_of == Notification.PUBLISH:
                unread['publish'].append(notice)
            elif notice.type_of == Notification.RESTORE:
                unread['restore'].append(notice)
            elif notice.type_of == Notification.BLOCK_USER:
                unread['blocked'] = notice
            elif notice.type_of == Notification.UNBLOCK_USER:
                unread['unblocked'] = notice

        # if request.user.is_blocked:
        #     unread['blocked'] = Notification.objects.filter(type_of=Notification.BLOCK_USER,
        #                                                     user=request.user.pk).order_by('-created_at').first()
        # print(unread['blocked'])
        return \
            {
                'notice':
                {
                    # 'all_notifications': Notification.get_all(request.user.pk),
                    'total_count': Notification.total_count(request.user.pk),
                    'unread': unread,
                    'unread_count': Notification.total_unread_count(request.user.pk),
                    'new_liked_articles': Notification.get_new_liked_articles(request.user.pk),
                    'new_disliked_articles': Notification.get_new_disliked_articles(request.user.pk),
                    'new_liked_comments': Notification.get_new_liked_comments(request.user.pk),
                    'new_disliked_comments': Notification.get_new_disliked_comments(request.user.pk),
                    'new_comments_articles': Notification.get_new_comments_articles(request.user.pk),
                    'new_comments_reply': Notification.get_new_comments_reply(request.user.pk),
                }
            }
    else:
        return {'notice': 0}
