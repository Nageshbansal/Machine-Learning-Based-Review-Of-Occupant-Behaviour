import xml.etree.ElementTree as et

tree = et.parse('testing_data/response.xml')
root = tree.getroot()

pth = "{http://www.elsevier.com/xml/svapi/article/dtd}full-text-retrieval-response/{http://www.elsevier.com/xml/svapi/article/dtd}originalText/{http://www.elsevier.com/xml/xocs/dtd}doc/{http://www.elsevier.com/xml/xocs/dtd}serial-item/{http://www.elsevier.com/xml/ja/dtd}article/{http://www.elsevier.com/xml/ja/dtd}head/{http://www.elsevier.com/xml/common/dtd}keywords/{http://www.elsevier.com/xml/common/dtd}keyword/{http://www.elsevier.com/xml/common/dtd}text"
for movie in root.findall(pth):
    print(movie.attrib)

def pathGen(fn):
    path = []
    it = et.iterparse(fn, events=('start', 'end'))
    for evt, el in it:
        if evt == 'start':
            path.append(el.tag)
            yield '/'.join(path)
        else:
            path.pop()

for path in pathGen('testing_data/response.xml'):
    if "keywords" in path :
        with open('respons','w') as f:
            print(path, file=f)        
