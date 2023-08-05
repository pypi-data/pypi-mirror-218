from datetime import datetime
from typing import List, Optional

from .context import Context
from .paging import Cursor, CursorPaging
from .serialise import Model
from .track import FullTrack


class PlayHistory(Model):
    """
    Previously played track.

    Context is supposedly sometimes available.
    """

    track: FullTrack
    played_at: datetime
    context: Optional[Context]


class PlayHistoryCursor(Cursor):
    """Cursor to play history."""

    before: str


class PlayHistoryPaging(CursorPaging):
    """
    Paging to play history.

    Cursors are not available when paging is exhausted.
    """

    items: List[PlayHistory]
    cursors: Optional[PlayHistoryCursor]
