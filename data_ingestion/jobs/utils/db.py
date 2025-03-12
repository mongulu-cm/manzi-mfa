import dataset

def conn():
    db = dataset.connect()
    return db

def store_company(db, name, cont, lien, scrapper, data):
    df = db['entreprises']
    df.insert(dict(nom=name, contact=cont, url=lien, type_scrapper=scrapper, metadata=data))

def store_job(db, entreprise, title, location):
    df = db['jobs']
    df.insert(dict(nom_enteprise=entreprise, titre=title, localisation=location))

def read_data(db, table):
    return db[table].all()


