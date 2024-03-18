import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Don_du_Sang.settings')

import django
django.setup()

from faker import Faker
from dons_des_sangs.models import Donateur,Wilaya,Type_Sang

fake = Faker()
def generate_tel():
    # Générer un numéro de téléphone commençant par 2, 3 ou 4
    prefix = fake.random_element(elements=('2', '3', '4'))
    # Générer le reste du numéro de téléphone
    suffix = fake.numerify(text='#######')  # 7 chiffres au hasard
    return f"{prefix}{suffix}"

fakes = Faker('ar')
 # Utilisation de la localisation jordanienne pour les prénoms et noms arabes

def generate_arabic_name():
    # Générer un prénom et un nom de famille arabes
    first_name = fakes.first_name()
    last_name = fakes.last_name()
    return first_name, last_name

def create_donateur():
    tel = generate_tel()
    email = fake.email()
    first_name, last_name = generate_arabic_name()
    # first_name = fake.first_name()
    # last_name = fake.last_name()
    date_naissance = fake.date_of_birth(minimum_age=18, maximum_age=65)
    # Récupérez une wilaya aléatoire existante dans la base de données
    wilaya = Wilaya.objects.order_by('?').first()
    # Récupérez un type de sang aléatoire existant dans la base de données
    type_sang = Type_Sang.objects.order_by('?').first()
    # Créez un mot de passe pour le donateur (par exemple, '1234')
    password = '1234'
    donateur = Donateur.objects.create(
        tel=tel,
        email=email,
        first_name=first_name,
        last_name=last_name,
        date_naissance=date_naissance,
        wilaya=wilaya,
        type_sang=type_sang,
    )
    donateur.set_password(password)
    donateur.save()
    print(f"Donateur créé: {donateur}")

def run():
    for _ in range(15):
        create_donateur()

if __name__ == '__main__':
    print("Insertion des donateurs dans la base de données...")
    run()
    print("Insertion terminée.")
