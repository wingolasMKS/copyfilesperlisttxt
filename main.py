import os
import shutil
import fnmatch
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def copiar_arquivos_por_coringa(lista_arquivos, pasta_origem, pasta_destino, log_text):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    with open(lista_arquivos, 'r', encoding='utf-8') as arquivo_lista:
        padroes = [linha.strip() for linha in arquivo_lista.readlines()]

    total_copiados = 0
    relatorio = []
    nao_encontrados = []

    for padrao in padroes:
        encontrados = []
        for root, dirs, files in os.walk(pasta_origem):
            for arquivo in files:
                if fnmatch.fnmatch(arquivo, padrao):
                    caminho_arquivo = os.path.join(root, arquivo)
                    caminho_destino = os.path.join(pasta_destino, arquivo)

                    base, extensao = os.path.splitext(arquivo)
                    contador = 1
                    while os.path.exists(caminho_destino):
                        caminho_destino = os.path.join(pasta_destino, f"{base}_{contador}{extensao}")
                        contador += 1

                    shutil.copy2(caminho_arquivo, caminho_destino)
                    msg = f"Copiado: {caminho_arquivo} -> {caminho_destino}"
                    log_text.insert(tk.END, msg + "\n")
                    log_text.see(tk.END)
                    relatorio.append(f'"{padrao}" -> "{arquivo}"')
                    total_copiados += 1
                    encontrados.append(arquivo)

        if not encontrados:
            nao_encontrados.append(padrao)

    relatorio_path = os.path.join(pasta_destino, 'relatorio_copia.txt')
    with open(relatorio_path, 'w', encoding='utf-8') as rel:
        rel.write("RELATÓRIO DE CÓPIA:\n\n")
        for linha in relatorio:
            rel.write(linha + '\n')
        if nao_encontrados:
            rel.write("\nItens da lista NÃO encontrados:\n")
            for item in nao_encontrados:
                rel.write(f"- {item}\n")

    log_text.insert(tk.END, f"\nTotal de arquivos copiados: {total_copiados}\n")
    if nao_encontrados:
        log_text.insert(tk.END, "\nItens NÃO encontrados:\n")
        for item in nao_encontrados:
            log_text.insert(tk.END, f"- {item}\n")
    log_text.insert(tk.END, f"\nRelatório salvo em: {relatorio_path}\n")
    log_text.see(tk.END)
    messagebox.showinfo("Concluído", f"Cópia concluída! Total de arquivos copiados: {total_copiados}")

def selecionar_arquivo(entry):
    caminho = filedialog.askopenfilename(title="Selecione o arquivo de lista (.txt)", filetypes=[("Arquivos de texto", "*.txt")])
    if caminho:
        entry.delete(0, tk.END)
        entry.insert(0, caminho)

def selecionar_pasta(entry):
    caminho = filedialog.askdirectory(title="Selecione a pasta")
    if caminho:
        entry.delete(0, tk.END)
        entry.insert(0, caminho)

def iniciar_copia(entry_lista, entry_origem, entry_destino, log_text):
    lista = entry_lista.get()
    origem = entry_origem.get()
    destino = entry_destino.get()

    if not all([lista, origem, destino]):
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    log_text.delete(1.0, tk.END)
    copiar_arquivos_por_coringa(lista, origem, destino, log_text)

# Layout da interface
janela = tk.Tk()
janela.title("Copiador de Arquivos por Coringa")
janela.geometry("700x500")

# Lista
tk.Label(janela, text="Arquivo de Lista (.txt):").pack(anchor='w')
frame_lista = tk.Frame(janela)
frame_lista.pack(fill='x')
entry_lista = tk.Entry(frame_lista, width=70)
entry_lista.pack(side='left', padx=5, pady=5)
btn_lista = tk.Button(frame_lista, text="Selecionar", command=lambda: selecionar_arquivo(entry_lista))
btn_lista.pack(side='left', padx=5)

# Origem
tk.Label(janela, text="Pasta de Origem:").pack(anchor='w')
frame_origem = tk.Frame(janela)
frame_origem.pack(fill='x')
entry_origem = tk.Entry(frame_origem, width=70)
entry_origem.pack(side='left', padx=5, pady=5)
btn_origem = tk.Button(frame_origem, text="Selecionar", command=lambda: selecionar_pasta(entry_origem))
btn_origem.pack(side='left', padx=5)

# Destino
tk.Label(janela, text="Pasta de Destino:").pack(anchor='w')
frame_destino = tk.Frame(janela)
frame_destino.pack(fill='x')
entry_destino = tk.Entry(frame_destino, width=70)
entry_destino.pack(side='left', padx=5, pady=5)
btn_destino = tk.Button(frame_destino, text="Selecionar", command=lambda: selecionar_pasta(entry_destino))
btn_destino.pack(side='left', padx=5)

# Botão iniciar
btn_iniciar = tk.Button(janela, text="Iniciar Cópia", bg="#4CAF50", fg="white", height=2,
                        command=lambda: iniciar_copia(entry_lista, entry_origem, entry_destino, log_text))
btn_iniciar.pack(pady=10)

# Log
log_text = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=80, height=15)
log_text.pack(padx=10, pady=10)

janela.mainloop()
