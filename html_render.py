#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:

    def __init__(self, content=None, tag=""):
        if tag:
            self._tag = tag
        elif content == "None":
            self._tag = "None"
        else:
            self._tag = ""

        if content and content != "None":
            self._content = [content]
        else:
            self._content = []

    def append(self, new_content):
        self._content.append(new_content)

    def render(self, out_file):
        self.write_opening_tag(out_file)
        for item in self._content:
            mro = str(item.__class__.__mro__[-2])
            if mro.__contains__(".Element'>"):
                item.render(out_file)
            else:
                out_file.write(item + "\n")
        self.write_closing_tag(out_file)
    
    def write_opening_tag(self, out_file):
        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"<{self._tag}>\n")
        else:
            out_file.write(f"<html>\n")
    
    def write_closing_tag(self, out_file):
        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"</{self._tag}>\n")
        else:
            out_file.write(f"</html>\n")

class Html(Element):

    def __init__(self, content=None):
        super().__init__(content=content, tag="html")

class Body(Element):

    def __init__(self, content=None):
        super().__init__(content=content, tag="body")

class P(Element):

    def __init__(self, content=None):
        super().__init__(content=content, tag="p")

class Head(Element):

    def __init__(self, content=None):
        super().__init__(content=content, tag="head")

class OneLineTag(Element):
    """
    A subclass that overrides render(), such that it prints the element all on one line.
    Note that the only difference is that the line feeds for the opening tag
    and the content are taken out.
    Some refactoring can be done here.
    """

    def __init__(self, content=None, tag=""):
        super().__init__(content=content, tag=tag)

    def render(self, out_file):
        self.write_opening_tag(out_file)
        for item in self._content:
            mro = str(item.__class__.__mro__[-2])
            if mro.__contains__(".Element'>"):
                item.render(out_file)
            else:
                out_file.write(item)
        self.write_closing_tag(out_file)
    
    def write_opening_tag(self, out_file):
        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"<{self._tag}>")
        else:
            out_file.write(f"<html>")
    
    def write_closing_tag(self, out_file):
        if self._tag == "None":
            pass
        elif self._tag:
            out_file.write(f"</{self._tag}>\n")
        else:
            out_file.write(f"</html>\n")

class Title(OneLineTag):

    def __init__(self, content=None):
        super().__init__(content=content, tag="title")




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
    html = Html()
    html.append(Title("Title goes here"))
    head.append(html)
    e = Body("this is some text")
    e.append("and this is some more text")
    html.append(e)

    outfile = io.StringIO()
    top.render(outfile)
    print(outfile.getvalue())
