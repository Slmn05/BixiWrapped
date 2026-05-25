import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Playwright
import pandas as pd

historique = {}
CSV_PATH = 'data/statistiques_trajets.csv'

# Charge les variables du fichier .env dans l'environnement système
load_dotenv()

# Récupère les valeurs
username = os.getenv('BIXI_USERNAME')
password = os.getenv('BIXI_PASSWORD')


if not username or not password:
    raise ValueError("Identifiants manquants : vérifie ton fichier .env")

print(f"Prêt à connecter l'utilisateur : {username}")


def connect(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://secure.bixi.com/sign-in?next=http%3A%2F%2Fsecure.bixi.com%2Fprofile")
    try:
        page.wait_for_selector("#onetrust-accept-btn-handler", timeout=5000)
        page.click("#onetrust-accept-btn-handler")
        print("Bannière de cookies acceptée.")
    except:
        print("Pas de bannière de cookies détectée.")
    page.fill('input[name="bssUsername"]', username)
    page.fill('input[name="bssPassword"]', password)
    page.click('span[data-testid="icon-button-text"]')
    page.wait_for_timeout(1000)
    return context, page


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    
    # On vérifie si le fichier existe pour éviter de se reconnecter
    if os.path.exists(CSV_PATH):
        df_existing = pd.read_csv(CSV_PATH)
        already_scraped = int(df_existing['nb'].sum())
        print(f"Trajets déjà enregistrés dans le CSV : {already_scraped}")
    else:
        already_scraped = 0
        print("Aucun fichier CSV existant, on part de zéro.")

    if os.path.exists("data/state.json"):
        context = browser.new_context(storage_state="data/state.json")
        page = context.new_page()
        page.goto("https://secure.bixi.com/profile")
    else:
        context, page = connect(browser)

    context.storage_state(path="data/state.json")
    total_text = page.locator(r"text=/\d+ rides taken./").inner_text()
    total_trajets = int(total_text.split()[0])
    print(f"Total BIXI : {total_trajets}")
    page.get_by_role("link", name="Ride history").click()

    nb_trajets = total_trajets - already_scraped
    if nb_trajets == 0:
        print("Aucun nouveau trajet.")
        input("Appuie sur Entrée pour fermer le navigateur...")
        browser.close()
        return

    for i in range(nb_trajets//10):
        show_more_locator = page.locator('[data-testid="DATA_TESTID_SHOW_MORE"]') # pyright: ignore[reportPossiblyUnboundVariable]
        show_more_locator.scroll_into_view_if_needed()
        show_more_locator.click()

        #page.wait_for_load_state("networkidle")
        page.wait_for_timeout(250)


    trajets = page.locator('[data-testid="DATA_TESTID_RIDE_OVERVIEW_CARD"]').count()
    print(f"Nombre de trajets à ouvrir : {trajets}")
    for i in range(nb_trajets):
        trajet = page.locator('[data-testid="DATA_TESTID_RIDE_OVERVIEW_CARD"]').nth(i)
        
        trajet.scroll_into_view_if_needed()
        trajet.click()
        page.wait_for_timeout(250) 
        try:
            depart = page.locator('[class*="Start"]').locator('div').first.inner_text().split('\n')[0]
            arrivee = page.locator('[class*="End"]').locator('div').first.inner_text().split('\n')[0]
            print(f"Trajet {i+1} : {depart} -> {arrivee}")
            itineraire = (depart.strip(), arrivee.strip())

            if itineraire in historique:
                historique[itineraire] += 1
            else:
                historique[itineraire] = 1
            
        except Exception as e:
            print(f"Erreur d'extraction pour le trajet {i+1}")
            input("Appuie sur Entrée pour fermer le navigateur...")
        trajet.click()

    path = "data/statistiques_trajets.csv"

    if os.path.exists(path):
        df_old = pd.read_csv(path)
    else:
        df_old = pd.DataFrame(columns=["depart", "arrivee", "nb"])

    df_new = pd.DataFrame(
        [(dep, arr, nb) for (dep, arr), nb in historique.items()],
        columns=["depart", "arrivee", "nb"]
    )

    # 3. Fusion + agrégation
    df = pd.concat([df_old, df_new], ignore_index=True)
    df = df.groupby(["depart", "arrivee"], as_index=False)["nb"].sum()

    # CHECKK SYNTAX
    # df = df.sort_values(by=["nb", "depart", "arrivee"], ascending=(False, True, True))
    df.to_csv(path, index=False)


    input("Appuie sur Entrée pour fermer le navigateur...")
    
    browser.close()
        
def main():
    with sync_playwright() as playwright:
        run(playwright)
        
if __name__ == "__main__":
    main()