from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        (
            "store",
            "0013_alter_favouriteproduct_device_id_and_more",
        ),  # замени на свою последнюю миграцию
    ]

    operations = [
        migrations.AddField(
            model_name="mysearch",
            name="user",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name="my_searches",
            ),
        ),
    ]
