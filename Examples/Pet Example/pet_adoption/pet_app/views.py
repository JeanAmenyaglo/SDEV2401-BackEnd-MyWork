from django.shortcuts import render

PET_TYPES = {
    'dog': {
        'name': 'Dog',
        'traits': 'Loyal, energetic, needs space and exercise.',
        'lifestyle_fit': 'active'
    },
    'cat': {
        'name': 'Cat',
        'traits': 'Independent, cuddly, low-maintenance.',
        'lifestyle_fit': 'quiet'
    },
    'rabbit': {
        'name': 'Rabbit',
        'traits': 'Gentle, small, requires calm environment.',
        'lifestyle_fit': 'quiet'
    },
    'parrot': {
        'name': 'Parrot',
        'traits': 'Social, intelligent, needs stimulation.',
        'lifestyle_fit': 'social'
    }
}

# Create your views here.
def home_page(request):
    return render(request, 'home_page.html', {'pet_types': PET_TYPES})

def pet_type_details(request, pet_type):
    context = {
        "pet_type": pet_type, #this is from the URL
    }
    pet_data = PET_TYPES.get(pet_type, None)
    context['pet_data'] = pet_data

    return render(request, 'pet_details.html', context)

def pets_for_lifestyle(request, lifestyle):
    lifestyle = lifestyle
    matching_pets = [pet for pet, details in PET_TYPES.items() if details['lifestyle_fit'] == lifestyle]
    context = {
        'lifestyle': lifestyle,
        'matching_pets': matching_pets
    }

    return render(request, 'lifestyle_pets.html', context)

def test_template(request):
    return render(request, 'test-template.html')