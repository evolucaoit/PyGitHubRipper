import os
import subprocess

def main():
    # Obtém o diretório atual onde este script está sendo executado
    root_dir = os.getcwd()
    
    # Define o arquivo que desejamos executar via Streamlit
    py_file = "git-ripperv3.py"
    
    # Comando para executar o Streamlit usando python3
    command = f'python3 -m streamlit run "{os.path.join(root_dir, py_file)}"'

    # Executa o comando via subprocesso
    subprocess.Popen(command, cwd=root_dir, shell=True)

if __name__ == "__main__":
    main()
