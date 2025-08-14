# Congrès Sûreté — Plateforme Django

Fonctions : inscription, réservation hôtelière, paiement CMI, annulation & remboursement, dashboard.

## Démarrage
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata demo_hotels
python manage.py runserver
```
- Front: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Notes
- Paiement en **simulation** par défaut (succès immédiat). Passer `CMI_MODE=live` en production et renseigner les secrets.
- Les règles d'annulation/remboursement sont configurables via `.env` (variable `REFUND_RULES`).
