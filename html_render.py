#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:
    indent = "    "

    def __init__(self, content=None, tag="", id="", style="", href="", charset=""):
        if tag:
            self._tag = tag
        elif content == "None":
            self._tag = "None"
        else:
            self._tag = ""
        
        self._id = id
        self._style = style
        self._href = href
        self._charset = charset

        if content and content != "None":
            self._content = [content]
        else:
            self._content = []

    def append(self, new_content):
        self._content.append(new_content)

    def render(self, out_file, oneline=False, selfclosing=False, cur_ind=""):
        self.write_opening_tag(out_file, oneline, selfclosing, cur_ind)
        for item in self._content:
            next_ind = cur_ind + self.indent
            mro = str(item.__class__.__mro__[-2])
            if mro.__contains__(".Element'>"):
                item.render(out_file, cur_ind=next_ind)
            else:
                if oneline:
                    out_file.write(item)
                else:
                    out_file.write(next_ind + item + "\n")
        if not selfclosing:
            self.write_closing_tag(out_file, cur_ind, oneline)
    
    def write_opening_tag(self, out_file, oneline=False, selfclosing=False, cur_ind = ""):
        id = ""
        if self._id != "":
            id = f" id=\"{self._id}\""
        style = ""
        if self._style != "":
            style = f" style=\"{self._style}\""
        href = ""
        if self._href:
            href = f" href=\"{self._href}\""
        charset = ""
        if self._charset:
            charset = f" charset=\"{self._charset}\""

        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"{cur_ind}<{self._tag}{id}{style}{href}{charset}")
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
    
    def write_closing_tag(self, out_file, cur_ind = "", oneline=False):
        if self._tag == "None":
            pass
        elif self._tag:
            if oneline:
                out_file.write(f"</{self._tag}>\n")
            else:
                out_file.write(f"{cur_ind}</{self._tag}>\n")
        else:
            out_file.write(f"</html>\n")

class Html(Element):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="html", id=id, style=style)
    
    def render(self, out_file, cur_ind=""):
        out_file.write("<!DOCTYPE html>\n")
        super().render(out_file, cur_ind=cur_ind)

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

    def render(self, out_file, cur_ind=""):
        super().render(out_file, oneline=True, cur_ind=cur_ind)

class SelfClosingTag(Element):
    """
    A subclass that overrides render, making a self closing tag
    """

    def __init__(self, content=None, tag="", id="", style="", charset=""):
        super().__init__(content=content, tag=tag, id=id, style=style, charset=charset)

    def render(self, out_file, cur_ind=""):
        super().render(out_file, oneline=True, selfclosing=True, cur_ind=cur_ind)

class Title(OneLineTag):

    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="title", id=id, style=style)

class Hr(SelfClosingTag):

    def __init__(self, content="", link=""):
        super().__init__(content=content, tag="hr")

class A(OneLineTag):

    def __init__(self, content="", link=""):
        super().__init__(content=content, tag="a", href=link)

class Ul(Element):
    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="ul", id=id, style=style)

class Li(Element):
    def __init__(self, content=None, id="", style=""):
        super().__init__(content=content, tag="li", id=id, style=style)

class H(OneLineTag):
    def __init__(self, level= 1, content=None, id="", style=""):
        header_tag = "h" + str(level)
        super().__init__(content=content, tag=header_tag, id="", style="")

class Meta(SelfClosingTag):
    def __init__(self, content="", charset=""):
        super().__init__(content=content, tag="meta", charset=charset)


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
    html = Html()
    head = Head()
    head.append(Meta(charset="UTF-8"))
    head.append(Title("Python Class Sample page"))
    html.append(head)

    body = Body()
    body.append(H("Python Class - Html rendering example", level=2))
    body.append(P("Here is a paragraph of text -- there could be more of them, but this is enough to show that we can do some text",
                  style="text-align; font-style: oblique;"))
    body.append(Hr())
    ul = Ul(id="TheList", style="line-height:200%")
    ul.append(Li("The first item in a list"))
    ul.append(Li("This is the second item", style="color: red"))
    li3 = Li("And this is a")
    a = A(content="link to google", link="http://google.com")
    li3.append(a)
    li3.append("to google")
    ul.append(li3)
    body.append(ul)
    html.append(body)

    outfile = io.StringIO()
    html.render(outfile)
    print(outfile.getvalue())
