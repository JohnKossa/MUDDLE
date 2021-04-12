from game_objects.Enemy import Enemy


class BossEnemy(Enemy):
    from game_objects.Commands.CombatCommands.AttackCommand import AttackCommand

    def __init__(self):
        super().__init__()

    def get_action(self) -> AttackCommand:
        pass