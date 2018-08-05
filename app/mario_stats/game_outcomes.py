from math import ceil


def calculate_scores_needed(game):
    net_red_handicap = 0  # Higher means red is better
    snapshot = game.handicap_snapshot

    for player in game.players.all():
        relevant_handicap_snapshot = snapshot.players.all().filter(person=player.person).first()
        if player.red_team:
            net_red_handicap += relevant_handicap_snapshot.handicap
        else:
            net_red_handicap -= relevant_handicap_snapshot.handicap
    net_red_handicap = float(net_red_handicap)

    return {
        'to win': {
            'red': ceil(205 + net_red_handicap * 5 / 2.0 + 0.25),
            'blue': ceil(205 - net_red_handicap * 5 / 2.0 + 0.25),
        },
        'to change': {
            'red': ceil(205 + net_red_handicap * 5 / 2.0 + 2.5),
            'blue': ceil(205 - net_red_handicap * 5 / 2.0 + 2.5),
        },
    }
