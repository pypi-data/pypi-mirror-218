"""Response model definitions for client."""

from tekore._model import (
    Actions,
    Album,
    AlbumGroup,
    AlbumType,
    Artist,
    AudioAnalysis,
    Audiobook,
    AudioFeatures,
    Author,
    Category,
    CategoryPaging,
    Chapter,
    Context,
    ContextType,
    Copyright,
    CurrentlyPlaying,
    CurrentlyPlayingContext,
    CurrentlyPlayingType,
    Cursor,
    CursorPaging,
    Device,
    DeviceType,
    Disallows,
    Episode,
    ExplicitContent,
    Followers,
    FullAlbum,
    FullArtist,
    FullArtistCursorPaging,
    FullArtistOffsetPaging,
    FullAudiobook,
    FullChapter,
    FullEpisode,
    FullPlaylist,
    FullPlaylistEpisode,
    FullPlaylistTrack,
    FullShow,
    FullTrack,
    FullTrackPaging,
    Identifiable,
    Image,
    Item,
    LocalAlbum,
    LocalArtist,
    LocalItem,
    LocalPlaylistTrack,
    LocalTrack,
    Model,
    Narrator,
    OffsetPaging,
    Paging,
    PlayerErrorReason,
    PlayHistory,
    PlayHistoryCursor,
    PlayHistoryPaging,
    Playlist,
    PlaylistTrack,
    PlaylistTrackPaging,
    PrivateUser,
    PublicUser,
    Queue,
    RecommendationAttribute,
    Recommendations,
    RecommendationSeed,
    ReleaseDatePrecision,
    RepeatState,
    Restrictions,
    ResumePoint,
    SavedAlbum,
    SavedAlbumPaging,
    SavedEpisode,
    SavedEpisodePaging,
    SavedShow,
    SavedShowPaging,
    SavedTrack,
    SavedTrackPaging,
    Section,
    Segment,
    Show,
    SimpleAlbum,
    SimpleAlbumPaging,
    SimpleArtist,
    SimpleAudiobook,
    SimpleAudiobookPaging,
    SimpleChapter,
    SimpleChapterPaging,
    SimpleEpisode,
    SimpleEpisodePaging,
    SimplePlaylist,
    SimplePlaylistPaging,
    SimpleShow,
    SimpleShowPaging,
    SimpleTrack,
    SimpleTrackPaging,
    StrEnum,
    TimeInterval,
    Track,
    TrackLink,
    Tracks,
    UnknownModelAttributeWarning,
    User,
)

# Change the module of classes to hide module structure
# and fix Sphinx base class links
_classes = [
    AlbumType,
    Album,
    AlbumGroup,
    SimpleAlbum,
    SimpleAlbumPaging,
    FullAlbum,
    SavedAlbum,
    SavedAlbumPaging,
    Artist,
    SimpleArtist,
    FullArtist,
    FullArtistCursorPaging,
    FullArtistOffsetPaging,
    AudioAnalysis,
    TimeInterval,
    Section,
    Segment,
    AudioFeatures,
    Author,
    Narrator,
    Audiobook,
    SimpleAudiobook,
    SimpleAudiobookPaging,
    FullAudiobook,
    Identifiable,
    Item,
    Category,
    CategoryPaging,
    Chapter,
    SimpleChapter,
    SimpleChapterPaging,
    FullChapter,
    ContextType,
    Context,
    CurrentlyPlayingType,
    CurrentlyPlayingContext,
    CurrentlyPlaying,
    RepeatState,
    Disallows,
    Actions,
    Queue,
    Device,
    DeviceType,
    ResumePoint,
    Episode,
    SimpleEpisode,
    SimpleEpisodePaging,
    FullEpisode,
    SavedEpisode,
    SavedEpisodePaging,
    PlayerErrorReason,
    LocalItem,
    LocalAlbum,
    LocalArtist,
    LocalTrack,
    ReleaseDatePrecision,
    Copyright,
    Followers,
    Image,
    Restrictions,
    Paging,
    OffsetPaging,
    Cursor,
    CursorPaging,
    PlayHistory,
    PlayHistoryCursor,
    PlayHistoryPaging,
    PlaylistTrack,
    PlaylistTrackPaging,
    Playlist,
    SimplePlaylist,
    FullPlaylist,
    SimplePlaylistPaging,
    FullPlaylistTrack,
    FullPlaylistEpisode,
    LocalPlaylistTrack,
    Recommendations,
    RecommendationSeed,
    RecommendationAttribute,
    Show,
    SimpleShow,
    SimpleShowPaging,
    SavedShow,
    SavedShowPaging,
    FullShow,
    TrackLink,
    Track,
    Tracks,
    SimpleTrack,
    SavedTrack,
    FullTrack,
    SimpleTrackPaging,
    SavedTrackPaging,
    FullTrackPaging,
    ExplicitContent,
    UnknownModelAttributeWarning,
    User,
    PrivateUser,
    PublicUser,
    Model,
    StrEnum,
]

for _cls in _classes:
    _cls.__module__ = "tekore.model"
