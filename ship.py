import random


def calculate_compatibility(user1, user2):

    id1, username1, name1, messages1 = user1
    id2, username2, name2, messages2 = user2

    # aktivitas grup
    activity_score = min(
        ((messages1 + messages2) / 200) * 40,
        40
    )

    # keseimbangan aktivitas
    interaction_score = random.randint(10, 30)

    # faktor chemistry kecil
    random_score = random.randint(5, 15)

    total = int(
        activity_score +
        interaction_score +
        random_score
    )

    return min(max(total, 50), 99)



def choose_ship(users):

    if len(users) < 2:
        return None

    best_pair = None
    best_score = 0


    for i in range(len(users)):

        for j in range(i + 1, len(users)):

            user1 = users[i]
            user2 = users[j]


            score = calculate_compatibility(
                user1,
                user2
            )


            if score > best_score:

                best_score = score
                best_pair = (
                    user1,
                    user2,
                    score
                )


    return best_pair
