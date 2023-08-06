from typing import Any, Callable, Type


class LazyProperty:

    "Calculate value of a property in a lazy way"

    __doc__: str
    _name: str

    fget: Callable
    fset: Callable
    fdel: Callable

    def __init__(
            self, fget: Callable = None, fset: Callable = None,
            fdel: Callable = None, doc: str = None) -> None:
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def _is_calculated(self, owner: Any) -> bool:
        return hasattr(owner, self._private_property_name)

    def __set_name__(self, owner_class: Type, name: str) -> None:
        self._property_name = name
        self._private_property_name = f"__lazy__{name}"

    def getter(self, fget: Callable) -> 'LazyProperty':
        # always create entirely new property object. Do not mutate existing
        # one. Mutating existing property object would break subclassing.
        # Let's have a look at this example:
        # class Parent:
        #   @lazy_property
        #   def some_property(self) -> int:
        #       ...
        #
        # class Child(Parent):
        #   @Parent.some_property.setter
        #   def some_property(self, int) -> None:
        #       ...
        # In this example mutating property on class 'Child' would mutate also
        # the same property object on super class 'Parent'. Creating new
        # property object each time efficiently resolves this problem.
        # But be warned! On the other hand this solution puts on user some
        # strong assumption: getter, setter and deleter must be always
        # annotated on a class attribute with the exact same name. So this is
        # allowed:
        # class my_class:
        #   @lazy_property
        #   def some_property(self) -> int:
        #       ...
        #   @some_property.setter
        #   def some_property(self, int) -> None:
        #       ...
        # but this is NOT allowed:
        # class my_class:
        #   @lazy_property
        #   def some_property(self) -> int:
        #       ...
        #   @some_property.setter
        #   def set_some_property(self, int) -> None:
        #       ...
        # the latter example would create two different class attributes with
        # two different property objects
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset: Callable) -> 'LazyProperty':
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel: Callable) -> 'LazyProperty':
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

    def __get__(self, owner: Any, owner_class=None) -> Any:
        if owner is None:
            # probably accessing property by class eg.: C.x
            # in that case we should return propery object itself and not a
            # value from getter
            return self
        if not self._is_calculated(owner):
            if self.fget is None:
                raise AttributeError(
                    f"Getter not defined for property '{self._property_name}'")
            setattr(
                owner,
                self._private_property_name,
                self.fget(owner))
        return getattr(owner,  self._private_property_name)

    def __set__(self, owner: Any, value: Any) -> None:
        if self.fset is None:
            raise AttributeError(
                f"Attribute '{self._property_name}' is read only")
        if self._is_calculated(owner):
            delattr(owner, self._private_property_name)
        self.fset(owner, value)

    def __delete__(self, owner: Any) -> None:
        if self._is_calculated(owner):
            delattr(owner, self._private_property_name)
        if self.fdel is not None:
            self.fdel(owner)


def lazy_property(fget: Callable) -> LazyProperty:
    return LazyProperty(fget=fget)


# Example
#
# class C:

#     @lazy_property
#     def x(self):
#         return 2 * self._a

#     @x.setter
#     def x(self, value):
#         self._a = value

#     @x.deleter
#     def x(self):
#         del self._a


# class C2(C):

#     @C.x.setter
#     def x(self, value):
#         self._a = 2 * value


# a = C()
# a.x = 1
# a.x  # evaluation
# a.x  # this is already evaluated
