
E = "/e:full-text-retrieval-response"
ART = "*[self::ja:converted-article or self::ja:article]"

CE = "http://www.elsevier.com/xml/common/dtd"
TAG = "{%s}%%s" % CE
XREFS = {TAG % "cross-ref", TAG % "cross-refs"}
ITALIC = {TAG % "italic"}

class Elsevier():
    def __init__(self, root):
        super().__init__(root)
        ns = root.nsmap.copy()
        ns["e"] = ns.pop(None)
        self.ns = ns
        self.figures = {
            f.attrib["id"]: f
            for f in self.root.xpath(
                E + "/e:originalText/xocs:doc/xocs:serial-item//ce:figure[@id]",
                namespaces=ns,
            )
        }

        self.tables = {
            f.attrib["id"]: f
            for f in self.root.xpath(
                E + "/e:originalText/xocs:doc/xocs:serial-item//ce:table[@id]",
                namespaces=ns,
            )
        }

    @property
    def pubmed(self):
        r = self.root.xpath(E + "/e:pubmed-id", namespaces=self.ns)
        if not r:
            return None
        return r[0].text.strip()

    def title(self):
        r = self.root.xpath(E + "/e:coredata/dc:title", namespaces=self.ns)
        if not r:
            return None
        return r[0].text.strip()

    def results(self):

        secs = self.root.xpath(
            E
            + "/e:originalText/xocs:doc/xocs:serial-item/"
            + ART
            + "/ja:body/ce:sections",
            namespaces=self.ns,
        )
        for sec in secs:
            for s in sec.xpath("./ce:section", namespaces=self.ns):
                for t in s.xpath(".//ce:section-title/text()", namespaces=self.ns):
                    if t.lower().find("results") >= 0:
                        return s

        return None

    def methods(self):

        secs = self.root.xpath(
            E
            + "/e:originalText/xocs:doc/xocs:serial-item/"
            + ART
            + "/ja:body/ce:sections",
            namespaces=self.ns,
        )
        for sec in secs:
            for s in sec.xpath("./ce:section", namespaces=self.ns):
                for t in s.xpath(".//ce:section-title/text()", namespaces=self.ns):
                    txt = t.lower()
                    if txt.find("methods") >= 0:
                        return s
                    if txt.find("experimental procedures") >= 0:
                        return s

        return None

    def abstract(self):

        secs = self.root.xpath(
            E
            + "/e:originalText/xocs:doc/xocs:serial-item/"
            + ART
            + "/ja:head/ce:abstract/ce:abstract-sec",
            namespaces=self.ns,
        )
        if not secs:
            return None
        return secs[0]



    def tostr(self, sec):
        def txt(p):
            res = []
            for t in para2txt2(p):
                res.append(t)

            txt = "".join(res)
            txt = self.SPACE.sub(" ", txt)
            return txt.strip()

        for p in sec.xpath(
            ".//*[self::ce:para or self::ce:simple-para]", namespaces=self.ns
        ):
            # TODO: <ce:float-anchor refid='FIG2'/>
            yield txt(p)
            for f in p.xpath(".//ce:float-anchor[@refid]", namespaces=self.ns):
                fid = f.attrib["refid"]
                if fid in self.figures:
                    fig = self.figures[fid]
                    t = " ".join(
                        txt(c) for c in fig.xpath(".//ce:caption", namespaces=self.ns)
                    )
                    yield self.FIGURE % t
                else:
                    fig = self.tables[fid]
                    t = " ".join(
                        txt(c) for c in fig.xpath(".//ce:caption", namespaces=self.ns)
                    )
                    yield self.TABLE % t
