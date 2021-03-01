from typing import Union, List, Callable, Any
from dataclass_property import field_property, MISSING, get_return_type


__all__ = ['attr_property']


class attr_property(field_property):
    DOC_FMT = '{}'

    @property
    def private_name(self):
        return '_' + str(self.name)

    def get_private_or_default(self, instance):
        """Return the private variable value or default."""
        if self.default_factory_attr != MISSING:
            default_factory = getattr(instance, str(self.default_factory_attr), self.default_factory_attr)
            if isinstance(default_factory, (staticmethod, classmethod)):
                default_factory = default_factory.__get__(instance, type(instance))
            return getattr(instance, self.private_name, default_factory())

        elif self.default_attr != MISSING:
            default = getattr(instance, str(self.default), self.default)
            return getattr(instance, self.private_name, default)

        else:
            return getattr(instance, self.private_name)

    def __init__(self,
                 attr: str = None,
                 allow_none: bool = True,
                 fget: Callable[[Any], Any] = None,
                 fset: Callable[[Any, Any], None] = None,
                 fdel: Callable[[Any], None] = None,
                 doc: str = None,
                 default: Any = MISSING,
                 default_factory: Callable[[], Any] = MISSING):
        """Create an attribute based dataclass property where the underlying value is saved to "_attr".

        Args:
            attr (str): Attribute name (example: "created_on"
            allow_none (bool)[True]: Allows the property to be set to None. This is needed if the default is None.
            fget (callable/function)[None]: Function that gets and returns the value.
            fset (callable/function)[None]: Function that sets and saves the value.
            fdel (callable/function)[None]: Function that deletes the saved value/attribute.
            doc (str)[None]: Documentation comment for the property.
            default (object)[MISSING]: Default value for the dataclass
            default_factory (function)[MISSING]: Function that returns the default value.
        """
        typeref = get_return_type(default=default, default_factory=default_factory)
        self.name = attr

        if fget is None:
            def fget(this):
                return self.get_private_or_default(this)

        if fset is None:
            def fset(this, value: typeref):
                if value is None and not allow_none:
                    raise TypeError('Invalid value given!')
                setattr(this, self.private_name, value)

        if fdel is None:
            def fdel(this):
                delattr(this, self.private_name)

        super().__init__(fget=fget, fset=fset, fdel=fdel, doc=doc, default=default, default_factory=default_factory)

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)

        if not self.__doc__:
            self.__doc__ = self.DOC_FMT.format(name)
        if not self.fget.__doc__:
            try:
                self.__doc__ = self.DOC_FMT.format(name)
            except (AttributeError, Exception):
                pass
