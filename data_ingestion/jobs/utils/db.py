import dataset

def conn():
    db = dataset.connect()
    return db

def store_company(db, name, cont, lien, scrapper, data):
    df = db['entreprises']
    df.insert(dict(nom=name, contact=cont, url=lien, type_scrapper=scrapper, metadata=data))

def store_job(db, entreprise, title, location):
    df = db['jobs']
    df.insert(dict(nom_entreprise=entreprise, titre=title, localisation=location))

def get_jobs_by_company(db, entreprise):
    df = db['jobs']
    return list(df.find(nom_entreprise=entreprise))
