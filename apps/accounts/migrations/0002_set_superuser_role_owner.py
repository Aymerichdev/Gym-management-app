from django.db import migrations


def set_superusers_as_owner(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(is_superuser=True).update(role="owner")


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_superusers_as_owner, migrations.RunPython.noop),
    ]
