import xml.etree.ElementTree as ET


def read_xml(file_path, word_min_len=6, top_words_amt=10):
    """
    функция для чтения файла с новостями.
    """
    # Ваш алгоритм
    news_list = []
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(file_path, parser)
    root = tree.getroot()
    news_list =  root.findall('channel/item/description')
#   print(news_list)
    news = []
    for i in news_list:
        news.append(i.text)
    words = []
    for t in news:
 #       t = t.lower()
        clean = ""
        for ch in t:
            if ch.isalnum() or ch.isspace():
                clean += ch
            else:
                clean += " "
        for w in clean.split():
            if len(w) > 6:   # только слова длиннее 6 символов
                words.append(w)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    # Сортировка по убыванию частоты
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    # Берём только первые 10 слов
    top10 = [word for word, count in sorted_freq[:10]]
    return top10
if __name__ == '__main__':
    print(read_xml('newsafr.xml'))

