from game_message import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: TeamGameState) -> list[Action]:
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        # The engine applies only ONE action per turn (actions[0]); extra actions
        # are ignored and reported in lastTickErrors.

        # Baseline strategy: grab the first dinosaur we can see and drop a meteor
        # right on top of it. This is intentionally simple and far from optimal:
        # it just shows the shape of a working bot.
        if game_message.dinosaurs:
            first_dinosaur = game_message.dinosaurs[0]
            actions.append(LaunchMeteorAction(target=first_dinosaur.position))

        # You can clearly do better than this. Have fun!!
        return actions
