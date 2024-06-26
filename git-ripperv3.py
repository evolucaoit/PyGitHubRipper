import requests
from bs4 import BeautifulSoup
import subprocess
import os
import shutil
import streamlit as st

# Function to get repository links
def get_repo_links(username):
    url = f'https://github.com/{username}?tab=repositories'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_links = []
        for a_tag in soup.find_all('a', itemprop='name codeRepository'):
            repo_name = a_tag.get('href')
            repo_links.append(f'https://github.com{repo_name}')
        return repo_links
    except requests.RequestException as e:
        st.error(f'Error accessing {url}: {e}')
        return []

# Function to clone repositories
def clone_repository(repo_url, download_path):
    os.makedirs(download_path, exist_ok=True)
    repo_name = repo_url.split('/')[-1]
    repo_path = os.path.join(download_path, repo_name)
    if not os.path.exists(repo_path):
        result = subprocess.run(['git', 'clone', f'{repo_url}.git', repo_path], capture_output=True, text=True)
        if result.returncode == 0:
            st.write(f'Successfully cloned {repo_name}')
        else:
            st.write(f'Failed to clone {repo_name}: {result.stderr}')
    else:
        st.write(f'Repository {repo_name} already exists.')

# Function to download repository as zip
def download_as_zip(repo_url, download_path):
    os.makedirs(download_path, exist_ok=True)
    repo_name = repo_url.split('/')[-1]
    repo_path = os.path.join(download_path, f'{repo_name}.zip')
    if not os.path.exists(repo_path):
        zip_url = f'{repo_url}/archive/refs/heads/main.zip'
        try:
            response = requests.get(zip_url, stream=True)
            response.raise_for_status()
            with open(repo_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            st.write(f'Successfully downloaded {repo_name} as zip')
        except requests.RequestException as e:
            st.write(f'Failed to download {repo_name}: {e}')
    else:
        st.write(f'File {repo_name}.zip already exists.')

# Streamlit interface
def main():
    st.sidebar.title('Options')
    app_mode = st.sidebar.selectbox('Choose an action', ['Download all user repositories', 'Download specific repository'])

    if app_mode == 'Download all user repositories':
        st.header('Download all user repositories')
        username = st.text_input('GitHub Username')
        download_path = st.text_input('Download Path', 'c:/git-rip/')
        download_option = st.radio('Choose download format', ('Clone repositories', 'Download as zip'))

        if st.button('Download Repos'):
            if username:
                repos = get_repo_links(username)
                if repos:
                    for repo in repos:
                        if download_option == 'Clone repositories':
                            clone_repository(repo, os.path.join(download_path, username, 'repos'))
                        else:
                            download_as_zip(repo, os.path.join(download_path, username, 'repos'))
                    st.success('Download complete!')
                else:
                    st.error('No repositories found or invalid user.')
            else:
                st.error('Please enter a GitHub username.')

    elif app_mode == 'Download specific repository':
        st.header('Download specific repository')
        repo_url = st.text_input('GitHub repository URL')
        download_path = st.text_input('Download Path', 'c:/git-rip/')
        download_option = st.radio('Choose download format', ('Clone repository', 'Download as zip'))

        if st.button('Download Repo'):
            if repo_url:
                if download_option == 'Clone repository':
                    clone_repository(repo_url, download_path)
                else:
                    download_as_zip(repo_url, download_path)
            else:
                st.error('Please enter the GitHub repository URL.')

if __name__ == "__main__":
    main()

# Run the app with: streamlit run github_downloader.py
