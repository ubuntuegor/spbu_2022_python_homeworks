from functools import wraps
from typing import Callable, Optional
from html import escape


class HTMLError(Exception):
    pass


class HTMLUnexpectedChildError(HTMLError):
    pass


class _HTMLNode:
    def __init__(self, tag: str, closing: bool, attrs: dict[str, str]):
        self.tag = tag
        self.closing = closing
        self.attrs = attrs
        self.children: list[_HTMLNode] = []

    def add_child(self, child: "_HTMLNode"):
        if not self.closing:
            raise HTMLUnexpectedChildError()
        self.children.append(child)

    def generate_html(self, prettify: bool = True) -> str:
        result = ""
        if len(self.attrs) == 0:
            result += f"<{self.tag}>"
        else:
            attrs_string = " ".join([f'{key}="{escape(value, True)}"' for key, value in self.attrs.items()])
            result += f"<{self.tag} {attrs_string}>"
        has_only_text = all([isinstance(child, _HTMLTextNode) for child in self.children])
        result += "\n" if not has_only_text and prettify else ""

        for child in self.children:
            child_html = child.generate_html(prettify)
            if not has_only_text and prettify:
                for line in child_html.strip().split("\n"):
                    result += "    " + line + "\n"
            else:
                result += child_html

        if self.closing:
            result += f"</{self.tag}>"
            result += "\n" if prettify else ""

        return result


class _HTMLTextNode(_HTMLNode):
    def __init__(self, text: str):
        self.text = text

    def add_child(self, _: "_HTMLNode"):
        raise HTMLUnexpectedChildError()

    def generate_html(self, _: bool = True) -> str:
        return self.text


class _HTMLShadowRootNode(_HTMLNode):
    def __init__(self):
        self.children: list[_HTMLNode] = []

    def add_child(self, child: "_HTMLNode"):
        self.children.append(child)

    def generate_html(self, prettify: bool = True) -> str:
        result = ""
        for child in self.children:
            child_html = child.generate_html(prettify)
            result += child_html
        return result


class _HTMLTag:
    def __init__(self, html: "HTML", node: _HTMLNode):
        self.html = html
        self.node = node

    def __enter__(self):
        self.parent = self.html.node
        self.html.node = self.node

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.parent.add_child(self.node)
        self.html.node = self.parent


def _void_tag_decorator(tag: str) -> Callable:
    def wrappee(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self, **attrs):
            node = _HTMLNode(tag, False, attrs)
            self.node.add_child(node)

        return wrapper

    return wrappee


def _tag_with_content_decorator(tag: str) -> Callable:
    def wrappee(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
            node = _HTMLNode(tag, True, attrs)
            if content is not None:
                node.add_child(_HTMLTextNode(content))
                self.node.add_child(node)
            else:
                return _HTMLTag(self, node)

        return wrapper

    return wrappee


class HTML:
    def __init__(self):
        self.node = _HTMLShadowRootNode()

    def text(self, content: str):
        self.node.add_child(_HTMLTextNode(content))

    @_tag_with_content_decorator("html")
    def html(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
        pass

    @_tag_with_content_decorator("head")
    def head(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
        pass

    @_tag_with_content_decorator("body")
    def body(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
        pass

    @_tag_with_content_decorator("div")
    def div(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
        pass

    @_tag_with_content_decorator("p")
    def p(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
        pass

    @_tag_with_content_decorator("a")
    def a(self, content: Optional[str] = None, **attrs) -> Optional[_HTMLTag]:
        pass

    @_void_tag_decorator("img")
    def img(self, **attrs):
        pass

    def generate(self, prettify: bool = True) -> str:
        return self.node.generate_html(prettify)
