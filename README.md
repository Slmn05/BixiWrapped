# 🚲 BixiWrapped

**BixiWrapped** est un projet Python personnel qui analyse et visualise l'historique de trajets BIXI d'un utilisateur montréalais — un peu à la manière d'un *Spotify Wrapped*, mais pour le vélo.

Le projet se décompose en deux étapes : la collecte automatique des données depuis le site BIXI, puis la génération d'une carte interactive affichant les itinéraires empruntés sur le réseau cyclable de Montréal.

---

## Fonctionnalités

- **Scraping automatisé** du site `bixi.com` via Playwright (authentification, navigation, extraction des trajets)
- **Persistance incrémentale** : les trajets déjà récupérés sont conservés dans un CSV, seuls les nouveaux sont collectés à chaque exécution
- **Mise en cache de session** : le cookie de connexion est sauvegardé localement pour éviter de se reconnecter à chaque fois
- **Calcul d'itinéraires** sur le réseau cyclable réel de Montréal grâce à OSMnx et NetworkX
- **Visualisation interactive** des trajets sous forme de carte Folium, où l'épaisseur des lignes est proportionnelle à la fréquence du trajet
- **Mise en cache des routes** calculées pour accélérer les exécutions suivantes

---

## Structure du projet

```
BixiWrapped/
├── scrapping.py          # Collecte des trajets depuis le site BIXI
├── traces.py             # Calcul et visualisation des itinéraires sur carte
├── requirements.txt      # Dépendances Python
├── .gitignore
└── data/
    ├── statistiques_trajets.csv   # Trajets collectés (départ, arrivée, fréquence)
    ├── bixi_stations.csv          # Coordonnées des stations BIXI
    ├── montreal_bike.graphml      # Carte du réseau cyclable (générée automatiquement)
    ├── route_cache.pkl            # Cache des itinéraires calculés
    ├── state.json                 # Cookie de session BIXI
    └── resultat_bixi_csv.html     # Carte interactive générée
```

---

## Installation

### Prérequis

- Python 3.10+
- Un compte BIXI actif

### Étapes

```bash
# Cloner le dépôt
git clone https://github.com/Slmn05/BixiWrapped.git
cd BixiWrapped

# Installer les dépendances
pip install -r requirements.txt

# Installer les navigateurs pour Playwright
playwright install chromium
```

### Configuration

Créer un fichier `.env` à la racine du projet :

```env
BIXI_USERNAME=ton_email@exemple.com
BIXI_PASSWORD=ton_mot_de_passe
```

Ajouter également un fichier `data/bixi_stations.csv` contenant les coordonnées des stations BIXI avec les colonnes `name`, `lat`, `lon`. Ce fichier peut être obtenu depuis l'[open data de BIXI Montréal](https://bixi.com/en/open-data/).

---

## Utilisation

### Étape 1 — Collecter les trajets

```bash
python scrapping.py
```

Le script ouvre un navigateur Chromium, se connecte à ton compte BIXI, parcourt l'historique de trajets et enregistre les résultats dans `data/statistiques_trajets.csv`.

### Étape 2 — Générer la carte

```bash
python traces.py
```

Le script charge la carte cyclable de Montréal (téléchargée automatiquement via OpenStreetMap lors de la première exécution), calcule le plus court chemin pour chaque trajet, et génère une carte interactive dans `data/resultat_bixi_csv.html`.

Ouvre ce fichier dans un navigateur pour visualiser tes trajets !

---

## Dépendances principales

| Bibliothèque | Usage |
|---|---|
| `playwright` | Automatisation du navigateur pour le scraping |
| `pandas` | Manipulation des données CSV |
| `osmnx` | Téléchargement et gestion du réseau routier OSM |
| `networkx` | Calcul des plus courts chemins |
| `folium` | Génération de cartes interactives |
| `python-dotenv` | Chargement des identifiants depuis `.env` |

---

## Notes

- La première exécution de `traces.py` peut prendre plusieurs minutes, le temps de télécharger la carte cyclable de Montréal depuis OpenStreetMap.
- Les routes calculées sont mises en cache dans `route_cache.pkl` pour accélérer les exécutions suivantes.
- Le fichier `state.json` contient la session BIXI. Ne pas le partager publiquement.

---

## Auteur

Projet personnel développé par [@Slmn05](https://github.com/Slmn05).