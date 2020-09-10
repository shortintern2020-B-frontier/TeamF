from django.core.management import call_command
from django.db import migrations

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'posts/fixture/user.json', app_label='posts')
    call_command('loaddata', 'posts/fixture/book.json', app_label='posts')
    call_command('loaddata', 'posts/fixture/post.json', app_label='posts')
    call_command('loaddata', 'posts/fixture/psermission.json', app_label='posts')
    call_command('loaddata', 'posts/fixture/category.json', app_label='posts')
    call_command('loaddata', 'posts/fixture/tag.json', app_label='posts')
    call_command('loaddata', 'posts/fixture/imagechoice.json', app_label='app')

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
      migrations.RunPython(load_fixture),
    ]
    