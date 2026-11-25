import json
import ipaddress

FICHIER = "equipements.json"


def charger():
    """Lit le fichier JSON. Renvoie une liste vide si le fichier est absent ou illisible."""
    try:
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Fichier de données absent : démarrage avec une liste vide.")
        return []
    except json.JSONDecodeError:
        print("Fichier de données illisible : démarrage avec une liste vide.")
        return []


def sauvegarder(equipements):
    """Écrit la liste dans le fichier JSON."""
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(equipements, f, indent=4, ensure_ascii=False)


def valider(ip, masque):
    """Renvoie l'interface réseau si IP et masque sont valides, sinon None."""
    try:
        return ipaddress.ip_interface(f"{ip}/{masque}")
    except ValueError:
        return None


def ajouter(equipements):
    nom = input("Nom : ").strip()
    type_eq = input("Type (ordinateur, imprimante, serveur, routeur) : ").strip()
    ip = input("Adresse IP : ").strip()
    masque = input("Masque : ").strip()

    if nom == "" or type_eq == "":
        print("Erreur : le nom et le type sont obligatoires.")
        return
    if valider(ip, masque) is None:
        print("Erreur : adresse IP ou masque invalide.")
        return
    for eq in equipements:
        if eq["ip"] == ip:
            print("Erreur : cette adresse IP existe déjà.")
            return

    equipements.append({"nom": nom, "type": type_eq, "ip": ip, "masque": masque})
    sauvegarder(equipements)
    print("Équipement ajouté.")


def afficher(equipements):
    if len(equipements) == 0:
        print("Aucun équipement enregistré.")
        return
    for eq in equipements:
        print(f"{eq['nom']} | {eq['type']} | {eq['ip']} | {eq['masque']}")


def rechercher(equipements):
    ip = input("Adresse IP à rechercher : ").strip()
    for eq in equipements:
        if eq["ip"] == ip:
            print(f"Trouvé : {eq['nom']} ({eq['type']}), masque {eq['masque']}")
            return
    print("Aucun équipement avec cette adresse IP.")


def regrouper(equipements):
    if len(equipements) == 0:
        print("Aucun équipement enregistré.")
        return
    groupes = {}
    for eq in equipements:
        interface = valider(eq["ip"], eq["masque"])
        if interface is None:
            continue
        reseau = str(interface.network)
        if reseau not in groupes:
            groupes[reseau] = []
        groupes[reseau].append(eq["nom"])

    for reseau, noms in groupes.items():
        print(f"Sous-réseau {reseau} : {', '.join(noms)}")


def menu():
    equipements = charger()
    while True:
        print("\n--- Inventaire réseau ---")
        print("1. Ajouter un équipement")
        print("2. Afficher les équipements")
        print("3. Rechercher par adresse IP")
        print("4. Regrouper par sous-réseau")
        print("5. Quitter")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            ajouter(equipements)
        elif choix == "2":
            afficher(equipements)
        elif choix == "3":
            rechercher(equipements)
        elif choix == "4":
            regrouper(equipements)
        elif choix == "5":
            print("Au revoir.")
            break
        else:
            print("Choix invalide, tapez un chiffre de 1 à 5.")
menu()






