from django.urls import path
from .views import *


app_name = 'announces'

urlpatterns = [
    path('', list, name='announces'),
    path('<int:pk>', AnnounceDetail.as_view(), name='announce_detail'),
    path('reply/<int:pk>', reply_to_announce, name='reply_to_announce'),
    path('add', AnnounceCreate.as_view(), name='announce_create'),
    path('account', PersonalPageView.as_view(), name='personal_page'),
    path('edit/<int:pk>', AnnounceEdit.as_view(), name='announce_edit'),
    path('delete/<int:pk>', AnnounceDelete.as_view(), name='announce_delete'),
    path('replydelete/<int:pk>', ReplyDeleteView.as_view(), name='reply_delete'),
    path('replyaccept/<int:pk>', reply_accept, name='reply_accept'),
    path('account/replies', PersonalRepliesView.as_view(), name='personal_replies'),
    path('get_announces', list_announces, name='get_announces'),
]