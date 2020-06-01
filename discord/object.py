# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from . import utils
from .mixins import Hashable
from .abc import Messageable
from enum import Enum

class BareObjectTypes(Enum):
    USER = 'User'

class Object(Hashable, Messageable):
    """Represents a generic Discord object.

    **habiter-app fork**: we need object to be a messageable, 
    specifically in the case of
    users where we want to inverse map Habiter User -> discord.py users, and 
    be able to use the `user.send` method. Thus this class extends `abc.Messageable`
    and implements a `_get_channel`.

    ---

    The purpose of this class is to allow you to create 'miniature'
    versions of data classes if you want to pass in just an ID. Most functions
    that take in a specific data class with an ID can also take in this class
    as a substitute instead. Note that even though this is the case, not all
    objects (if any) actually inherit from this class.

    There are also some cases where some websocket events are received
    in :issue:`strange order <21>` and when such events happened you would
    receive this class rather than the actual data class. These cases are
    extremely rare.

    .. container:: operations

        .. describe:: x == y

            Checks if two objects are equal.

        .. describe:: x != y

            Checks if two objects are not equal.

        .. describe:: hash(x)

            Returns the object's hash.

    Attributes
    -----------
    id: :class:`int`
        The ID of the object.
    """

    def __init__(self, id, _state, _type=BareObjectTypes.USER):
        """
        Args:
            _state: bot._connection
        """
        try:
            id = int(id)
        except ValueError:
            raise TypeError('id parameter must be convertable to int not {0.__class__!r}'.format(id)) from None
        else:
            self.id = id

        self._state = _state
        self._type = _type

    @property
    def dm_channel(self):
        """Optional[:class:`DMChannel`]: Returns the channel associated with this user if it exists.

        If this returns ``None``, you can create a DM channel by calling the
        :meth:`create_dm` coroutine function.
        """
        return self._state._get_private_channel_by_user(self.id)

    async def create_dm(self):
        """Creates a :class:`DMChannel` with this user.

        This should be rarely called, as this is done transparently for most
        people.
        """
        found = self.dm_channel
        if found is not None:
            return found

        state = self._state
        data = await state.http.start_private_message(self.id)
        return state.add_dm_channel(data)

    def __repr__(self):
        return '<Object id=%r type=%s>' % self.id, self._type

    async def _get_channel(self):
        """
        Supported only if this is a (bare) user
        """
        if self._type == BareObjectTypes.USER:
            ch = await self.create_dm()
            return ch
        raise NotImplemented

    @property
    def created_at(self):
        """:class:`datetime.datetime`: Returns the snowflake's creation time in UTC."""
        return utils.snowflake_time(self.id)
