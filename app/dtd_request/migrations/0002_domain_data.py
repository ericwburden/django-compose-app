from django.db import migrations
import json

DEFAULT_DOMAIN_DATA = json.loads(
    """
    [
        {
            "value": 1,
            "label": "Shelter/Housing"
        },
        {
        "value": 2,
        "label": "Employment"
        },
        {
            "value": 3,
            "label": "Income"
        },
        {
            "value": 4,
            "label": "Food and Nutrition"
        },
        {
            "value": 5,
            "label": "Childcare"
        },
        {
            "value": 6,
            "label": "Children's Education"
        },
        {
        
            "value": 7,
            "label": "Adult Education"
        },
        {
            "value": 8,
            "label": "Life Skills"
        },
        {
            "value": 9,
            "label": "Life Skills"
        },
        {
            "value": 10,
            "label": "Family Relationships/Social Network"
        },
        {
            "value": 11,
            "label": "Transportation/Mobility"
        },
        {
            "value": 12,
            "label": "Community Involvement"
        },
        {
            "value": 13,
            "label": "Parenting Skills"
        },
        {
            "value": 14,
            "label": "Legal"
        },
        {
            "value": 15,
            "label": "Mental Health"
        },
        {
            "value": 16,
            "label": "Substance Abuse"
        },
        {
            "value": 17,
            "label": "Safety"
        },
        {
            "value": 18,
            "label": "Disability Services"
        },
        {
            "value": 19,
            "label": "Credit/Financial Management"
        },
        {
            "value": 20,
            "label": "Spirituality"
        }
    ]
    """
)

def import_domains(apps, schema_editor):
    Domain = apps.get_model('dtd_request', 'Domain')
    for domain in DEFAULT_DOMAIN_DATA:
        Domain(value=domain['value'], label=domain['label']).save()

class Migration(migrations.Migration):

    dependencies = [
        ('dtd_request', '0001_initial')
    ]

    operations = [
        migrations.RunPython(import_domains),
    ]
