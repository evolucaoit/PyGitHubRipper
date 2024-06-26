import subprocess
import sys
import os

def main():
    # Obtém o diretório onde este script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o diretório onde queremos navegar (a raiz onde o script está)
    root_dir = script_dir

    # Comando para executar o Streamlit via linha de comando
    command = f'python3 -m streamlit run "{os.path.join(root_dir, "git-ripperv3.py")}"'

    # Executa o comando via subprocesso
    subprocess.Popen(command, cwd=root_dir, shell=True)

if __name__ == "__main__":
    main()
