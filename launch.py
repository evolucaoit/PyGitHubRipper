import os
import subprocess
import sys
import platform

def main():
    # Obtém o diretório onde este script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o diretório raiz onde o script git-ripperv3.py estará
    root_dir = script_dir
    
    # Nome do script do Streamlit que será executado (use caminho absoluto se necessário)
    streamlit_script = os.path.join(root_dir, "git-ripperv3.py")
    
    try:
        # Comando para executar o Streamlit usando python
        if platform.system() == 'Windows':
            command = f'python -m streamlit run "{streamlit_script}"'
        else:
            command = f'python3 -m streamlit run "{streamlit_script}"'
        
        # Executa o comando via subprocesso
        subprocess.Popen(command, cwd=root_dir, shell=True)
    except Exception as e:
        print(f"Erro ao tentar executar o Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
