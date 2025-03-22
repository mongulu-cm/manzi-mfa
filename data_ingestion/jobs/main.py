import typer
import json
from typing import Optional
from scrapers.scraper_factory import ScraperFactory, ScraperType
from utils.functions import get_site_list
from utils.selenium import get_driver_path, get_positions
from utils.db import conn,get_jobs_by_company, store_job, store_company
from tabulate import tabulate

app = typer.Typer(
    help="CLI tool for scraping job positions. Use 'positions' to get coordinates or 'scrape' to extract jobs."
)

@app.command()
def positions(url: str = typer.Option(..., "--url", help="URL de la page à analyser")):
    """
    Obtenir les coordonnées d'un élément en cliquant dessus.
    """
    get_positions(url, get_driver_path())

@app.command()
def scrape(
    csv_file: Optional[str] = typer.Option(None, "--csv", help="Fichier CSV contenant les URLs et configurations"),
    url: Optional[str] = typer.Option(None, "--url", help="URL à scraper"),
    scraper_type: Optional[ScraperType] = typer.Option(None, "--type", help="Type de scraper (SCROLL/PAGINATION)"),
    company: Optional[str] = typer.Option(None, "--comp", help="Nom de l'entreprise"),
    x_pos: Optional[int] = typer.Option(None, "--x", help="Position X du bouton next (requis pour PAGINATION)"),
    y_pos: Optional[int] = typer.Option(None, "--y", help="Position Y du bouton next (requis pour PAGINATION)"),
    cookie_x: Optional[int] = typer.Option(None, "--cookiex", help="Position X du bouton cookie"),
    cookie_y: Optional[int] = typer.Option(None, "--cookiey", help="Position Y du bouton cookie")
):
    """
    Scraper les offres d'emploi.
    """
    if csv_file:
        urls_config = get_site_list(csv_file)
        for config in urls_config[1:]:
            parts = config.split(';')
            company = parts[0]
            url = parts[1]
            scraper_type = ScraperType(parts[2])
            cookie_x = int(parts[5])
            cookie_y = int(parts[6])
            if scraper_type == ScraperType.PAGINATION:
                x, y = int(parts[3]), int(parts[4])
                execute_scraper(url, scraper_type, company,x, y, cookie_x, cookie_y)
            else:
                execute_scraper(url, scraper_type, company, 0, 0, cookie_x, cookie_y)
    else:
        if not url or not scraper_type:
            typer.echo("Error: --url et --type sont requis si --csv n'est pas fourni")
            raise typer.Exit(1)

        if scraper_type == ScraperType.PAGINATION and (x_pos is None or y_pos is None):
            typer.echo("Error: --x et --y sont requis pour le type PAGINATION")
            raise typer.Exit(1)

        execute_scraper(url, scraper_type, company, x_pos, y_pos, cookie_x, cookie_y)

@app.command()
def store(
    url: Optional[str] = typer.Option(None, "--url", help="URL du site carrières"),
    name: Optional[str] = typer.Option(None, "--nom", help="Nom entreprise"),
    contact: Optional[str] = typer.Option(None, "--contact", help="Contact au sein du collectif"),
    scraper_type: Optional[str] = typer.Option(None, "--type", help="Type de scraper (SCROLL/PAGINATION)"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="JSON contenant x_pos, y_pos, cookie_x, cookie_y")
):
    """
    Ajouter une nouvelle entreprise dans la base.
    """
    if not url:
        typer.echo("Error: --url est requis pour l'enregistrment")
        raise typer.Exit(1)
    if not name:
        typer.echo("Error: --nom est requis pour l'enregistrment")
        raise typer.Exit(1)
    if not contact:
        typer.echo("Error: --contact est requis pour l'enregistrment")
        raise typer.Exit(1)
    if not scraper_type:
        typer.echo("Error: --type est requis pour l'enregistrment")
        raise typer.Exit(1)
    if not metadata:
        typer.echo("Error: --metadata est requis pour l'enregistrment")
        raise typer.Exit(1)
    else:
        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            typer.echo("Erreur : Le format du JSON est invalide.", err=True)
            raise typer.Exit(code=1)

    database = conn()
    for comp in database['entreprises']:
        t_name = str(name).lower().replace(" ", "")
        t_contact = str(contact).lower().replace(" ", "")
        if comp['nom'].lower().replace(" ", "") == t_name and comp['contact'].lower().replace(" ", "") == t_contact:
            typer.echo("Error: Entreprise deja presente dans la base")
            raise typer.Exit(1)
        else:
            store_company(database, name, contact, url, scraper_type, metadata)

def execute_scraper(
    url: str,
    scraper_type: ScraperType,
    company: Optional[str] = None,
    x: Optional[int] = None,
    y: Optional[int] = None,
    cookie_x: Optional[int] = None,
    cookie_y: Optional[int] = None
):
    """
    Exécute le scraper avec les paramètres donnés et synchronise les jobs dans la base.
    """
    scraper = ScraperFactory.create_scraper(
        scraper_type,
        url=url,
        driver_path=get_driver_path(),
        next_button_x=x,
        next_button_y=y,
        cookie_x=cookie_x,
        cookie_y=cookie_y
    )
    database = conn()
    new_jobs = scraper.scrape()

    # Synchronisation des jobs
    existing_jobs = get_jobs_by_company(database, company)
    existing_jobs_set = {f"{job['titre']}|{job['localisation']}" for job in existing_jobs}
    new_jobs_set = {f"{job['title']}|{job['location']}" for job in new_jobs}

    # Calcul des jobs à supprimer et à ajouter
    jobs_to_delete = existing_jobs_set - new_jobs_set
    jobs_to_add = new_jobs_set - existing_jobs_set

    # Suppression des jobs obsolètes
    for job in existing_jobs:
        job_key = f"{job['titre']}|{job['localisation']}"
        if job_key in jobs_to_delete:
            database['jobs'].delete(id=job['id'])

    # Ajout des nouveaux jobs
    for job in new_jobs:
        job_key = f"{job['title']}|{job['location']}"
        if job_key in jobs_to_add:
            print(f"Ajout du nouveau job: {job}")
            store_job(database, company, job['title'], job['location'])

    print(tabulate(new_jobs, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    app()