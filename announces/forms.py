from django import forms
from .models import Announce
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AnnounceForm(forms.ModelForm):
    title = forms.CharField(label="Введите заголовок объявления")
    content = forms.CharField(widget=CKEditorUploadingWidget(), label="Содержимое объявления")
    category = forms.ChoiceField(choices=Announce.categories, label="Выберите категорию")

    class Meta:
        model = Announce
        fields = ['title', 'content', 'category']

