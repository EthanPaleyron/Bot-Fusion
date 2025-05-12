from instagrapi import Client
import schedule
import time
from dotenv import load_dotenv
import os

# Charger les identifiants depuis .env
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# Vérification des identifiants
if not USERNAME or not PASSWORD:
    print("Les identifiants Instagram sont manquants. Vérifiez votre fichier .env.")
    exit(1)

# Initialisation du client Insta
cl = Client()

# Tentative de login, et sauvegarde de la session
try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")  # Sauvegarder la session après une connexion réussie
    print("Connexion réussie et session sauvegardée.")
except Exception as e:
    print("Erreur de connexion :", e)
    exit(1)  # Arrêter le script si la connexion échoue

# Fonction d'envoi de message
def send_daily_message():
    try:
        # Récupérer tous les threads (groupes)
        threads = cl.direct_threads()
        for thread in threads:
            # Vérifie si le titre du thread contient "Test_fusion"
            if "Test_fusion" in thread.thread_title:
                # Envoie le message au groupe
                cl.direct_send("Message automatique envoyé à 08h00 🌙", thread_ids=[thread.id])
                print(f"Message envoyé au groupe: {thread.thread_title}")
                break
        else:
            print("Aucun thread contenant 'Test_fusion' n'a été trouvé.")
    except Exception as e:
        print("Erreur lors de l'envoi du message :", e)

# Programmer l'envoi quotidien à 08h00
schedule.every().day.at("08:00").do(send_daily_message)

# Boucle infinie qui vérifie l'heure
try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    print("Arrêt du script.")
