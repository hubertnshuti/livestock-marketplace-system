import os
import django

# Setup Django access
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livestock_backend.settings')
django.setup()

from livestock.models import LivestockSpecies
from django.contrib.auth.models import User

def run_seed():
    # 1. Add Livestock Species (Fixes your dropdown)
    species_list = ['Cow', 'Goat', 'Sheep', 'Chicken', 'Pig', 'Rabbit', 'Duck', 'Turkey']
    for name in species_list:
        obj, created = LivestockSpecies.objects.get_or_create(species_name=name)
        if created:
            print(f"Added species: {name}")

    # 2. Create a Superuser (So you can login to /admin)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'nshutihubert4@gmail.com', 'admin123')
        print("Superuser created! Username: admin, Password: admin123")
    else:
        print("Superuser 'admin' already exists.")

if __name__ == '__main__':
    run_seed()