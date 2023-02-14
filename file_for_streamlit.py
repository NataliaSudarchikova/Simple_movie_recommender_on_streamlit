import streamlit as st
import pandas as pd
import seaborn as sns

N_MOVIES = 10
#NO_MOVIE_SELECTED  = "Select a Movie"

st.title("Movie Reccomender: item based")

movies = pd.read_csv("C:/Users/m218101/Desktop/WBS_Coding_school/Course/Recommerder_systems/movies/reccomender_on_streamlit/movies.csv")
ratings = pd.read_csv("C:/Users/m218101/Desktop/WBS_Coding_school/Course/Recommerder_systems/movies/reccomender_on_streamlit/ratings.csv")


def item_based_recom(n,chosen_movie_title):
    chosen_movie_id = int(movies.query("title == @chosen_movie_title").movieId)
    cross_table = pd.pivot_table(data=ratings,values='rating',columns='movieId',index='userId')
    corr_table=pd.DataFrame({})
    corr_table["cross_corr"] = cross_table.corrwith(cross_table[chosen_movie_id]).dropna().drop(chosen_movie_id)  
    corr_table_view = corr_table.merge(movies,on="movieId")[["title","genres","cross_corr","movieId"]]

    rating2 = ratings.groupby("movieId").agg(rate_count = ("rating","count"))
    final_table = (
            corr_table_view
            .merge(rating2,on="movieId")
            .drop(columns="movieId")
            .query("rate_count >= 100")
            .nlargest(n,"cross_corr")
        )
  
    return final_table

#Visualize result

with st.container():
    all_movies = list(movies.title)
#    all_movies.insert(0, NO_MOVIE_SELECTED)
    st.header("Tell me a Movie that you like")
    title = st.selectbox("", all_movies)
#    if title != NO_MOVIE_SELECTED:
    similar_movie_list = item_based_recom(N_MOVIES*2, title)
    msg= f" :heart: Because you loved {title}, you might enjoy these movies :heart:"
#        fail_msg = f"Sorry my Database is teeny-tiny .. There is no Movies Similar enough to {title} :pleading_face: "
#        visualize_result(similar_movie_list, msg, fail_msg)
    (similar_movie_list,msg)

st.markdown('&nbsp;')




