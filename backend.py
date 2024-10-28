import pandas as pd
from math import sqrt

# Função para carregar o dataset CSV
def load_data():
    try:
        data = pd.read_csv('dataset.csv')
        if 'Username' not in data.columns or 'Game' not in data.columns or 'Rating' not in data.columns:
            return pd.DataFrame(columns=["Username", "Game", "Rating"])
        return data
    except FileNotFoundError:
        return pd.DataFrame(columns=["Username", "Game", "Rating"])

# Função para salvar o dataset atualizado no CSV
def save_data(data):
    data.to_csv('dataset.csv', index=False)

# Função para calcular a similaridade do cosseno manualmente
def cosine_similarity_manual(rating1, rating2):
    xy = 0
    sum_x2 = 0
    sum_y2 = 0

    for key in rating1:
        if key in rating2:
            sum_x2 += pow(rating1[key], 2)
            sum_y2 += pow(rating2[key], 2)
            xy += rating1[key] * rating2[key]

    if xy == 0:
        return 0
    else:
        return xy / (sqrt(sum_x2) * sqrt(sum_y2))

# Função para calcular os vizinhos mais próximos
def computeNearestNeighbor(username, users_ratings):
    distances = []
    current_user_ratings = users_ratings[users_ratings['Username'] == username].set_index('Game')['Rating'].to_dict()

    for user in users_ratings['Username'].unique():
        if user != username:
            other_user_ratings = users_ratings[users_ratings['Username'] == user].set_index('Game')['Rating'].to_dict()
            distance = cosine_similarity_manual(current_user_ratings, other_user_ratings)
            distances.append((distance, user))

    distances.sort(reverse=True)
    return distances

# Função para recomendar filmes
def recommend(username, users_ratings):
    similar_users = computeNearestNeighbor(username, users_ratings)
    if not similar_users:
        return []

    nearest = similar_users[1][1]

    neighbor_ratings = users_ratings[users_ratings['Username'] == nearest].set_index('Game')['Rating'].to_dict()
    user_ratings = users_ratings[users_ratings['Username'] == username].set_index('Game')['Rating'].to_dict()

    recommendations = []
    for game in neighbor_ratings:
        if game not in user_ratings:
            recommendations.append((game, neighbor_ratings[game]))

    return sorted(recommendations, key=lambda x: x[1], reverse=True)
