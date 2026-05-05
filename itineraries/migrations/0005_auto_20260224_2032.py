from django.db import migrations


def rename_culture_to_vibes(apps, schema_editor):
    Category = apps.get_model("itineraries", "Category")
    Category.objects.filter(name="Culture").update(name="Vibes")


class Migration(migrations.Migration):

    dependencies = [
        ("itineraries", "0004_trip"),
    ]

    operations = [
        migrations.RunPython(rename_culture_to_vibes),
    ]
