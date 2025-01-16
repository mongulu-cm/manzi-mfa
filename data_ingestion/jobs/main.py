import typer
from typing import Optional
from scrapers.scraper_factory import ScraperFactory, ScraperType
from utils.functions import get_site_list
from utils.selenium import get_driver_path, get_positions
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
        for config in urls_config:
            parts = config.split(',')
            url = parts[0]
            scraper_type = ScraperType[parts[1]]
            if scraper_type == ScraperType.PAGINATION:
                x, y = int(parts[2]), int(parts[3])
                cookie_x_value, cookie_y_value = None, None
                if len(parts) >= 6:
                    cookie_x_value = int(parts[4])
                    cookie_y_value = int(parts[5])
                execute_scraper(url, scraper_type, x, y, cookie_x_value, cookie_y_value)
            else:
                execute_scraper(url, scraper_type, cookie_x=cookie_x, cookie_y=cookie_y)
    else:
        if not url or not scraper_type:
            typer.echo("Error: --url et --type sont requis si --csv n'est pas fourni")
            raise typer.Exit(1)

        if scraper_type == ScraperType.PAGINATION and (x_pos is None or y_pos is None):
            typer.echo("Error: --x et --y sont requis pour le type PAGINATION")
            raise typer.Exit(1)

        execute_scraper(url, scraper_type, x_pos, y_pos, cookie_x, cookie_y)

def execute_scraper(
    url: str,
    scraper_type: ScraperType,
    x: Optional[int] = None,
    y: Optional[int] = None,
    cookie_x: Optional[int] = None,
    cookie_y: Optional[int] = None
):
    """
    Exécute le scraper avec les paramètres donnés.
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
    jobs = scraper.scrape()
    print(tabulate(jobs, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    app()