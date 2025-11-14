import subprocess
import sys
import time

import requests


def wait_for_server(url, timeout=10):
    """Attend que le serveur Flask soit UP."""
    for _ in range(timeout * 10):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.1)
    return False


def main():
    print("Démarrage du serveur Flask pour les tests Locust...")

    # Lancement du serveur Flask dans un process
    flask_proc = subprocess.Popen(
        [sys.executable, "-m", "gudlft_reservation.server"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Attendre qu’il soit en ligne
    if not wait_for_server("http://127.0.0.1:5000"):
        print("ERREUR : Le serveur Flask ne démarre pas.")
        flask_proc.terminate()
        return

    print("Serveur Flask lancé sur http://127.0.0.1:5000")

    # Lancer locust avec le bon dossier
    print("Lancement de Locust...")
    try:
        subprocess.run(["locust", "-f", "tests/performance/locustfile.py"], check=True)
    except KeyboardInterrupt:
        print("\nLocust arrêté manuellement.")

    print("Arrêt du serveur Flask...")
    flask_proc.terminate()
    flask_proc.wait()
    print("Serveur arrêté proprement.")


if __name__ == "__main__":
    main()
