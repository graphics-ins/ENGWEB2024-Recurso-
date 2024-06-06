
Setup mongodb

Para o setup da base de dados Mongo, tivemos de fazer um mongoimport do ficheiro que nos foi fornecido, mas não antes de fazer o tratamento do ficheiro que se encontrava num formato JSON. Para isto, usamos um script de Python onde alteramos as strings que representavam lista e convertemos em listas com strings. De seguida, modificámos o campo "bookId" do ficheiro para "_id" para estar em conformidade com o Mongo e "titulo", de seguida, fizemos os seguintes comandos para importar o dataset. Estes comandos foram feitos com o Mongo já a correr:

docker cp livros.json mongoEW:/tmp
docker exec -it mongoEW bash
mongoimport -d livros -c livros /tmp/livros.json --jsonArray

>> 20000 document(s) imported successfully. 0 document(s) failed to import.


Persistencia dos dados

Exercício 1 

Quantos livros têm a palavra Love no título:

db.livros.find({"title": /Love/i}).count()

Quais os títulos dos livros, em ordem alfabética, em que um dos autores tem apelido Austen:

db.livros.find({"author": /Austen/i}, {"title": 1, "_id": 0}).sort({"title": 1}).collation({"locale": "pt", "strength": 2})

Qual a lista de autores (ordenada alfabeticamente e sem repetições)?

db.livros.distinct("author").sort()

Qual a distribuição de livros por género (genre) (quantos livros tem cada género)?

db.livros.aggregate([
    { $unwind: "$genres" },  
    { $group: { _id: "$genres", count: { $sum: 1 } } }, 
    { $sort: { "count": -1 } }  
])

Quais os títulos dos livros e respetivos isbn, em ordem alfabética de título, em que um dos personagens (characters) é Sirius Black?

db.livros.aggregate([
    { $match: { characters: "Sirius Black" } }, // Filtra os documentos onde "Sirius Black" é um personagem
    { $sort: { title: 1 } }, // Ordena os resultados pelo título em ordem alfabética
    { $project: { _id: 0, title: 1, isbn: 1 } } // Projeta apenas os campos 'title' e 'isbn', excluindo o '_id'
])