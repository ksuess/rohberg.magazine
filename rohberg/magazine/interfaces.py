from plone.theme.interfaces import IDefaultPloneLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "zhrefch.corporatetheme" theme, this interface must be its layer
       (in corporatetheme/viewlets/configure.zcml).
    """
