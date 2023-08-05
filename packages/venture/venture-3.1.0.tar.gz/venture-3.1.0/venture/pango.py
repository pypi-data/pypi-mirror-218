"""Utility functions for generating Pango Markup
https://docs.gtk.org/Pango/pango_markup.html
"""


def pango_markup(element: str, child: object, **kwargs):
    return (
        f"<{element} "
        + " ".join(f'{key}="{value}"' for key, value in kwargs.items())
        + f">{child}</{element}>"
    )


def span(child: object, **kwargs):
    return pango_markup("span", child, **kwargs)
