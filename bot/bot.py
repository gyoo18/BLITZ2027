from game_message import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: TeamGameState) -> list[Action]:
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        # Placement de volcan pour optimiser la surface d'effet
        if len(game_message.volcanoes) == 0:
            max_surf = -1
            max_m : WorldPosition = None
            for m in game_message.mountains:
                if m.y-game_message.map.origin.y < game_message.map.height//4 or m.y-game_message.map.origin.y > 3*game_message.map.height//4:
                    continue
                if self.surface_volcan(m, game_message) > max_surf:
                    max_surf = m.y
                    max_m = m
            if max_m:
                self.surface_volcan(max_m, game_message, afficher=True)
                return [TriggerVolcanoAction(max_m)]
        
        if game_message.dinosaurs:
            first_dinosaur = game_message.dinosaurs[0]
            actions.append(LaunchMeteorAction(target=first_dinosaur.position))

        # You can clearly do better than this. Have fun!!
        return actions

    def surface_volcan(self, montage : WorldPosition, game_message : TeamGameState, afficher=False) -> int:
        est_lave : list[list[bool]] = [None]*game_message.map.width
        for x in range(game_message.map.width):
            est_lave[x] = [False]*game_message.map.height
        est_lave[montage.x-game_message.map.origin.x][montage.y-game_message.map.origin.y] = True

        surface = 0
        while True:
            modifié = False
            for x in range(game_message.map.width):
                for y in range(game_message.map.height):

                    if not est_lave[x][y]:
                        continue
                    
                    min_cases : list[Tile] = []
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if ((dx == 0 and dy ==0) or
                                (dx != 0 and dy != 0) or
                                x+dx < 0 or
                                x+dx >= game_message.map.width or
                                y+dy < 0 or
                                y+dy >= game_message.map.height or
                                game_message.map.tiles[y+dy][x+dx].isMountain or 
                                game_message.map.tiles[y+dy][x+dx].isImpassable or
                                est_lave[x+dx][y+dy]):

                                continue
                            if (est_lave[x][y] and 
                                game_message.map.tiles[y+dy][x+dx].elevation <= game_message.map.tiles[y][x].elevation):

                                if len(min_cases) == 0 or (min_cases[0].elevation > game_message.map.tiles[y+dy][x+dx].elevation):
                                    min_cases.clear()
                                    min_cases = [game_message.map.tiles[y+dy][x+dx]]
                                elif min_cases[0].elevation == game_message.map.tiles[y+dy][x+dx].elevation:
                                    min_cases.append(game_message.map.tiles[y+dy][x+dx])
                    for c in min_cases:
                        x = c.position.x-game_message.map.origin.x
                        y = c.position.y-game_message.map.origin.y
                        est_lave[x][y] = True
                        surface += 1
                        modifié = True

            if afficher:
                carte_str = ""
                for y in range(len(est_lave[0])):
                    for x in range(len(est_lave)):
                        if x==montage.x-game_message.map.origin.x and y==montage.y-game_message.map.origin.y:
                            carte_str += ROUGE+"xx"
                        elif game_message.map.tiles[y][x].isMountain:
                            carte_str += GRIS+"^^"
                        elif game_message.map.tiles[y][x].isImpassable:
                            carte_str += BLEU+"OO"
                        else:
                            c = str(game_message.map.tiles[y][x].elevation)
                            carte_str += (ROUGE if est_lave[x][y] else VERT) + (c if len(c) == 2 else "0"+c)
                    carte_str += "\n"   
                print(carte_str+NTRE)
                pass     
            if not modifié:
                if afficher:
                    carte_str = ""
                    for y in range(len(est_lave[0])):
                        for x in range(len(est_lave)):
                            if x==montage.x-game_message.map.origin.x and y==montage.y-game_message.map.origin.y:
                                carte_str += ROUGE+"xx"
                            elif game_message.map.tiles[y][x].isMountain:
                                carte_str += GRIS+"^^"
                            elif game_message.map.tiles[y][x].isImpassable:
                                carte_str += BLEU+"OO"
                            else:
                                c = str(game_message.map.tiles[y][x].elevation)
                                carte_str += (ROUGE if est_lave[x][y] else VERT) + (c if len(c) == 2 else "0"+c)
                        carte_str += "\n"
                    print(carte_str+NTRE)
                return surface



ESC="\033["
"""Séquence d'échappement ANSI """
CURS=ESC+"s"
"""Sauvegarde la position du curseur. Utilisez CURA pour l'appliquer."""
CURA=ESC+"u"
"""Applique la position du curseur sauvegardée avec CURS. """
NTRE=ESC+"0m"
"""Réinitalise le style d'affichage. """
GRAS=ESC+"1m"
"""Met la police en gras """
FIN=ESC+"2m"
"""Met la police en fin, à l'opposé de gras """
ITAL=ESC+"3m"
"""Met la police en italique """
SOUL=ESC+"4m"
"""Met la police en souligné """
CLGN_LNT=ESC+"5m"
"""Fait lentement clignoter le texte """
CLGN_RPD=ESC+"6m"
"""Fait rapidement clignoter le texte """
INVRS=ESC+"7m"
"""Inverse les couleurs du terminal """
BARRE=ESC+"9m"
"""Met la police en barré """
NOIR=ESC+"30m"
"""Met la couleur de la police en noir """
ROUGE=ESC+"31m"
"""Met la couleur de la police en rouge """
VERT=ESC+"32m"
"""Met la couleur de la police en vert """
JAUNE=ESC+"33m"
"""Met la couleur de la police en jaune """
BLEU=ESC+"34m"
"""Met la couleur de la police en bleu """
MAGENTA=ESC+"35m"
"""Met la couleur de la police en magenta """
CYAN=ESC+"36m"
"""Met la couleur de la police en cyan """
GRIS_CLAIR=ESC+"37m"
"""Met la couleur de la police en gris clair """
GRIS=ESC+"90m"
"""Met la couleur de la police en gris """
ROUGE_CLAIR=ESC+"91m"
"""Met la couleur de la police en rouge clai """
VERT_CLAIR=ESC+"92m"
"""Met la couleur de la police en vert clair """
JAUNE_CLAIR=ESC+"93m"
"""Met la couleur de la police en jaune clair """
BLEU_CLAIR=ESC+"94m"
"""Met la couleur de la police en bleu clair """
MAGENTA_CLAIR=ESC+"95m"
"""Met la couleur de la police en magenta clair """
CYAN_CLAIR=ESC+"96m"
"""Met la couleur de la police en cyan clair """
BLANC=ESC+"97m"
"""Met la couleur de la police en blanc """
SURL_NOIR=ESC+"40m"
"""Met la couleur du surlignage en noir """
SURL_ROUGE=ESC+"41m"
"""Met la couleur du surlignage en rouge """
SURL_VERT=ESC+"42m"
"""Met la couleur du surlignage en vert """
SURL_JAUNE=ESC+"43m"
"""Met la couleur du surlignage en jaune """
SURL_BLEU=ESC+"44m"
"""Met la couleur du surlignage en bleu """
SURL_MAGENTA=ESC+"45m"
"""Met la couleur du surlignage en magenta """
SURL_CYAN=ESC+"46m"
"""Met la couleur du surlignage en cyan """
SURL_GRIS_CLAIR=ESC+"47m"
"""Met la couleur du surlignage en gris clair """
SURL_GRIS=ESC+"100m"
"""Met la couleur du surlignage en gris """
SURL_ROUGE_CLAIR=ESC+"101m"
"""Met la couleur du surlignage en rouge clair """
SURL_VERT_CLAIR=ESC+"102m"
"""Met la couleur du surlignage en vert clair """
SURL_JAUNE_CLAIR=ESC+"103m"
"""Met la couleur du surlignage en jaune clair """
SURL_BLEU_CLAIR=ESC+"104m"
"""Met la couleur du surlignage en bleu clair """
SURL_MAGENTA_CLAIR=ESC+"105m"
"""Met la couleur du surlignage en magenta clair """
SURL_CYAN_CLAIR=ESC+"106m"
"""Met la couleur du surlignage en cyan clair """
SURL_BLANC=ESC+"107m"
"""Met la couleur du surlignage en blanc """