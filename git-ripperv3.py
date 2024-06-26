import requests
from bs4 import BeautifulSoup
import subprocess
import os
import shutil
import streamlit as st

# Função para obter links de repositórios
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
        st.error(f'Erro ao acessar {url}: {e}')
        return []

# Função para clonar repositórios
def clone_repository(repo_url, download_path):
    os.makedirs(download_path, exist_ok=True)
    repo_name = repo_url.split('/')[-1]
    repo_path = os.path.join(download_path, repo_name)
    if not os.path.exists(repo_path):
        result = subprocess.run(['git', 'clone', f'{repo_url}.git', repo_path], capture_output=True, text=True)
        if result.returncode == 0:
            st.write(f'Sucesso ao clonar {repo_name}')
        else:
            st.write(f'Falha ao clonar {repo_name}: {result.stderr}')
    else:
        st.write(f'Repositório {repo_name} já existe.')

# Função para baixar repositório como zip
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
            st.write(f'Sucesso ao baixar {repo_name} como zip')
        except requests.RequestException as e:
            st.write(f'Falha ao baixar {repo_name}: {e}')
    else:
        st.write(f'Arquivo {repo_name}.zip já existe.')

# Interface do Streamlit
def main():
    st.sidebar.title('Opções')
    app_mode = st.sidebar.selectbox('Escolha a ação', ['Baixar todos os repositórios do usuário', 'Baixar repositório específico'])

    if app_mode == 'Baixar todos os repositórios do usuário':
        st.header('Baixar todos os repositórios do usuário')
        username = st.text_input('GitHub Username')
        download_path = st.text_input('Download Path', 'c:/git-rip/')
        download_option = st.radio('Escolha o formato de download', ('Clonar repositórios', 'Baixar como zip'))

        if st.button('Download Repos'):
            if username:
                repos = get_repo_links(username)
                if repos:
                    for repo in repos:
                        if download_option == 'Clonar repositórios':
                            clone_repository(repo, os.path.join(download_path, username, 'repos'))
                        else:
                            download_as_zip(repo, os.path.join(download_path, username, 'repos'))
                    st.success('Download completo!')
                else:
                    st.error('Nenhum repositório encontrado ou usuário inválido.')
            else:
                st.error('Por favor, insira um nome de usuário do GitHub.')

    elif app_mode == 'Baixar repositório específico':
        st.header('Baixar repositório específico')
        repo_url = st.text_input('URL do repositório GitHub')
        download_path = st.text_input('Download Path', 'c:/git-rip/')
        download_option = st.radio('Escolha o formato de download', ('Clonar repositório', 'Baixar como zip'))

        if st.button('Download Repo'):
            if repo_url:
                if download_option == 'Clonar repositório':
                    clone_repository(repo_url, download_path)
                else:
                    download_as_zip(repo_url, download_path)
            else:
                st.error('Por favor, insira a URL do repositório GitHub.')

if __name__ == "__main__":
    main()

# Run the app with: streamlit run github_downloader.py
