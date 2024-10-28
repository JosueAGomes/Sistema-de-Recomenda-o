import streamlit as st
import pandas as pd
from backend import *

# Função para criar o aplicativo Streamlit
def recommend_app():
    st.title("Sistema de Recomendação Colaborativo de Filmes Nacionais")

    # Carregar o dataset de avaliações e o dataset das capas
    users_ratings = load_data()
    covers_df = pd.read_csv("movie_covers.csv")  # Carrega o CSV com capas dos filmes

    # Exibir os usuários existentes
    if not users_ratings.empty:
        username = st.selectbox("Selecione o nome de usuário:", users_ratings['Username'].unique())

        # Verificar se o usuário já avaliou algum filme
        user_ratings = users_ratings[users_ratings['Username'] == username]

        if user_ratings.empty or user_ratings['Rating'].isnull().all():
            st.write(f"O usuário {username} ainda não avaliou nenhum filme.")
            st.write("Por favor, avalie pelo menos um filme para obter recomendações.")

            filme_to_rate = st.selectbox("Selecione um filme para avaliar:", users_ratings['Game'].unique())
            rating = st.slider("Avaliação (1-5):", 1, 5)

            if st.button("Avaliar Filme"):
                new_rating = pd.DataFrame({'Username': [username], 'Game': [filme_to_rate], 'Rating': [rating]})
                users_ratings = pd.concat([users_ratings, new_rating], ignore_index=True)
                save_data(users_ratings)
                st.write(f"Avaliação para {filme_to_rate} adicionada com sucesso!")
        else:
            filme_to_rate = st.selectbox("Selecione um filme para avaliar:", users_ratings['Game'].unique())
            rating = st.slider("Avaliação (1-5):", 1, 5)

            if st.button("Avaliar Filme"):
                new_rating = pd.DataFrame({'Username': [username], 'Game': [filme_to_rate], 'Rating': [rating]})
                users_ratings = pd.concat([users_ratings, new_rating], ignore_index=True)
                save_data(users_ratings)
                st.write(f"Avaliação para {filme_to_rate} adicionada com sucesso!")

            if st.button("Recomendar Filmes"):
                st.write(f"Gerando recomendações para {username}...")
                recommendations = recommend(username, users_ratings)

                if recommendations:
                    st.write(f"Recomendações para {username}:")
                    for recommendation in recommendations:
                        movie_name = recommendation[0]
                        cover_url = covers_df[covers_df['Movie'] == movie_name]['Cover'].values[0]
                        st.image(cover_url, caption=movie_name)
                        st.write(f"Pontuação: {recommendation[1]}")
                else:
                    st.write(f"Nenhuma recomendação disponível para {username}.")

    # Adicionar um novo usuário
    new_user = st.text_input("Digite o nome de um novo usuário:")

    if st.button("Adicionar Novo Usuário"):
        if new_user not in users_ratings['Username'].unique():
            users_ratings = pd.concat(
                [users_ratings, pd.DataFrame({'Username': [new_user], 'Game': [""], 'Rating': [""]})],
                ignore_index=True)
            save_data(users_ratings)
            st.write(f"Novo usuário {new_user} adicionado com sucesso! Recarregue a página para vê-lo na lista")
        else:
            st.write(f"O usuário {new_user} já existe!")


def main():
    recommend_app()


if __name__ == "__main__":
    main()
