import os
import subprocess
import time

import requests


def wait_for_server(url, timeout=10):
    """Attend que le serveur Flask réponde avec un statut 200 avant de continuer."""
    for _ in range(timeout * 10):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(0.1)
    return False


def main():
    """Démarre Flask pour les tests Locust, lance Locust, puis arrête proprement le serveur."""
    print("Démarrage du serveur Flask pour les tests Locust...")

    # -----------------------------
    # VARIABLES D’ENVIRONNEMENT
    # -----------------------------
    LOCUST_USERS = "6"
    LOCUST_SPAWN_RATE = "1"

    # Injecte les variables dans l’environnement
    env = {
        **os.environ,
        "LOCUST_USERS": LOCUST_USERS,
        "LOCUST_SPAWN_RATE": LOCUST_SPAWN_RATE,
    }

    # -----------------------------
    # Lancer Flask via pipenv
    # -----------------------------
    flask_proc = subprocess.Popen(
        ["pipenv", "run", "flask", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        env=env,
    )

    # Attendre que Flask soit UP
    if not wait_for_server("http://127.0.0.1:5000"):
        print("ERREUR : Le serveur Flask ne démarre pas.")
        flask_proc.terminate()
        return

    print("Serveur Flask lancé → http://127.0.0.1:5000")

    print("Lancement de Locust...\n")

    try:
        subprocess.run(
            ["pipenv", "run", "locust", "-f", "tests/performance/locustfile.py"],
            check=True,
            env=env,
        )
        input("Appuyez sur Entrée pour arrêter Locust...")
    except KeyboardInterrupt:
        print("\nLocust arrêté manuellement.")

    print("Arrêt du serveur Flask...")
    flask_proc.terminate()
    flask_proc.wait()
    print("Serveur arrêté correctement.")


if __name__ == "__main__":
    main()
