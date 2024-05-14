import streamlit as st
from langchain import OpenAI
from instagram_private_api import Client, ClientCompatPatch
import random

def login_instagram(username, password):
    try:
        api = Client(username, password)
        return api
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None

def get_followers(api, user_id):
    followers = []
    try:
        rank_token = Client.generate_uuid()
        results = api.user_followers(user_id, rank_token=rank_token)
        followers.extend(results.get('users', []))
        while results.get('next_max_id'):
            results = api.user_followers(user_id, rank_token=rank_token, max_id=results.get('next_max_id'))
            followers.extend(results.get('users', []))
    except Exception as e:
        st.error(f"Error fetching followers: {e}")
    return followers

def choose_winner(followers):
    return random.choice(followers) if followers else None

def main():
    st.title('Instagram Giveaway Picker')

    username = st.text_input('Instagram Username')
    password = st.text_input('Instagram Password', type='password')

    if st.button('Fetch Followers and Pick Winner'):
        if not username or not password:
            st.error('Please enter both username and password')
            return
       
        api = login_instagram(username, password)
        if not api:
            return

        user_info = api.current_user()
        user_id = user_info['user']['pk']

        followers = get_followers(api, user_id)
        if not followers:
            st.error('No followers found or error fetching followers')
            return

        winner = choose_winner(followers)
        if winner:
            st.success(f"The winner is: {winner['username']}")
        else:
            st.error('Could not choose a winner')

if __name__ == "__main__":
    main()

