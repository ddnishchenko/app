from collisionconf.models import Person

job_titles = [
    'Founder',
    'CO-Founder',
    'CTO',
    'CEO',
    'COO',
    'Product Manager',
    'Director of IT',
    'Product Owner',
    'Director of Technology',
    'Director of product',
    'Partner',
]

def filter_persons():
    persons = Person.objects.all()
    print('Persons count: ', persons.count())
    filtered = list()
    for person in persons:
        for jt in job_titles:
            if jt.lower() in person.job_title.lower():
                filtered.append(person)
                break
    print('Filered len: ', len(filtered))
    persons.delete()
    return filtered