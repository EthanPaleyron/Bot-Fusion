from instagrapi import Client
import schedule
import time
from dotenv import load_dotenv
import os

# Charger les identifiants depuis .env
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# Initialisation du client Insta
cl = Client()

# Tentative de login, et sauvegarde de la session
try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")  # Sauvegarder la session après une connexion réussie
    print("Connexion réussie et session sauvegardée.")
except Exception as e:
    print("Erreur de connexion :", e)

# Fonction d'envoi de message
def send_daily_message():
    # Récupérer tous les threads (groupes)
    threads = cl.direct_threads()

    for thread in threads:
        # Vérifie si le titre du thread contient "Test_fusion"
        if "Test_fusion" in thread.thread_title:
            # Envoie le message au groupe
            cl.direct_send("Message automatique envoyé à 08h00 🌙", thread_ids=[thread.id])
            print(f"Message envoyé au groupe: {thread.thread_title}")
            break  # Arrête la boucle une fois le message envoyé

# Programmer l'envoi quotidien à 00h31
schedule.every().day.at("08:00").do(send_daily_message)

# Boucle infinie qui vérifie l'heure
while True:
    schedule.run_pending()
    time.sleep(60)
