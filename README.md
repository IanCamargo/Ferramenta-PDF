# 📄 Ferramenta PDF - Zucchetti

Este projeto oferece uma interface gráfica de usuário (GUI) 🖼️ desenvolvida para facilitar a manipulação de arquivos PDF. As funcionalidades incluem separar um único arquivo PDF em várias páginas individuais ✂️, extrair um conjunto específico de páginas para um novo arquivo PDF único 📜, e juntar múltiplos arquivos PDF em um único documento consolidado ➕. A aplicação foi criada utilizando a biblioteca `customtkinter` para uma aparência moderna e agradável ✨, e incorpora funcionalidades como arrastar e soltar (drag-and-drop) 🖱️ para maior conveniência do usuário.

## ✨ Funcionalidades Principais

A ferramenta é organizada em três abas principais, cada uma dedicada a uma operação específica:

1.  **✂️ Separar PDF (Pág. Indiv.)**
    * Permite ao usuário selecionar um arquivo PDF de entrada 📥.
    * O usuário deve especificar a pasta de saída 📁 onde os arquivos resultantes serão salvos.
    * É possível definir um intervalo de páginas para separação (ex: "1-3, 5, 8-10"). Se o campo de intervalo for deixado em branco, todas as páginas do PDF serão separadas.
    * Cada página selecionada (ou todas) será salva como um arquivo PDF individual.
    * Para organizar a saída, a aplicação cria automaticamente uma subpasta dentro do diretório de saída escolhido, nomeada com base no arquivo PDF original (ex: `nome_do_arquivo_paginas_separadas`), e salva todas as páginas individuais dentro dessa subpasta.
    * Suporte para arrastar e soltar 🖱️ o arquivo PDF de entrada na área designada.
    * Uma barra de progresso ⏳ e mensagens de status 💬 informam sobre o andamento.

2.  **📜 Extrair Páginas Agrupadas**
    * Permite ao usuário selecionar um arquivo PDF de entrada 📥.
    * O usuário **obrigatoriamente** deve fornecer um intervalo de páginas a serem extraídas (ex: "1-5, 8, 10-12") 📝. Este intervalo define o conteúdo do novo PDF.
    * As páginas especificadas são extraídas do PDF original e combinadas em um **único novo arquivo PDF**.
    * O usuário precisa selecionar a pasta de saída 📁 onde este novo PDF consolidado será salvo.
    * O nome do arquivo de saída é gerado automaticamente com base no nome do arquivo original e no intervalo de páginas (ex: `nome_do_arquivo_extracao_1-5_8_10-12.pdf`), com um contador para evitar sobrescrever arquivos existentes.
    * Suporte para arrastar e soltar 🖱️ o arquivo PDF de entrada.
    * Feedback visual através de barra de progresso ⏳ e mensagens de status 💬.

3.  **➕ Juntar PDF**
    * Nesta aba, os usuários podem combinar vários arquivos PDF em um único documento.
    * A interface apresenta uma lista 📑 onde os arquivos PDF a serem juntados podem ser adicionados clicando no botão "Adicionar" ou arrastando e soltando múltiplos arquivos PDF diretamente na área da lista.
    * A ordem dos arquivos na lista determina a sequência em que serão mesclados.
    * Ferramentas permitem reorganizar a ordem (⬆️ Mover Acima, ⬇️ Mover Abaixo) e remover arquivos selecionados ❌ ou limpar toda a lista 🗑️.
    * O usuário especifica o nome e local para o arquivo PDF resultante 💾 através do botão "Salvar Como...".
    * Uma barra de progresso ⏳ é exibida durante a operação de junção.

## 🌟 Recursos Adicionais

* **Interface Intuitiva:** Construída com `customtkinter`, oferecendo modos claro ☀️ e escuro 🌙 e um tema padrão ("dark-blue").
* **Arrastar e Soltar (Drag-and-Drop):** Suporte para arrastar arquivos PDF diretamente para a aplicação nas abas "Separar" e "Extrair" (para o arquivo de entrada) e na aba "Juntar" (para adicionar múltiplos arquivos à lista).
* **Feedback Visual:** Barras de progresso ⏳ e mensagens de status 💬 informam o usuário sobre o andamento das operações e eventuais erros ⚠️.
* **Processamento em Segundo Plano:** Operações de manipulação de PDF são executadas em threads separadas 🧵 para manter a interface gráfica responsiva.
* **Validação de Entrada:** Verificações são feitas para entradas como intervalos de páginas e seleção de arquivos/pastas, com mensagens de erro informativas ❗.
* **Limpeza de Campos:** Cada aba possui um botão "Limpar Campos" para resetar facilmente as entradas.
* **Consciência de DPI (Windows):** A aplicação tenta ajustar sua escala automaticamente em monitores de alta resolução no Windows 🖥️ para uma melhor experiência visual.
* **Nomenclatura Inteligente de Arquivos:** Arquivos de saída são nomeados de forma descritiva e evitam sobrescritas acidentais.

## 🚀 Uso

1.  Execute a aplicação.
2.  Selecione a aba correspondente à operação desejada: "Separar PDF (Pág. Indiv.)" ✂️, "Extrair Páginas Agrupadas" 📜, ou "Juntar PDF" ➕.

    * **Para Separar PDF (Pág. Indiv.):**
        1.  Clique em "Selecionar PDF" ou arraste e solte o arquivo PDF na área "Arquivo PDF".
        2.  Opcionalmente, insira o intervalo de páginas (ex: "1-3, 5"). Deixe em branco para todas as páginas.
        3.  Clique em "Selecionar Pasta" para definir onde a subpasta com as páginas separadas será criada.
        4.  Clique em "Separar em Páginas Individuais". Aguarde a conclusão.

    * **Para Extrair Páginas Agrupadas:**
        1.  Clique em "Selecionar PDF" ou arraste e solte o arquivo PDF na área "Arquivo PDF".
        2.  **Insira o intervalo de páginas OBRIGATÓRIO** (ex: "1-5, 8, 10-12") no campo "Páginas a Agrupar".
        3.  Clique em "Selecionar Pasta" para escolher onde o novo PDF agrupado será salvo.
        4.  Clique em "Extrair Páginas para Um Novo PDF". Aguarde a conclusão.

    * **Para Juntar PDF:**
        1.  Clique em "Adicionar" para selecionar os arquivos PDF ou arraste e solte-os na lista.
        2.  Use os botões "Mover Acima" ⬆️, "Mover Abaixo" ⬇️, e "Remover" ❌ para organizar a lista.
        3.  Clique em "Salvar Como..." 💾 para especificar o nome e o local do arquivo PDF final.
        4.  Clique em "Juntar PDF Agora". Aguarde a conclusão.

## ✍️ Autoria

Conforme mencionado no código-fonte: `Este programa dedica seus direitos de criação a Ian Camargo.`
