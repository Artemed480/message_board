from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Announce(models.Model):
    categories =[
        ('tanks', 'Танки'),
        ('hills', 'Хилы'),
        ('dd', 'ДД'),
        ('torg', 'Торговцы'),
        ('gild', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('cousn', 'Кузнецы'),
        ('scin', 'Кожевники'),
        ('pot', 'Зельевары'),
        ('magic', 'Мастера заклинаний'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=12, choices=categories, default='tanks')
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    content = RichTextUploadingField(null=True, config_name="default",)

    def __str__(self):
        return self.title
    
    def get_reply(self):
        replies = Reply.objects.filter(announce_id=self.id)
        return replies

    def get_accept_reply(self):
        replies = Reply.objects.filter(announce_id=self.id).filter(accept=True)
        return replies

    def get_category(self):
        return self.get_category_display()



class Reply(models.Model):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:50]

    def grant(self):
        self.accept = True
        self.save()

    def reject(self):
        self.delete()
