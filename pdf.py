import customtkinter
from tkinter import filedialog, messagebox, Listbox, END, MULTIPLE, ANCHOR, Scrollbar
from pypdf import PdfReader, PdfWriter
import os
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES
import platform # Adicionado para checar o SO
import ctypes   # Adicionado para interagir com a API do Windows

# --- CONFIGURAÇÃO DE DPI AWARENESS (SOMENTE PARA WINDOWS) ---
# Isso deve vir ANTES da inicialização da janela principal do Tkinter/CustomTkinter
if platform.system() == "Windows":
    try:
        # Tenta definir DPI Awareness por monitor (V2), mais moderno (Windows 10 1703+)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        print("DPI Awareness set to Per-Monitor V2.")
    except AttributeError:
        try:
            # Fallback para System DPI Awareness (Windows Vista+)
            ctypes.windll.user32.SetProcessDPIAware()
            print("DPI Awareness set to System Aware.")
        except AttributeError:
            print("Could not set DPI awareness (ctypes issue or not Windows).")
    except Exception as e:
        print(f"Error setting DPI awareness: {e}")
# --- FIM DA CONFIGURAÇÃO DE DPI AWARENESS ---

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# --- FUNÇÕES DE LÓGICA (DIVIDIR E JUNTAR) ---

def dividir_pdf_em_paginas_gui(caminho_pdf_entrada, pasta_saida, status_callback, progress_callback=None, done_callback=None):
    try:
        if not caminho_pdf_entrada:
            status_callback("Erro: Nenhum arquivo PDF de entrada selecionado.")
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
            if done_callback: done_callback(False); return
        if not pasta_saida:
            status_callback("Erro: Nenhuma pasta de saída selecionada.")
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de saída.")
            if done_callback: done_callback(False); return

        leitor = PdfReader(caminho_pdf_entrada)
        num_paginas = len(leitor.pages)

        # status_callback(f"Dividindo '{os.path.basename(caminho_pdf_entrada)}' em {num_paginas} páginas...")

        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
            status_callback(f"Pasta '{os.path.basename(pasta_saida)}' criada.")

        for i in range(num_paginas):
            escritor_pagina = PdfWriter()
            escritor_pagina.add_page(leitor.pages[i])
            nome_arquivo_saida = os.path.join(pasta_saida, f"pagina_{i + 1}.pdf")
            with open(nome_arquivo_saida, "wb") as f_saida:
                escritor_pagina.write(f_saida)
            escritor_pagina.close()
            if progress_callback:
                progress_callback(i + 1, num_paginas)
        status_callback(f"Divisão Concluída.") # Mensagem final mais concisa

        # status_callback(f"PDF dividido com sucesso em {num_paginas} páginas na pasta '{os.path.basename(pasta_saida)}'.")

        messagebox.showinfo("Sucesso", f"PDF Dividido com Sucesso!")
        if done_callback: done_callback(True)
    except FileNotFoundError:
        status_callback(f"Erro: O arquivo '{os.path.basename(caminho_pdf_entrada)}' não foi encontrado.")
        messagebox.showerror("Erro", f"O arquivo '{caminho_pdf_entrada}' não foi encontrado.")
        if done_callback: done_callback(False)
    except Exception as e:
        status_callback(f"Ocorreu um erro ao dividir: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")
        if done_callback: done_callback(False)

def juntar_pdfs_gui(lista_arquivos_entrada, caminho_pdf_saida, status_callback, progress_callback=None, done_callback=None):
    if not lista_arquivos_entrada:
        status_callback("Erro: Nenhum arquivo PDF selecionado para juntar.")
        messagebox.showerror("Erro", "Por favor, adicione arquivos PDF à lista.")
        if done_callback: done_callback(False); return
    if not caminho_pdf_saida:
        status_callback("Erro: Nenhum arquivo de saída selecionado.")
        messagebox.showerror("Erro", "Por favor, especifique um nome para o arquivo PDF final.")
        if done_callback: done_callback(False); return

    writer = PdfWriter()
    try:
        status_callback(f"Iniciando junção de {len(lista_arquivos_entrada)} arquivos...")
        for i, pdf_path in enumerate(lista_arquivos_entrada):
            status_callback(f"Adicionando ({i+1}/{len(lista_arquivos_entrada)}): {os.path.basename(pdf_path)}")
            writer.append(pdf_path)
            if progress_callback:
                progress_callback(i + 1, len(lista_arquivos_entrada))

        status_callback(f"Salvando PDF juntado como: {os.path.basename(caminho_pdf_saida)}")
        with open(caminho_pdf_saida, "wb") as f_out:
            writer.write(f_out)
        writer.close()
        status_callback(f"PDFs juntados com sucesso em '{os.path.basename(caminho_pdf_saida)}'.")
        messagebox.showinfo("Sucesso", f"PDFs juntados com sucesso!")
        if done_callback: done_callback(True)
    except Exception as e:
        status_callback(f"Ocorreu um erro ao juntar os PDFs: {e}")
        messagebox.showerror("Erro de Junção", f"Ocorreu um erro: {e}")
        if 'writer' in locals():
            try: writer.close()
            except Exception as close_exc:
                print(f"Erro ao fechar o PdfWriter durante o tratamento de exceção: {close_exc}")
        if done_callback: done_callback(False)


# --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---

janela_raiz_dnd = TkinterDnD.Tk()
janela_raiz_dnd.title("Ferramenta PDF - Zucchetti")
janela_raiz_dnd.geometry("700x600")
janela_raiz_dnd.minsize(600, 500)

app_frame = customtkinter.CTkFrame(master=janela_raiz_dnd, fg_color=("gray92", "gray14"))
app_frame.pack(expand=True, fill="both")

texto_autoria = "Este programa dedica seus direitos de criação a Ian Camargo."
label_dedicatoria = customtkinter.CTkLabel(app_frame, text=texto_autoria, font=customtkinter.CTkFont(size=10, slant="italic"))
label_dedicatoria.pack(side="top", pady=(10, 0), padx=10, fill="x")

tabview = customtkinter.CTkTabview(app_frame) # Master é app_frame
tabview.pack(padx=10, pady=10, expand=True, fill="both")

tab_dividir = tabview.add("Dividir PDF")
tab_juntar = tabview.add("Juntar PDF")

status_var = customtkinter.StringVar(value="Pronto. Arraste arquivos PDF aqui ou use os botões.")

# --- ABA: DIVIDIR PDF ---
entrada_pdf_dividir_var = customtkinter.StringVar()
saida_pasta_dividir_var = customtkinter.StringVar()
progress_dividir_var = customtkinter.DoubleVar(value=0.0)

def on_drop_dividir(event):
    try:
        arquivos_soltos = janela_raiz_dnd.tk.splitlist(event.data)
        if arquivos_soltos:
            primeiro_arquivo = arquivos_soltos[0]
            if primeiro_arquivo.lower().endswith(".pdf"):
                entrada_pdf_dividir_var.set(primeiro_arquivo)
                status_var.set(f"Dividir (arrastado): {os.path.basename(primeiro_arquivo)}")
                progress_dividir_var.set(0.0)
            else:
                status_var.set("Erro: Por favor, arraste apenas arquivos PDF.")
                messagebox.showwarning("Arquivo Inválido", "Por favor, solte apenas arquivos PDF.")
        else:
            status_var.set("Nenhum arquivo detectado no arraste.")
    except Exception as e:
        print(f"Erro no drop dividir: {e}")
        status_var.set("Erro ao processar arquivos arrastados.")


def ui_selecionar_arquivo_pdf_dividir():
    caminho = filedialog.askopenfilename(title="Selecione o PDF para dividir", filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
    if caminho:
        entrada_pdf_dividir_var.set(caminho)
        status_var.set(f"Dividir: {os.path.basename(caminho)}") # Restaurado para dar feedback imediato
        progress_dividir_var.set(0.0)

def ui_selecionar_pasta_saida_dividir():
    caminho = filedialog.askdirectory(title="Selecione a pasta de destino das páginas")
    if caminho:
        saida_pasta_dividir_var.set(caminho)
        status_var.set(f"Pasta de saída para divisão: {os.path.basename(caminho)}") # Feedback

def atualizar_progresso_dividir(atual, total):
    progresso = float(atual) / total
    progress_dividir_var.set(progresso)
    # janela_raiz_dnd.update_idletasks() # Removido, geralmente não necessário com threads

def callback_done_dividir(success):
    botao_executar_dividir.configure(state="normal")
    if not success:
        progress_dividir_var.set(0.0)
    # else: # Se sucesso, a mensagem já foi mostrada pela função lógica
    #     status_var.set("Pronto.")

def iniciar_divisao_thread():
    pdf_in = entrada_pdf_dividir_var.get()
    pasta_out_base = saida_pasta_dividir_var.get()
    if not pdf_in: messagebox.showerror("Entrada Inválida", "Por favor, selecione um arquivo PDF."); return
    if not pasta_out_base: messagebox.showerror("Entrada Inválida", "Por favor, selecione uma pasta de saída."); return
    nome_base_arquivo = os.path.splitext(os.path.basename(pdf_in))[0]
    pasta_out_especifica = os.path.join(pasta_out_base, f"{nome_base_arquivo}_paginas")
    botao_executar_dividir.configure(state="disabled")
    progress_dividir_var.set(0.0)
    status_var.set("Dividindo... Por favor, aguarde.")
    thread = threading.Thread(target=dividir_pdf_em_paginas_gui, args=(
        pdf_in, pasta_out_especifica, lambda msg: status_var.set(msg),
        atualizar_progresso_dividir, callback_done_dividir
    ))
    thread.start()

frame_widgets_dividir = customtkinter.CTkFrame(tab_dividir, fg_color="transparent")
frame_widgets_dividir.pack(pady=10, padx=10, fill="x")

frame_widgets_dividir.drop_target_register(DND_FILES)
frame_widgets_dividir.dnd_bind('<<Drop>>', on_drop_dividir)

customtkinter.CTkLabel(frame_widgets_dividir, text="Arquivo PDF (ou arraste aqui):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_pdf_dividir = customtkinter.CTkEntry(frame_widgets_dividir, textvariable=entrada_pdf_dividir_var, width=350)
entry_pdf_dividir.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
customtkinter.CTkButton(frame_widgets_dividir, text="Selecionar PDF", command=ui_selecionar_arquivo_pdf_dividir).grid(row=0, column=2, padx=5, pady=5)
customtkinter.CTkLabel(frame_widgets_dividir, text="Salvar Páginas Em:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_pasta_dividir = customtkinter.CTkEntry(frame_widgets_dividir, textvariable=saida_pasta_dividir_var, width=350)
entry_pasta_dividir.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
customtkinter.CTkButton(frame_widgets_dividir, text="Selecionar Pasta", command=ui_selecionar_pasta_saida_dividir).grid(row=1, column=2, padx=5, pady=5)
frame_widgets_dividir.grid_columnconfigure(1, weight=1)
progressbar_dividir = customtkinter.CTkProgressBar(tab_dividir, variable=progress_dividir_var)
progressbar_dividir.set(0)
progressbar_dividir.pack(pady=10, padx=10, fill="x")
botao_executar_dividir = customtkinter.CTkButton(tab_dividir, text="Dividir PDF Agora", command=iniciar_divisao_thread, height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
botao_executar_dividir.pack(pady=20, padx=10, fill="x")


# --- ABA: JUNTAR PDFS ---
saida_pdf_juntar_var = customtkinter.StringVar()
lista_arquivos_para_juntar = []
progress_juntar_var = customtkinter.DoubleVar(value=0.0)

def on_drop_juntar(event):
    try:
        arquivos_soltos = janela_raiz_dnd.tk.splitlist(event.data)
        novos_adicionados = 0
        if arquivos_soltos:
            for arq_path in arquivos_soltos:
                if arq_path.lower().endswith(".pdf"):
                    if arq_path not in lista_arquivos_para_juntar:
                        lista_arquivos_para_juntar.append(arq_path)
                        listbox_juntar_arquivos.insert(END, os.path.basename(arq_path))
                        novos_adicionados +=1
                else:
                    status_var.set(f"Ignorado (não é PDF): {os.path.basename(arq_path)}")
            if novos_adicionados > 0:
                status_var.set(f"{novos_adicionados} PDF(s) arrastado(s) e adicionado(s). Total: {len(lista_arquivos_para_juntar)}")
                progress_juntar_var.set(0.0) # Resetar progresso se a lista mudar
            elif not any(f.lower().endswith(".pdf") for f in arquivos_soltos):
                 messagebox.showwarning("Arquivos Inválidos", "Apenas arquivos PDF podem ser arrastados para esta lista.")
        else:
            status_var.set("Nenhum arquivo detectado no arraste para juntar.")
    except Exception as e:
        print(f"Erro no drop juntar: {e}")
        status_var.set("Erro ao processar arquivos arrastados para juntar.")

frame_principal_juntar = customtkinter.CTkFrame(tab_juntar, fg_color="transparent")
frame_principal_juntar.pack(expand=True, fill="both", padx=10, pady=10)
frame_principal_juntar.grid_columnconfigure(0, weight=1)
frame_principal_juntar.grid_rowconfigure(0, weight=1) # Alterado para dar peso à linha da listbox

frame_listbox_container = customtkinter.CTkFrame(frame_principal_juntar) # bg explícito removido, CustomTkinter cuida disso
frame_listbox_container.grid(row=0, column=0, rowspan=5, padx=(0,5), pady=5, sticky="nsew")
frame_listbox_container.grid_rowconfigure(0, weight=1)
frame_listbox_container.grid_columnconfigure(0, weight=1)

frame_listbox_container.drop_target_register(DND_FILES)
frame_listbox_container.dnd_bind('<<Drop>>', on_drop_juntar)

# Usando CTkListbox se disponível, ou mantendo Listbox padrão
try:
    from CTkListbox import CTkListbox # Tenta importar
    listbox_juntar_arquivos = CTkListbox(frame_listbox_container, select_mode="multiple")
    listbox_juntar_arquivos.pack(side="left", fill="both", expand=True, padx=(2,0), pady=2)
    # CTkListbox não usa scrollbar externo dessa forma, geralmente é integrado ou configurado diferentemente
    # Se estiver usando CTkListbox, pode ser necessário ajustar ou remover o scrollbar_juntar_arquivos
    # Por ora, vamos manter o scrollbar do CustomTkinter, pode funcionar ou precisar de ajuste
    scrollbar_juntar_arquivos = customtkinter.CTkScrollbar(frame_listbox_container, command=listbox_juntar_arquivos.yview)
    # scrollbar_juntar_arquivos.pack(side="right", fill="y", pady=2, padx=(0,2)) # Descomente se necessário e ajuste
    # listbox_juntar_arquivos.configure(yscrollcommand=scrollbar_juntar_arquivos.set) # Descomente se necessário
    # Nota: a integração do scrollbar com CTkListbox pode variar. Consulte a doc do CTkListbox.
    # Se CTkListbox não for usado, o Listbox original será.
    # As funções de manipulação (insert, delete, get, curselection) precisam ser adaptadas para CTkListbox
    # Ex: listbox_juntar_arquivos.insert(END, ...) -> listbox_juntar_arquivos.insert("END", ...)
    # Ex: listbox_juntar_arquivos.curselection() -> listbox_juntar_arquivos.get_selected_indices() (ou similar)
    # ESTA PARTE REQUER ATENÇÃO ESPECIAL SE CTkListbox FOR REALMENTE USADO E TIVER API DIFERENTE
    # Por segurança e simplicidade, vamos reverter para o Listbox padrão que já funciona
    # Se quiser usar CTkListbox, precisará adaptar as funções de manipulação da lista.
    raise ImportError # Forçar fallback para Listbox padrão por enquanto para manter a funcionalidade original

except ImportError:
    print("CTkListbox não encontrado, usando tkinter.Listbox padrão.")
    listbox_juntar_arquivos = Listbox(frame_listbox_container, selectmode=MULTIPLE, bg="#2B2B2B", fg="white", borderwidth=0, highlightthickness=0, activestyle="none", font=("Arial", 12))
    listbox_juntar_arquivos.pack(side="left", fill="both", expand=True, padx=(2,0), pady=2)
    scrollbar_juntar_arquivos = customtkinter.CTkScrollbar(frame_listbox_container, command=listbox_juntar_arquivos.yview)
    scrollbar_juntar_arquivos.pack(side="right", fill="y", pady=2, padx=(0,2))
    listbox_juntar_arquivos.configure(yscrollcommand=scrollbar_juntar_arquivos.set)


frame_botoes_lista = customtkinter.CTkFrame(frame_principal_juntar, fg_color="transparent")
frame_botoes_lista.grid(row=0, column=1, rowspan=5, padx=(5,0), pady=5, sticky="ns")

def ui_adicionar_arquivos_juntar():
    arquivos = filedialog.askopenfilenames(title="Selecione PDF para juntar", filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
    if arquivos:
        novos_adicionados = 0
        for arq_path in arquivos:
            if arq_path not in lista_arquivos_para_juntar:
                lista_arquivos_para_juntar.append(arq_path)
                listbox_juntar_arquivos.insert(END, os.path.basename(arq_path))
                novos_adicionados +=1
        if novos_adicionados > 0:
            status_var.set(f"{len(lista_arquivos_para_juntar)} arquivo(s) na lista para juntar.")
        progress_juntar_var.set(0.0)

def ui_remover_selecionados_juntar():
    # Adaptar para CTkListbox se usado: listbox_juntar_arquivos.get_selected_indices()
    selecionados_indices = list(listbox_juntar_arquivos.curselection())
    selecionados_indices.sort(reverse=True)
    if not selecionados_indices: messagebox.showinfo("Info", "Nenhum arquivo selecionado para remover."); return
    for index in selecionados_indices:
        listbox_juntar_arquivos.delete(index) # Adaptar para CTkListbox: listbox_juntar_arquivos.delete(index)
        del lista_arquivos_para_juntar[index]
    status_var.set(f"{len(lista_arquivos_para_juntar)} arquivo(s) na lista para juntar.")

def ui_limpar_lista_juntar():
    if messagebox.askyesno("Limpar Lista", "Tem certeza que deseja remover todos os arquivos da lista?"):
        lista_arquivos_para_juntar.clear()
        listbox_juntar_arquivos.delete(0, END) # Adaptar para CTkListbox: listbox_juntar_arquivos.delete_all() ou similar
        status_var.set("Lista de arquivos para juntar está vazia.")
        progress_juntar_var.set(0.0)

def mover_item(direcao):
    # Adaptar para CTkListbox se usado
    selecionados = listbox_juntar_arquivos.curselection()
    if not selecionados: messagebox.showinfo("Info", "Selecione um item para mover."); return
    if len(selecionados) > 1: messagebox.showinfo("Info", "Selecione apenas um item para mover."); return
    index = selecionados[0]
    
    # Para CTkListbox, listbox_juntar_arquivos.size() seria len(listbox_juntar_arquivos.get_all()) ou similar
    if (direcao == -1 and index == 0) or \
       (direcao == 1 and index == listbox_juntar_arquivos.size() - 1):
        return

    novo_index = index + direcao
    item_path = lista_arquivos_para_juntar.pop(index)
    lista_arquivos_para_juntar.insert(novo_index, item_path)
    
    item_display = listbox_juntar_arquivos.get(index) # Adaptar para CTkListbox: listbox_juntar_arquivos.get_item(index)
    listbox_juntar_arquivos.delete(index)
    listbox_juntar_arquivos.insert(novo_index, item_display)
    
    listbox_juntar_arquivos.selection_clear(0, END) # Adaptar para CTkListbox: listbox_juntar_arquivos.deselect_all()
    listbox_juntar_arquivos.selection_set(novo_index) # Adaptar para CTkListbox: listbox_juntar_arquivos.select(novo_index)
    listbox_juntar_arquivos.activate(novo_index) # Manter ou verificar equivalente CTkListbox

botao_adicionar_juntar = customtkinter.CTkButton(frame_botoes_lista, text="Adicionar Arquivo(s)", command=ui_adicionar_arquivos_juntar)
botao_adicionar_juntar.pack(pady=5, fill="x")
botao_remover_juntar = customtkinter.CTkButton(frame_botoes_lista, text="Remover Selecionado", command=ui_remover_selecionados_juntar)
botao_remover_juntar.pack(pady=5, fill="x")
botao_subir_juntar = customtkinter.CTkButton(frame_botoes_lista, text="Mover Acima", command=lambda: mover_item(-1))
botao_subir_juntar.pack(pady=5, fill="x")
botao_descer_juntar = customtkinter.CTkButton(frame_botoes_lista, text="Mover Abaixo", command=lambda: mover_item(1))
botao_descer_juntar.pack(pady=5, fill="x")
botao_limpar_juntar = customtkinter.CTkButton(frame_botoes_lista, text="Limpar Lista", command=ui_limpar_lista_juntar, fg_color="#D2042D", hover_color="#AA0324")
botao_limpar_juntar.pack(pady=5, fill="x")

frame_saida_juntar = customtkinter.CTkFrame(frame_principal_juntar, fg_color="transparent")
frame_saida_juntar.grid(row=5, column=0, columnspan=2, pady=(10,0), padx=0, sticky="ew")
customtkinter.CTkLabel(frame_saida_juntar, text="Salvar PDF Juntado Como:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_saida_juntar = customtkinter.CTkEntry(frame_saida_juntar, textvariable=saida_pdf_juntar_var, width=350)
entry_saida_juntar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
frame_saida_juntar.grid_columnconfigure(1, weight=1)

def ui_selecionar_saida_pdf_juntar():
    caminho = filedialog.asksaveasfilename(title="Salvar PDF juntado como...", defaultextension=".pdf", filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
    if caminho:
        saida_pdf_juntar_var.set(caminho)
        status_var.set(f"PDF juntado será salvo como: {os.path.basename(caminho)}")

customtkinter.CTkButton(frame_saida_juntar, text="Salvar Como...", command=ui_selecionar_saida_pdf_juntar).grid(row=0, column=2, padx=5, pady=5)
progressbar_juntar = customtkinter.CTkProgressBar(frame_principal_juntar, variable=progress_juntar_var)
progressbar_juntar.set(0)
progressbar_juntar.grid(row=6, column=0, columnspan=2, pady=10, padx=0, sticky="ew")

def atualizar_progresso_juntar(atual, total):
    progresso = float(atual) / total
    progress_juntar_var.set(progresso)

def callback_done_juntar(success):
    botao_executar_juntar.configure(state="normal")
    if not success:
        progress_juntar_var.set(0.0)
    # else:
    #     status_var.set("Pronto.")


def iniciar_juncao_thread():
    pdf_out = saida_pdf_juntar_var.get()
    if not lista_arquivos_para_juntar: messagebox.showerror("Lista Vazia", "Adicione arquivos PDF à lista para juntar."); return
    if not pdf_out: messagebox.showerror("Saída Inválida", "Por favor, especifique um nome para o arquivo PDF final."); return
    botao_executar_juntar.configure(state="disabled")
    progress_juntar_var.set(0.0)
    status_var.set("Juntando... Por favor, aguarde.")
    lista_copia = list(lista_arquivos_para_juntar) # Criar cópia para a thread
    thread = threading.Thread(target=juntar_pdfs_gui, args=(
        lista_copia, pdf_out, lambda msg: status_var.set(msg),
        atualizar_progresso_juntar, callback_done_juntar
    ))
    thread.start()

botao_executar_juntar = customtkinter.CTkButton(frame_principal_juntar, text="Juntar PDF Agora", command=iniciar_juncao_thread, height=40, font=customtkinter.CTkFont(size=14, weight="bold"))
botao_executar_juntar.grid(row=7, column=0, columnspan=2, pady=20, padx=0, sticky="ew")

# --- RODAPÉ (LABEL DE STATUS) ---
label_status = customtkinter.CTkLabel(app_frame, textvariable=status_var, wraplength=680, justify="left") # Aumentar wraplength se necessário
label_status.pack(side="bottom", pady=(5, 10), padx=10, fill="x")

# Iniciar a interface.
janela_raiz_dnd.mainloop()