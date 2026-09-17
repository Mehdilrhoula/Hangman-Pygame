import sys
import random
import pygame
import time


if len(sys.argv) == 1:
    print("Error: missing argument")
    exit()

if len(sys.argv) > 2:
    print("Error: too many arguments")
    exit()


try:
    fichier = open(sys.argv[1], encoding="utf-8")
except FileNotFoundError:
    print("Error: file not found")
    exit()


mots = []

for ligne in fichier:
    mot = ligne.strip()

    if mot == "":
        continue

    if " " in mot:
        print("Error: invalid file format")
        fichier.close()
        exit()

    if not mot.isalpha():
        print("Error: invalid file format")
        fichier.close()
        exit()

    mots.append(mot.lower())

fichier.close()


if len(mots) == 0:
    print("Error: no words found")
    exit()


pygame.init()

LARGEUR = 1200
HAUTEUR = 800

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))

pygame.display.set_caption("Hangman")


NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (220, 220, 220)
GRIS_FONCE = (100, 100, 100)
VERT = (50, 170, 80)
ROUGE = (200, 50, 50)
ORANGE = (240, 150, 40)


police_titre = pygame.font.Font(None, 80)
police_bouton = pygame.font.Font(None, 45)
police_texte = pygame.font.Font(None, 38)
police_mot = pygame.font.Font(None, 65)
police_petit = pygame.font.Font(None, 30)


def afficher_texte_centre(texte, police, couleur, y):

    image = police.render(
        texte,
        True,
        couleur
    )

    rectangle = image.get_rect()

    rectangle.centerx = LARGEUR // 2
    rectangle.y = y

    fenetre.blit(image, rectangle)


def dessiner_bouton(texte, rectangle):

    pygame.draw.rect(
        fenetre,
        GRIS,
        rectangle,
        border_radius=10
    )

    pygame.draw.rect(
        fenetre,
        NOIR,
        rectangle,
        3,
        border_radius=10
    )

    image = police_bouton.render(
        texte,
        True,
        NOIR
    )

    texte_rectangle = image.get_rect()

    texte_rectangle.center = rectangle.center

    fenetre.blit(
        image,
        texte_rectangle
    )


def dessiner_pendu(penalites):

    if penalites >= 1:
        pygame.draw.line(
            fenetre,
            NOIR,
            (100, 650),
            (400, 650),
            7
        )

    if penalites >= 2:
        pygame.draw.line(
            fenetre,
            NOIR,
            (170, 650),
            (170, 180),
            7
        )

    if penalites >= 3:
        pygame.draw.line(
            fenetre,
            NOIR,
            (170, 180),
            (450, 180),
            7
        )

    if penalites >= 4:
        pygame.draw.line(
            fenetre,
            NOIR,
            (450, 180),
            (450, 240),
            7
        )

    if penalites >= 5:
        pygame.draw.circle(
            fenetre,
            NOIR,
            (450, 300),
            60,
            7
        )

    if penalites >= 6:

        pygame.draw.line(
            fenetre,
            NOIR,
            (450, 360),
            (450, 510),
            7
        )

        pygame.draw.line(
            fenetre,
            NOIR,
            (450, 400),
            (370, 470),
            7
        )

        pygame.draw.line(
            fenetre,
            NOIR,
            (450, 400),
            (530, 470),
            7
        )

        pygame.draw.line(
            fenetre,
            NOIR,
            (450, 510),
            (370, 610),
            7
        )

        pygame.draw.line(
            fenetre,
            NOIR,
            (450, 510),
            (530, 610),
            7
        )


def dessiner_barre_vie(vies, vies_max):

    x = 750
    y = 170
    largeur = 350
    hauteur = 30

    pygame.draw.rect(
        fenetre,
        GRIS,
        (x, y, largeur, hauteur),
        border_radius=10
    )

    largeur_vie = int(largeur * vies / vies_max)

    couleur = VERT

    if vies <= 2:
        couleur = ROUGE
    elif vies <= 4:
        couleur = ORANGE

    pygame.draw.rect(
        fenetre,
        couleur,
        (x, y, largeur_vie, hauteur),
        border_radius=10
    )

    pygame.draw.rect(
        fenetre,
        NOIR,
        (x, y, largeur, hauteur),
        3,
        border_radius=10
    )

    texte = police_petit.render(
        "VIES",
        True,
        NOIR
    )

    fenetre.blit(
        texte,
        (750, 125)
    )


def charger_scores():

    scores = []

    try:
        fichier_scores = open(
            "scores.txt",
            "r",
            encoding="utf-8"
        )

        for ligne in fichier_scores:

            ligne = ligne.strip()

            if "|" not in ligne:
                continue

            nom, score = ligne.split("|")

            try:
                scores.append(
                    (nom, int(score))
                )
            except ValueError:
                continue

        fichier_scores.close()

    except FileNotFoundError:
        pass

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores


def sauvegarder_score(nom, score):

    fichier_scores = open(
        "scores.txt",
        "a",
        encoding="utf-8"
    )

    fichier_scores.write(
        nom + "|" + str(score) + "\n"
    )

    fichier_scores.close()


def leaderboard():

    bouton_retour = pygame.Rect(
        450,
        650,
        300,
        70
    )

    page = True

    while page:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if bouton_retour.collidepoint(event.pos):
                    return

        fenetre.fill(BLANC)

        afficher_texte_centre(
            "LEADERBOARD",
            police_titre,
            NOIR,
            60
        )

        scores = charger_scores()

        if len(scores) == 0:

            afficher_texte_centre(
                "Aucun score pour le moment",
                police_texte,
                NOIR,
                250
            )

        else:

            for i, (nom, score) in enumerate(scores[:10]):

                texte = str(i + 1) + ". " + nom + "   " + str(score)

                afficher_texte_centre(
                    texte,
                    police_texte,
                    NOIR,
                    180 + i * 45
                )

        dessiner_bouton(
            "RETOUR",
            bouton_retour
        )

        pygame.display.flip()


def choisir_difficulte():

    boutons = {
        "facile": pygame.Rect(400, 250, 400, 70),
        "normal": pygame.Rect(400, 350, 400, 70),
        "difficile": pygame.Rect(400, 450, 400, 70),
        "retour": pygame.Rect(400, 600, 400, 70)
    }

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boutons["facile"].collidepoint(event.pos):
                    return "facile"

                if boutons["normal"].collidepoint(event.pos):
                    return "normal"

                if boutons["difficile"].collidepoint(event.pos):
                    return "difficile"

                if boutons["retour"].collidepoint(event.pos):
                    return None

        fenetre.fill(BLANC)

        afficher_texte_centre(
            "DIFFICULTE",
            police_titre,
            NOIR,
            100
        )

        dessiner_bouton(
            "FACILE",
            boutons["facile"]
        )

        dessiner_bouton(
            "NORMAL",
            boutons["normal"]
        )

        dessiner_bouton(
            "DIFFICILE",
            boutons["difficile"]
        )

        dessiner_bouton(
            "RETOUR",
            boutons["retour"]
        )

        pygame.display.flip()


def obtenir_parametres(difficulte):

    if difficulte == "facile":
        return 8, 120

    if difficulte == "normal":
        return 6, 90

    return 5, 60


def lettre_ia(mot, lettres_proposees):

    frequences = {
        "e": 12,
        "a": 8,
        "i": 7,
        "s": 7,
        "n": 7,
        "r": 6,
        "t": 6,
        "o": 5,
        "l": 5,
        "u": 5,
        "d": 4,
        "c": 3,
        "m": 3,
        "p": 3,
        "g": 2,
        "b": 2,
        "f": 2,
        "h": 2,
        "v": 2,
        "j": 1,
        "q": 1,
        "k": 1,
        "w": 1,
        "x": 1,
        "y": 1,
        "z": 1
    }

    lettres_disponibles = []

    for lettre in mot:

        if lettre not in lettres_proposees:
            lettres_disponibles.append(lettre)

    if len(lettres_disponibles) == 0:
        return None

    meilleure = lettres_disponibles[0]

    for lettre in lettres_disponibles:

        if frequences.get(lettre, 0) > frequences.get(meilleure, 0):
            meilleure = lettre

    return meilleure


def demander_nom():

    nom = ""
    actif = True

    while actif:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if nom != "":
                        return nom

                elif event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]

                else:

                    if len(nom) < 12 and event.unicode.isalnum():
                        nom += event.unicode

        fenetre.fill(BLANC)

        afficher_texte_centre(
            "ENTRE TON NOM",
            police_titre,
            NOIR,
            150
        )

        afficher_texte_centre(
            nom + "_",
            police_texte,
            NOIR,
            300
        )

        afficher_texte_centre(
            "Appuie sur ENTREE",
            police_texte,
            GRIS_FONCE,
            400
        )

        pygame.display.flip()


def ecran_fin(victoire, mot, score):

    nom = None

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if nom is None:
                        nom = demander_nom()

                        sauvegarder_score(
                            nom,
                            score
                        )

                    return

        fenetre.fill(BLANC)

        if victoire:

            afficher_texte_centre(
                "BRAVO !",
                police_titre,
                VERT,
                150
            )

            afficher_texte_centre(
                "Mot : " + mot,
                police_texte,
                NOIR,
                270
            )

        else:

            afficher_texte_centre(
                "PERDU !",
                police_titre,
                ROUGE,
                150
            )

            afficher_texte_centre(
                "Mot : " + mot,
                police_texte,
                NOIR,
                270
            )

        afficher_texte_centre(
            "Score : " + str(score),
            police_texte,
            NOIR,
            350
        )

        if nom is None:

            afficher_texte_centre(
                "Appuie sur ENTREE pour enregistrer ton score",
                police_texte,
                NOIR,
                480
            )

        pygame.display.flip()


def jouer(difficulte):

    vies_max, temps_max = obtenir_parametres(
        difficulte
    )

    mot = random.choice(mots)

    lettres_cachees = []

    for lettre in mot:
        lettres_cachees.append("_")

    lettres_proposees = []

    penalites = 0
    score = 0

    debut = time.time()

    jeu = True
    victoire = False

    horloge = pygame.time.Clock()

    while jeu:

        temps_ecoule = int(time.time() - debut)
        temps_restant = temps_max - temps_ecoule

        if temps_restant <= 0:

            temps_restant = 0
            jeu = False
            victoire = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_h:

                    aide = lettre_ia(
                        mot,
                        lettres_proposees
                    )

                    if aide is not None:
                        lettres_proposees.append(aide)

                        for i in range(len(mot)):

                            if mot[i] == aide:
                                lettres_cachees[i] = aide

                        score -= 25

                else:

                    lettre = event.unicode.lower()

                    if lettre.isalpha():

                        if lettre not in lettres_proposees:

                            lettres_proposees.append(
                                lettre
                            )

                            if lettre in mot:

                                for i in range(len(mot)):

                                    if mot[i] == lettre:
                                        lettres_cachees[i] = lettre

                                score += 100

                            else:

                                penalites += 1
                                score -= 50

        if "_" not in lettres_cachees:

            bonus_temps = temps_restant * 5

            score += bonus_temps

            victoire = True
            jeu = False

        if penalites >= vies_max:

            victoire = False
            jeu = False

        fenetre.fill(BLANC)

        afficher_texte_centre(
            "HANGMAN",
            police_titre,
            NOIR,
            20
        )

        dessiner_pendu(
            penalites
        )

        afficher_texte_centre(
            " ".join(lettres_cachees),
            police_mot,
            NOIR,
            300
        )

        afficher_texte_centre(
            "Lettres : " + " ".join(lettres_proposees),
            police_texte,
            NOIR,
            420
        )

        vies_restantes = vies_max - penalites

        dessiner_barre_vie(
            vies_restantes,
            vies_max
        )

        afficher_texte_centre(
            "Vies : " + str(vies_restantes) + " / " + str(vies_max),
            police_texte,
            ROUGE if vies_restantes <= 2 else NOIR,
            540
        )

        afficher_texte_centre(
            "TEMPS : " + str(temps_restant) + " s",
            police_texte,
            ROUGE if temps_restant <= 10 else NOIR,
            600
        )

        afficher_texte_centre(
            "SCORE : " + str(score),
            police_texte,
            NOIR,
            660
        )

        afficher_texte_centre(
            "Difficulte : " + difficulte.upper(),
            police_petit,
            GRIS_FONCE,
            710
        )

        afficher_texte_centre(
            "Appuie sur H pour demander une aide a l'IA (-25 points)",
            police_petit,
            GRIS_FONCE,
            750
        )

        pygame.display.flip()

        horloge.tick(60)

    ecran_fin(
        victoire,
        mot,
        max(0, score)
    )


def menu_principal():

    boutons = {
        "jouer": pygame.Rect(
            450,
            250,
            300,
            70
        ),

        "scores": pygame.Rect(
            450,
            340,
            300,
            70
        ),

        "credits": pygame.Rect(
            450,
            430,
            300,
            70
        ),

        "quitter": pygame.Rect(
            450,
            520,
            300,
            70
        )
    }

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if boutons["jouer"].collidepoint(event.pos):
                    return "jouer"

                if boutons["scores"].collidepoint(event.pos):
                    return "scores"

                if boutons["credits"].collidepoint(event.pos):
                    return "credits"

                if boutons["quitter"].collidepoint(event.pos):
                    pygame.quit()
                    exit()

        fenetre.fill(BLANC)

        afficher_texte_centre(
            "HANGMAN",
            police_titre,
            NOIR,
            100
        )

        dessiner_bouton(
            "JOUER",
            boutons["jouer"]
        )

        dessiner_bouton(
            "LEADERBOARD",
            boutons["scores"]
        )

        dessiner_bouton(
            "CREDITS",
            boutons["credits"]
        )

        dessiner_bouton(
            "QUITTER",
            boutons["quitter"]
        )

        pygame.display.flip()


def credits():

    bouton_retour = pygame.Rect(
        450,
        600,
        300,
        70
    )

    page = True

    while page:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if bouton_retour.collidepoint(event.pos):
                    return

        fenetre.fill(BLANC)

        afficher_texte_centre(
            "CREDITS",
            police_titre,
            NOIR,
            100
        )

        afficher_texte_centre(
            "Hangman",
            police_texte,
            NOIR,
            250
        )

        afficher_texte_centre(
            "Python + Pygame",
            police_texte,
            NOIR,
            320
        )

        afficher_texte_centre(
            "Projet informatique",
            police_texte,
            NOIR,
            390
        )

        dessiner_bouton(
            "RETOUR",
            bouton_retour
        )

        pygame.display.flip()


while True:

    choix = menu_principal()

    if choix == "jouer":

        difficulte = choisir_difficulte()

        if difficulte is not None:
            jouer(difficulte)

    elif choix == "scores":

        leaderboard()

    elif choix == "credits":

        credits()