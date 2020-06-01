"""
This is the Habiter module, to implement classes specifics to interface discord.py with habiter.
"""

from . import utils
from .mixins import Hashable

class Object(Hashable):
    """Represents a generic Discord object.

    The purpose of this class is to allow you to create 'miniature'
    versions of data classes if you want to pass in just an ID. Most functions
    that take in a specific data class with an ID can also take in this class
    as a substitute instead. Note that even though this is the case, not all
    objects (if any) actually inherit from this class.

    **HABITER**: we need object to be a messable, specifically in the case of
    users where we want to inverse map Habiter User -> discord.py users, and 
    be able to use the `user.send` method. Thus this class extends `abc.Messageable`
    and implements a `_get_channel`.

    Attributes
    -----------
    id: :class:`int`
        The ID of the object.
    """

    def __init__(self, id):
        try:
            id = int(id)
        except ValueError:
            raise TypeError('id parameter must be convertable to int not {0.__class__!r}'.format(id)) from None
        else:
            self.id = id

    def __repr__(self):
        return '<Object id=%r>' % self.id

    @property
    def created_at(self):
        """:class:`datetime.datetime`: Returns the snowflake's creation time in UTC."""
        return utils.snowflake_time(self.id)
