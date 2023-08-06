class NodeJSNotInstalled(Exception):
    """Node.js isn’t installed, raised by
    :meth:`~metacalls.MetaCalls.start` or
    :meth:`~metacalls.MetaCalls.run`
    """

    def __init__(
        self,
        version_needed: str,
    ):
        super().__init__(
            f'Please install node ({version_needed}+)',
        )


class TooOldNodeJSVersion(Exception):
    """Node.js version is too old, raised by
    :meth:`~metacalls.MetaCalls.start` or
    :meth:`~metacalls.MetaCalls.run`
    """

    def __init__(
        self,
        version_needed: str,
        node_version: str,
    ):
        super().__init__(
            f'Needed node {version_needed}+, '
            'actually installed is '
            f'{node_version}',
        )


class TooOldPyrogramVersion(Exception):
    """Pyrogram version is too old, raised by
    :meth:`~metacalls.MetaCalls.start` or
    :meth:`~metacalls.MetaCalls.run`
    """

    def __init__(
            self,
            version_needed: str,
            meta_version: str,
    ):
        super().__init__(
            f'Needed meta {version_needed}+, '
            'actually installed is '
            f'{meta_version}',
        )


class TooOldTelethonVersion(Exception):
    """Telethon version is too old, raised by
    :meth:`~metacalls.MetaCalls.start` or
    :meth:`~metacalls.MetaCalls.run`
    """

    def __init__(
        self,
        version_needed: str,
        telethon_version: str,
    ):
        super().__init__(
            f'Needed telethon {version_needed}+, '
            'actually installed is '
            f'{telethon_version}',
        )


class InvalidStreamMode(Exception):
    """The stream mode is invalid, raised by
    :meth:`~metacalls.MetaCalls.change_stream` or
    :meth:`~metacalls.MetaCalls.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Invalid stream mode',
        )


class NoMtProtoClientSet(Exception):
    """An MtProto client not set to
    :class:`~metacalls.MetaCalls`, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`,
    :meth:`~metacalls.MetaCalls.leave_group_call`,
    :meth:`~metacalls.MetaCalls.change_volume_call`,
    :meth:`~metacalls.MetaCalls.change_stream`,
    :meth:`~metacalls.MetaCalls.pause_stream` and
    :meth:`~metacalls.MetaCalls.resume_stream`
    """

    def __init__(self):
        super().__init__(
            'No MtProto client set',
        )


class NodeJSNotRunning(Exception):
    """NodeJS core not running, do
    :meth:`~metacalls.MetaCalls.start`
    before call these methods, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`,
    :meth:`~metacalls.MetaCalls.leave_group_call`,
    :meth:`~metacalls.MetaCalls.change_volume_call`,
    :meth:`~metacalls.MetaCalls.change_stream`,
    :meth:`~metacalls.MetaCalls.pause_stream` and
    :meth:`~metacalls.MetaCalls.resume_stream`
    """

    def __init__(self):
        super().__init__(
            'Node.js not running',
        )


class NoActiveGroupCall(Exception):
    """No active group call found, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`,
    :meth:`~metacalls.MetaCalls.leave_group_call`,
    :meth:`~metacalls.MetaCalls.change_volume_call`,
    """

    def __init__(self):
        super().__init__(
            'No active group call',
        )


class NotInGroupCallError(Exception):
    """The userbot there isn't in a group call, raised by
    :meth:`~metacalls.MetaCalls.leave_group_call`
    """

    def __init__(self):
        super().__init__(
            'The userbot there isn\'t in a group call',
        )


class AlreadyJoinedError(Exception):
    """Already joined into group call, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Already joined into group call',
        )


class TelegramServerError(Exception):
    """Telegram Server is having some
    internal problems, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Telegram Server is having some '
            'internal problems',
        )


class MetaCallsAlreadyRunning(Exception):
    """MetaCalls client is already running, raised by
    :meth:`~metacalls.MetaCalls.start`,
    """

    def __init__(self):
        super().__init__(
            'MetaCalls client is already running',
        )


class TooManyCustomApiDecorators(Exception):
    """Too Many Custom Api Decorators, raised by
    :meth:`~metacalls.CustomApi.on_update_custom_api`,
    """

    def __init__(self):
        super().__init__(
            'Too Many Custom Api Decorators',
        )


class GroupCallNotFound(Exception):
    """Group call not found, raised by
    :meth:`~metacalls.MetaCalls.get_active_call`,
    :meth:`~metacalls.MetaCalls.get_call`
    """

    def __init__(
        self,
        chat_id: int,
    ):
        super().__init__(
            f'Group call not found with the chat id {chat_id}',
        )


class InvalidMtProtoClient(Exception):
    """You set an invalid MtProto client, raised by
    :meth:`~metacalls.MetaCalls`
    """

    def __init__(self):
        super().__init__(
            'Invalid MtProto Client',
        )


class NoVideoSourceFound(Exception):
    """This error is raised when the stream does not have video streams
    :meth:`~metacalls.MetaCalls.join_group_call` or
    :meth:`~metacalls.MetaCalls.change_stream`
    """

    def __init__(self, path: str):
        super().__init__(
            f'No video source found on {path}',
        )


class InvalidVideoProportion(Exception):
    """FFmpeg have sent invalid video measure
    response, raised by
    :meth:`~metacalls.MetaCalls.join_group_call` or
    :meth:`~metacalls.MetaCalls.change_stream`
    """

    def __init__(self, message: str):
        super().__init__(
            message,
        )


class NoAudioSourceFound(Exception):
    """This error is raised when the stream does not have audio streams
    :meth:`~metacalls.MetaCalls.join_group_call` or
    :meth:`~metacalls.MetaCalls.change_stream`
    """

    def __init__(self, path: str):
        super().__init__(
            f'No audio source found on {path}',
        )


class FFmpegNotInstalled(Exception):
    """FFmpeg isn't installed, this error is raised by
    :meth:`~metacalls.MetaCalls.join_group_call` or
    :meth:`~metacalls.MetaCalls.change_stream`
    """

    def __init__(self, path: str):
        super().__init__(
            'FFmpeg ins\'t installed on your server',
        )


class RTMPStreamNeeded(Exception):
    """Needed an RTMP Stream, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Needed an RTMP Stream',
        )


class UnMuteNeeded(Exception):
    """Needed to unmute the userbot, raised by
    :meth:`~metacalls.MetaCalls.join_group_call`
    """

    def __init__(self):
        super().__init__(
            'Needed to unmute the userbot',
        )
