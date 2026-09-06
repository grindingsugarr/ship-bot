import random


def choose_ship(users):

    if len(users) < 2:
        return None

    weighted_users = []

    for user in users:
        user_id, username, name, messages = user

        weight = max(messages, 1)

        for _ in range(weight):
            weighted_users.append(user)

    person1 = random.choice(weighted_users)
    person2 = random.choice(weighted_users)

    while person1[0] == person2[0]:
        person2 = random.choice(weighted_users)

    return person1, person2