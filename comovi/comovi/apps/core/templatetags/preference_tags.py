from django import template

from comovi.apps.core.models import SitePreferences

register = template.Library()


class PreferenceNode(template.Node):
    def __init__(self, varname=None, property=None):
        if property is None:
            raise template.TemplateSyntaxError(
                "Preference template nodes must be given a property to return.")
        self.property = property
        self.varname = varname

    def render(self, context):
        preferences = SitePreferences.get()
        if hasattr(preferences, str(self.property)):
            attr = getattr(preferences, str(self.property), None)
        else:
            attr = None
        if self.varname is None:
            return attr
        context[self.varname] = attr
        return ''

    @classmethod
    def handle_token(cls, parser, token):
        """
        Class method to parse prefix node and return a Node.
        """
        bits = token.split_contents()

        if len(bits) < 2:
            raise template.TemplateSyntaxError(
                "'%s' takes at least one argument (property from preferences)" % bits[0])

        property = parser.compile_filter(bits[1])

        if len(bits) >= 2 and bits[-2] == 'as':
            varname = bits[3]
        else:
            varname = None

        return cls(varname, property)


def _fetch_preference(parser, token):
    return PreferenceNode.handle_token(parser, token)


@register.tag('preferences')
def fetch_preference(parser, token):
    return _fetch_preference(parser, token)
