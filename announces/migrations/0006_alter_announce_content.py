# Generated by Django 4.2.2 on 2023-06-27 01:06

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announces', '0005_alter_announce_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]