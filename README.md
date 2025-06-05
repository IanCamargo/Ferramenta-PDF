# 📄 Ferramenta PDF - Zucchetti

Este projeto oferece uma interface gráfica de usuário (GUI) 🖼️ desenvolvida para facilitar a manipulação de arquivos PDF, especificamente para dividir um único arquivo PDF em várias páginas individuais ✂️ e para juntar múltiplos arquivos PDF em um único documento consolidado ➕. A aplicação foi criada utilizando a biblioteca `customtkinter` para uma aparência moderna e agradável ✨, e incorpora funcionalidades como arrastar e soltar (drag-and-drop) 🖱️ para maior conveniência do usuário.

## ✨ Funcionalidades Principais

A ferramenta é organizada em duas abas principais, cada uma dedicada a uma operação específica:

### ✂️ Dividir PDF

Esta seção permite ao usuário selecionar um arquivo PDF existente e dividi-lo em arquivos separados, onde cada arquivo contém uma única página do documento original. O usuário precisa especificar o arquivo PDF de entrada 📥 e a pasta 📁 onde os arquivos resultantes serão salvos. Para organizar melhor a saída, a aplicação cria automaticamente uma subpasta dentro do diretório de saída escolhido, nomeada com base no arquivo PDF original (por exemplo, `nome_do_arquivo_paginas`), e salva todas as páginas individuais dentro dessa subpasta. A interface exibe uma barra de progresso ⏳ durante a operação de divisão, fornecendo feedback visual sobre o andamento do processo. É possível selecionar o arquivo de entrada clicando no botão "Selecionar PDF" ou simplesmente arrastando e soltando o arquivo PDF desejado na área indicada da janela.

### ➕ Juntar PDF

Nesta aba, os usuários podem combinar vários arquivos PDF em um único documento. A interface apresenta uma lista 📑 onde os arquivos PDF a serem juntados podem ser adicionados. Os usuários podem adicionar arquivos clicando no botão "Adicionar PDFs" ou arrastando e soltando múltiplos arquivos PDF diretamente na área da lista. A ordem em que os arquivos aparecem na lista determina a sequência em que serão mesclados no arquivo final. Ferramentas adicionais permitem ao usuário reorganizar a ordem dos arquivos na lista (⬆️ mover para cima, ⬇️ mover para baixo) e remover arquivos selecionados ❌. Após configurar a lista de arquivos e especificar o nome e local para o arquivo PDF resultante 💾 através do botão "Salvar Como", o usuário pode iniciar o processo de junção. Uma barra de progresso ⏳ também é exibida durante esta operação.

### 🌟 Recursos Adicionais

*   **Interface Intuitiva:** Construída com `customtkinter`, oferecendo modos claro ☀️ e escuro 🌙 e um tema padrão.
*   **Arrastar e Soltar (Drag-and-Drop):** Suporte para arrastar arquivos PDF diretamente para a aplicação, tanto na aba "Dividir" (para o arquivo de entrada) quanto na aba "Juntar" (para adicionar múltiplos arquivos à lista).
*   **Feedback Visual:** Barras de progresso ⏳ e mensagens de status 💬 informam o usuário sobre o andamento das operações e eventuais erros ⚠️.
*   **Processamento em Segundo Plano:** As operações de divisão e junção são executadas em threads separadas 🧵 para manter a interface gráfica responsiva.
*   **Consciência de DPI (Windows):** A aplicação tenta ajustar sua escala automaticamente em monitores de alta resolução no Windows 🖥️ para uma melhor experiência visual.

## 🚀 Uso

1.  Execute a aplicação conforme descrito acima.
2.  Selecione a aba correspondente à operação desejada: "Dividir PDF" ✂️ ou "Juntar PDF" ➕.
3.  **Para Dividir:**
    *   Clique em "Selecionar PDF" para escolher o arquivo a ser dividido ou arraste e solte o arquivo na área indicada.
    *   Clique em "Selecionar Pasta" para definir onde a subpasta com as páginas será criada.
    *   Clique em "Dividir PDF Agora". Aguarde a conclusão indicada pela barra de progresso e mensagem de status.
4.  **Para Juntar:**
    *   Clique em "Adicionar PDFs" para selecionar os arquivos a serem juntados ou arraste e solte os arquivos na lista.
    *   Use os botões "Mover Acima" ⬆️, "Mover Abaixo" ⬇️ e "Remover Selecionado(s)" ❌ para organizar a lista conforme necessário.
    *   Clique em "Salvar Como" 💾 para especificar o nome e o local do arquivo PDF final.
    *   Clique em "Juntar PDFs Agora". Aguarde a conclusão.

## ✍️ Autoria

Conforme mencionado no código-fonte, os direitos de criação deste programa são dedicados a Ian Camargo.
