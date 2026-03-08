from django.shortcuts import render

# Dictionary of pet types
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

def home_page(request):
    # Pass the dictionary to the template
    return render(request, "pet_adoption/home_page.html", {"pet_types": PET_TYPES})

def pet_type_details(request, pet_type):

    # context with the pet_type from the URL
    context = {
        "pet_type": pet_type,
    }

    # get the data for this pet type, or None if not found
    pet_data = PET_TYPES.get(pet_type, None)

    # add the data to the context
    context["pet_data"] = pet_data

    return render(request, "pet_adoption/pet_details.html", context)

def pets_for_lifestyle(request, lifestyle_fit):

    # Filter pets by lifestyle
    matching_pets = {
        key: pet
        for key, pet in PET_TYPES.items()
        if pet["lifestyle_fit"] == lifestyle_fit
    }

    context = {
        "lifestyle_fit": lifestyle_fit,
        "matching_pets": matching_pets,
    }

    return render(request, "pet_adoption/pets_for_lifestyle.html", context)