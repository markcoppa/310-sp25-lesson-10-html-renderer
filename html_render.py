#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:

    def __init__(self, content=None, tag="", id="", style="", href=""):
        if tag:
            self._tag = tag
        elif content == "None":
            self._tag = "None"
        else:
            self._tag = ""
        
        self._id = id
        self._style = style
        self._href = href

        if content and content != "None":
            self._content = [content]
        else:
            self._content = []

    def append(self, new_content):
        self._content.append(new_content)

    def render(self, out_file, oneline=False, selfclosing=False):
        self.write_opening_tag(out_file, oneline, selfclosing)
        for item in self._content:
            mro = str(item.__class__.__mro__[-2])
            if mro.__contains__(".Element'>"):
                item.render(out_file)
            else:
                out_file.write(item)
                if not oneline:
                    out_file.write("\n")
        if not selfclosing:
            self.write_closing_tag(out_file)
    
    def write_opening_tag(self, out_file, oneline=False, selfclosing=False):
        id = ""
        if self._id != "":
            id = f" id=\"{self._id}\""
        style = ""
        if self._style != "":
            style = f" style=\"{self._style}\""
        href = ""
        if self._href:
            href = f" href=\"{self._href}\""            

        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"<{self._tag}{id}{style}{href}")
            if selfclosing:
                out_file.write(" />\n")
            else:
                out_file.write(">")
            if not oneline:
                out_file.write("\n")
        else:
            out_file.write(f"<html>{id}{style}")
            if not oneline:
                out_file.write("\n")
    
    def write_closing_tag(self, out_file):
        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"</{self._tag}>\n")
        else:
            out_file.write(f"</html>\n")

class Html(Element):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="html", id=id, style=style)

class Body(Element):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="body", id=id, style=style)

class P(Element):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="p", id=id, style=style)

class Head(Element):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="head", id=id, style=style)

class OneLineTag(Element):
    """
    A subclass that overrides render(),
    such that it prints the element all on one line.
    """

    def __init__(self, content=None, tag="", id="", style="", href=""):
        super().__init__(content=content, tag=tag, id=id, style=style, href=href)

    def render(self, out_file):
        super().render(out_file, oneline=True)

class SelfClosingTag(Element):
    """
    A subclass that overrides render, making a self closing tag
    """

    def __init__(self, content=None, tag="", id="", style=""):
        super().__init__(content=content, tag=tag, id=id, style=style)

    def render(self, out_file):
        super().render(out_file, oneline=True, selfclosing=True)

class Title(OneLineTag):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="title", id="", style="")

class HR(SelfClosingTag):

    def __init__(self, content="", link=""):
        super().__init__(content=content, tag="hr")

class A(OneLineTag):

    def __init__(self, content="", link=""):
        super().__init__(content=content, tag="a", href=link)



import io

def render_result(element, ind=""):
    """
    calls the element's render method, and returns what got rendered as a
    string
    """
    # the StringIO object is a "file-like" object -- something that
    # provides the methods of a file, but keeps everything in memory
    # so it can be used to test code that writes to a file, without
    # having to actually write to disk.
    outfile = io.StringIO()
    # this so the tests will work before we tackle indentation
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()


if __name__ == "__main__":
    top = Element("None")
    top.append("<!DOCTYPE html>")
    head = Head()
    top.append(head)
    html = Html(style="mystyle")
    html.append(Title("Title goes here"))
    head.append(html)
    e = Body("this is some text")
    e.append("and this is some more text")
    html.append(e)
    p = P("Paragraph content", id="myid", style="mystyle")
    html.append(p)
    hr = HR()
    html.append(hr)
    a = A(content="link to google", link="http://google.com")
    html.append(a)
    outfile = io.StringIO()
    top.render(outfile)
    print(outfile.getvalue())
