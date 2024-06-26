import os
import subprocess

def main():
    # Obtém o diretório onde este script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o diretório onde queremos navegar (a raiz onde o script está)
    root_dir = script_dir

    # Comando para executar o Streamlit usando python3
    command = f'python3 -m streamlit run git-ripperv3.py'

    # Executa o comando via subprocesso
    subprocess.Popen(command, cwd=root_dir, shell=True)

if __name__ == "__main__":
    main()
