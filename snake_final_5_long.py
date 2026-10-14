import os
import sys
import random
import pygame 

FICHIER_SCORES = os.path.join(os.getcwd(), "D:/Snake_Game_github/Snack_Game/high_scores.txt")

class Jeu:
    def __init__(self):
        pygame.init()

        self.ecran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Jeu Snake')
        self.jeu_encours = True

        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 10
        self.serpent_corps = 10
        self.vitesse = 10
        self.niveau = 1

        self.pomme_position_x = random.randrange(110, 690, 10)
        self.pomme_position_y = random.randrange(110, 590, 10)
        self.pomme = 10

        self.clock = pygame.time.Clock()

        self.positions_serpent = []
        self.taille_du_serpent = 1

        self.ecran_du_debut = True

        try:
            chemin_image = os.path.join(os.getcwd(), "D:/Snake_Game_github/Snack_Game/tete_serpent.png")
            self.image_tete_serpent_original = pygame.image.load(chemin_image)
            self.image_tete_serpent_original = pygame.transform.flip(self.image_tete_serpent_original, False, True)
            self.image_tete_serpent = pygame.transform.scale(self.image_tete_serpent_original, (self.serpent_corps, self.serpent_corps))
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image de la tête du serpent : {e}")
            pygame.quit()
            sys.exit()

        try:
            chemin_son = os.path.join(os.getcwd(), "D:/Snake_Game_github/Snack_Game/game_over.mp3")
            self.son_game_over = pygame.mixer.Sound(chemin_son)
        except pygame.error as e:
            print(f"Erreur lors du chargement du son Game Over : {e}")
            self.son_game_over = None

        self.score = 0

    def mettre_a_jour_score_en_temps_reel(self):
        with open(FICHIER_SCORES, 'w') as fichier:
            fichier.write(f'{{"score": {self.score}, "LEVEL": {self.niveau}}}\n')


    def charger_scores(self):
        try:
            with open(FICHIER_SCORES, 'r') as fichier:
                lignes = fichier.readlines()
                scores = []
                for ligne in lignes:
                    try:
                        score = eval(ligne.strip())  # Évalue chaque ligne
                        if isinstance(score, dict):  # Vérifie que c'est bien un dictionnaire
                            scores.append(score)
                    except (SyntaxError, ValueError):
                        continue  # Ignore les lignes invalides
                if not scores:
                    return [{"score": 0, "LEVEL": 1}]  # Valeur par défaut si aucun score valide
                return scores
        except FileNotFoundError:
            with open(FICHIER_SCORES, 'w') as fichier:
                fichier.write('{"score": 0, "LEVEL": 1}\n')
            return [{"score": 0, "LEVEL": 1}]


    def afficher_scores(self):
        self.ecran.fill((0, 0, 0))
        self.creer_message('grande', 'Meilleurs Scores par LEVEL', (200, 50, 400, 50), (255, 255, 255))

        scores = self.charger_scores()
        print("Scores chargés :", scores)  # Debugging pour vérifier les données

        # Trouver les meilleurs scores pour chaque niveau
        meilleurs_scores = {}
        for score in scores:
            if isinstance(score, dict):
                niveau = score.get("LEVEL", 0)
                points = score.get("score", 0)
                if niveau not in meilleurs_scores or points > meilleurs_scores[niveau]:
                    meilleurs_scores[niveau] = points

        # Écriture dans le fichier des scores formatés
        with open(FICHIER_SCORES, 'w') as fichier:
            for niveau, points in sorted(meilleurs_scores.items()):
                fichier.write(f"LEVEL {niveau}: {points} points\n")

        # Affichage dans le jeu
        y_position = 100
        for niveau, points in sorted(meilleurs_scores.items()):
            texte = f"LEVEL {niveau}: {points} points"
            self.creer_message('moyenne', texte, (200, y_position, 400, 50), (255, 255, 255))
            y_position += 50

        self.creer_message('moyenne', 'Appuyez sur Entrée pour retourner', (200, 500, 400, 50), (255, 255, 255))
        pygame.display.flip()

        attendre = True
        while attendre:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RETURN:
                        attendre = False



    def fonction_principale(self):
        while self.ecran_du_debut:
            self.ecran.fill((0, 0, 0))
            self.creer_message('grande', 'Snake Game', (320, 100, 200, 50), (255, 255, 255))
            self.creer_message('moyenne', 'Choisissez un niveau pour commencer', (220, 200, 400, 50), (255, 255, 255))

            for i in range(1, 6):
                self.creer_message('moyenne', f'LEVEL {i}', (350, 250 + i * 40, 100, 30), (255, 255, 255))

            self.creer_message('moyenne', 'Appuyez sur S pour voir les scores', (200, 500, 400, 50), (255, 255, 255))

            pygame.display.flip()

            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evenement.type == pygame.KEYDOWN:
                    if pygame.K_1 <= evenement.key <= pygame.K_5:
                        self.niveau = evenement.key - pygame.K_0
                        self.vitesse = 10 + (10 * (self.niveau - 1))
                        self.ecran_du_debut = False

                    if evenement.key == pygame.K_s:
                        self.afficher_scores()

        while self.jeu_encours:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RIGHT and self.serpent_direction_x == 0:
                        self.serpent_direction_x = 10
                        self.serpent_direction_y = 0

                    if evenement.key == pygame.K_LEFT and self.serpent_direction_x == 0:
                        self.serpent_direction_x = -10
                        self.serpent_direction_y = 0

                    if evenement.key == pygame.K_DOWN and self.serpent_direction_y == 0:
                        self.serpent_direction_y = 10
                        self.serpent_direction_x = 0

                    if evenement.key == pygame.K_UP and self.serpent_direction_y == 0:
                        self.serpent_direction_y = -10
                        self.serpent_direction_x = 0

            if self.serpent_position_x <= 100 or self.serpent_position_x >= 700 \
                    or self.serpent_position_y <= 100 or self.serpent_position_y >= 600:
                self.game_over()

            if self.pomme_position_y == self.serpent_position_y and self.serpent_position_x == self.pomme_position_x:
                self.pomme_position_x = random.randrange(110, 690, 10)
                self.pomme_position_y = random.randrange(110, 590, 10)

                self.taille_du_serpent += 1
                self.score += 1
                self.mettre_a_jour_score_en_temps_reel()

            self.serpent_mouvement()

            la_tete_du_serpent = [self.serpent_position_x, self.serpent_position_y]
            self.positions_serpent.append(la_tete_du_serpent)

            if len(self.positions_serpent) > self.taille_du_serpent:
                self.positions_serpent.pop(0)

            self.afficher_les_elements()
            self.se_mord(la_tete_du_serpent)

            self.creer_message('grande', 'Snake Game', (320, 10, 200, 50), (255, 255, 255))
            self.creer_message('grande', str(self.score), (375, 50, 50, 50), (255, 255, 255))

            self.creer_limites()
            self.clock.tick(self.vitesse)
            pygame.display.flip()

    def creer_limites(self):
        pygame.draw.rect(self.ecran, (255, 255, 255), (100, 100, 600, 500), 3)


    def afficher_menu_niveau(self):
        self.ecran.fill((0, 0, 0))
        self.creer_message('grande', f'LEVEL {self.niveau}', (320, 200, 200, 50), (255, 255, 255))
        self.creer_message('moyenne', 'Appuyez sur Entrée pour continuer', (200, 400, 400, 50), (255, 255, 255))
        pygame.display.flip()

        attendre = True
        while attendre:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RETURN:
                        attendre = False

    def serpent_mouvement(self):
        self.serpent_position_x += self.serpent_direction_x
        self.serpent_position_y += self.serpent_direction_y

    def afficher_les_elements(self):
        self.ecran.fill((0, 0, 0))

        angle = 0
        if self.serpent_direction_x > 0:
            angle = -90
        elif self.serpent_direction_x < 0:
            angle = 90
        elif self.serpent_direction_y < 0:
            angle = 0
        elif self.serpent_direction_y > 0:
            angle = 180

        tete_rotated = pygame.transform.rotate(self.image_tete_serpent, angle)
        self.ecran.blit(tete_rotated, (self.serpent_position_x, self.serpent_position_y))
        
        
        pygame.draw.rect(self.ecran, (255, 0, 0),
                         (self.pomme_position_x, self.pomme_position_y, self.pomme, self.pomme))

        self.afficher_Serpent()

    def reinitialiser_jeu(self):
        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 10
        self.positions_serpent = []
        self.taille_du_serpent = 1
        self.pomme_position_x = random.randrange(110, 690, 10)
        self.pomme_position_y = random.randrange(110, 590, 10)

    def afficher_Serpent(self):
        for partie_du_serpent in self.positions_serpent[:-1]:
            pygame.draw.rect(self.ecran, (0, 255, 0),
                             (partie_du_serpent[0], partie_du_serpent[1], self.serpent_corps, self.serpent_corps))

    def se_mord(self, tete_serpent):
        for partie_serpent in self.positions_serpent[:-1]:
            if partie_serpent == tete_serpent:
                self.game_over()

    def creer_message(self, font, message, message_rectangle, couleur):
        if font == 'petite':
            font = pygame.font.SysFont('Lato', 20, False)

        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 30, False)

        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 40, True)

        message = font.render(message, True, couleur)

        self.ecran.blit(message, message_rectangle)

    def game_over(self):
        if self.son_game_over:
            self.son_game_over.play()

        self.ecran.fill((0, 0, 0))
        self.creer_message('grande', 'Game Over', (320, 250, 200, 50), (255, 0, 0))
        self.creer_message('moyenne', f'Votre score : {self.score}', (250, 300, 300, 50), (255, 255, 255))
        self.creer_message('moyenne', 'Appuyez sur Entrée pour rejouer ', (250, 350, 500, 50), (255, 255, 255))
        self.creer_message('moyenne', 'Appuyez sur Échap pour quitter', (250, 400, 500, 50), (255, 255, 255))

        pygame.display.flip()

        while True:
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_RETURN:
                        self.__init__()
                        self.fonction_principale()
                    if evenement.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()


        


if __name__ == '__main__':
    pygame.init()
    Jeu().fonction_principale()
    pygame.quit()
