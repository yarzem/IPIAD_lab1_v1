import pymorphy2
from fonetika.soundex import RussianSoundex
from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc, NewsNERTagger
from ipymarkup import format_dep_ascii_markup

text_file = open('source_text.txt', 'r', encoding='utf-8') #source text
result_file = open('result_file.txt', 'w', encoding='utf-8') #result text
readed_f = text_file.read()


############ Phonetic
soundex = RussianSoundex(code_vowels=True, reduce_word=False)
soundex._table = str.maketrans('бпвфгкхдтжшчщзсцлмнр', '11фф3к3445ш5щ666лmнр')
soundex._vowels_table = str.maketrans('аяоыиеёэюу', 'аяаыи6789у')
soundex._vowels_table = str.maketrans('ё', 'о')
result = soundex.transform(readed_f)
result_file.write('Phonetic Part:\n')
result_file.write(result)
result_file.write(('\n\n'))


########### Morph
result_file.write('Morph part:\n\n')
morph = pymorphy2.MorphAnalyzer()
splitted_f = readed_f.split()
splitted_f_new = splitted_f
#print(splitted_f)
readed_f_count = len(splitted_f)
#print(readed_f_count)
for i in range(readed_f_count):
    splitted_f_new[i] = morph.parse(splitted_f[i])
    #result_file.write(str(splitted_f_new[i]))

for i in range(readed_f_count):
    result_file.write(str(splitted_f_new[i]))
    result_file.write('\n')
result_file.write('\n\n')


######Syntax
result_file.write("Syntax part:\n")
emb = NewsEmbedding()
segmenter = Segmenter()
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
doc = Doc(readed_f)
doc.segment(segmenter)

doc.parse_syntax(syntax_parser)
for token in doc.tokens:
    result_file.write(str(token))
    result_file.write('\n')
result_file.write(str(doc.sents[0].syntax.print()))
for i in doc.sents:
    result_file.write(str(i.syntax.print()))


##### slovo - sochetania
tokens = doc.sents[1].syntax

for i in tokens:
    for j in i:
        for k in i :
            if j.__dict__["head_id"] == k.__dict__["id"] and j.__dict__["rel"] != 'punct' and k.__dict__["rel"] != 'punct':
                print(j.__dict__["text"], k.__dict__["text"])

text_file.close()
result_file.close()
