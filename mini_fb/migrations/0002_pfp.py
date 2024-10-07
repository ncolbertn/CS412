from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="Profile",
            name="pfp",
            field=models.URLField(blank=True),
        ),
    ]