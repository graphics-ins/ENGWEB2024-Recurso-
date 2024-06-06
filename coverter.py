import json
import ast

json_file_name = 'dataset.json'

# Definir os campos que precisam de conversão de string para lista
list_fields = ["genres", "characters", "awards", "ratingsByStars", "setting"]

with open(json_file_name, 'r') as file:
    books_data = json.load(file)

def split_book_id(book_id):
    if '.' in book_id:
        return book_id.split('.', 1)
    elif '-' in book_id:
        return book_id.split('-', 1)
    return [book_id, ""]

# Dicionário para rastrear os IDs dos autores e colaboradores
author_ids = {}

# Processar cada livro
for book in books_data:
    # Dividir o bookId em _id e title
    book_id_split = split_book_id(book["bookId"])
    book["_id"] = book_id_split[0]
    book["title"] = book_id_split[1]
    del book["bookId"]

    # Separar o autor principal dos colaboradores
    authors = book["author"].split(", ")

    # Atribuir IDs aos autores e manter o rastreamento
    for author in authors:
        if author not in author_ids:
            author_ids[author] = len(author_ids) + 1
    
    book["author"] = {
        "name": authors[0],
        "author_id": author_ids[authors[0]]
    }
    book["collaborators"] = [{"name": collaborator, "collaborator_id": author_ids[collaborator]} for collaborator in authors[1:]]

# Converter a lista de dicionários para uma string JSON formatada
json_data = json.dumps(books_data, indent=4)

# Salvar os dados JSON processados em um novo arquivo
with open('livros.json', 'w') as f:
    f.write(json_data)
