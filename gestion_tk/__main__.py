import argparse
import os
from datetime import date

from .bank import Bank, default_path


def main() -> None:
    parser = argparse.ArgumentParser(prog="gestion-tk", description="Gestion bancaire de bureau.")
    parser.add_argument(
        "--db",
        default=os.environ.get("GESTION_TK_DB"),
        help="fichier SQLite (par défaut ~/.local/share/gestion-tk/banque.sqlite3)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="crée un client de démonstration avec trois mois d'opérations, puis quitte",
    )
    args = parser.parse_args()
    bank = Bank(args.db or default_path())

    if args.demo:
        from .demo import DEMO_PIN, seed

        customer = seed(bank, date.today())
        print(f"Client de démonstration créé : numéro {customer.number}, code {DEMO_PIN}.")
        return

    try:
        from .ui.app import App
    except ImportError as err:  # tkinter missing from this Python build
        raise SystemExit(
            "Tkinter est introuvable. Sur Debian/Ubuntu : sudo apt install python3-tk"
        ) from err
    App(bank).run()


if __name__ == "__main__":
    main()
