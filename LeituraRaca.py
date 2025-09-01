import requests
from bs4 import BeautifulSoup

import json

def leituraRaca(raca):

    # URL da página a ser raspada
    url = f"http://dnd5e.wikidot.com/lineage:{raca}"

    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    content = response.content

    # Cria o objeto BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extrai todas as tags de títulos e parágrafos
    elementos = soup.find_all(['h1', 'h2', 'ul', 'li', 'p'])
    h1uns = soup.find_all(['h1'])
    startElement = soup.find(id="toc0")

    stopElement = soup.find(id="toc1")
    if h1uns.index(startElement) != len(h1uns):
        stopElement = h1uns[h1uns.index(startElement) + 1]

    escrever = False
    encontrouOutroLivro = False
    isLista = False
    print()
    print('Stop: ', stopElement)
    print('Start: ', startElement)

    textoUtil = []
    textoInutil = []
    listaDeTextos = []

    list_stack = []

    for elemento in elementos:
        if elemento == stopElement:
            escrever = False

        if elemento == startElement:
            escrever = True

        if escrever:
            # Check for the beginning of a list
            if elemento.name == 'ul':
                new_list = []

                # Check if this <ul> is a child of the current list's <li>
                is_nested = False
                if list_stack and elemento.parent.name == 'li' and elemento.parent in list_stack[-1]:
                    is_nested = True

                if is_nested:
                    list_stack[-1].append(new_list)
                    list_stack.append(new_list)
                else:
                    # It's a top-level list or a sibling list.
                    # Pop from the stack until it's empty to represent moving back to a top level.
                    while list_stack:
                        list_stack.pop()

                    textoUtil.append(new_list)
                    list_stack.append(new_list)
                continue

            # Check if the current element is a li
            if elemento.name == 'li':
                # Only add if we're in a list and the element is a direct child of a ul.
                if list_stack and elemento.parent.name == 'ul':
                    list_stack[-1].append(elemento.text.strip())
                continue

            # For non-list elements, we assume we've exited any list structure.
            while list_stack:
                list_stack.pop()

            textoUtil.append(elemento.text.strip())

    texto = [
        textoUtil,
        textoInutil,
    ]

    with open(f"JsonSoup/{raca}.json", "w") as f:
        json.dump(texto, f, indent=4)

#Ainda não há a leitura de tabelas <tr>, então a tabela de spells do
#Dragonborn não está sendo lida. O resto está ok!!
leituraRaca("dwarf")