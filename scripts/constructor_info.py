from src.utility.wikipedia_data import wikipedia_data


def constructor(constructors, db):
    collection = db['constructors']
    constructors_id = constructors['constructorId']
    constructors_url = constructors['url']
    constructors_name = constructors['name']
    constructors_nationality = constructors['nationality']

    # Wikipedia API Constructor
    wikipedia_constructor = wikipedia_data(url_wikipedia=constructors_url)

    collection.insert_one({
        "ID": constructors_id,
        "Name": constructors_name,
        "Nationality": constructors_nationality,
        wikipedia_constructor['type']: wikipedia_constructor,
    })