"""
Configuration générale de l'application :
- Limites de réservation
- Format des dates
- Date actuelle utilisée pour les validations
"""

from datetime import datetime

MAX_PLACES_REQUESTED = 12
CURRENT_DATETIME = datetime.now()
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
