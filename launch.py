import os
import subprocess

def main():
    # Obtém o diretório onde este script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o diretório onde queremos navegar (a raiz onde o script está)
    root_dir = script_dir

    # Abre o prompt de comando do Windows na pasta específica (opcional, pode não ser necessário)
    # subprocess.Popen(['cmd', '/K', 'cd', '/D', root_dir])

    # Executa o arquivo git-ripperv3.py usando python -m streamlit run <arquivo>
    selected_file = os.path.join(root_dir, 'git-ripperv3.py')
    command = f'python -m streamlit run "{selected_file}"'
    subprocess.Popen(command, cwd=root_dir, shell=True)

if __name__ == "__main__":
    main()
