import typing

from aiogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    LinkPreviewOptions,
    Message,
    MessageEntity,
    VideoNote,
    Voice,
)

MediaType: typing.TypeAlias = (
    InputMediaAudio
    | InputMediaDocument
    | InputMediaPhoto
    | InputMediaVideo
    | Voice
    | VideoNote
)


def apply_entities_to_html(text: str, entities: list[MessageEntity]):
    entities = sorted(entities, key=lambda e: e.offset, reverse=True)

    for entity in entities:
        start = entity.offset
        end = start + entity.length
        entity_type = entity.type

        if entity_type == "bold":
            text = text[:start] + "<b>" + text[start:end] + "</b>" + text[end:]
        elif entity_type == "italic":
            text = text[:start] + "<i>" + text[start:end] + "</i>" + text[end:]
        elif entity_type == "strikethrough":
            text = text[:start] + "<s>" + text[start:end] + "</s>" + text[end:]
        elif entity_type == "underline":
            text = text[:start] + "<u>" + text[start:end] + "</u>" + text[end:]
        elif entity_type == "spoiler":
            text = (
                text[:start]
                + '<span class="tg-spoiler">'
                + text[start:end]
                + "</span>"
                + text[end:]
            )
        elif entity_type == "code":
            text = text[:start] + "<code>" + text[start:end] + "</code>" + text[end:]
        elif entity_type == "text_link":
            url = entity.url
            text = (
                text[:start]
                + f'<a href="{url}">'
                + text[start:end]
                + "</a>"
                + text[end:]
            )
        elif entity_type == "blockquote":
            text = (
                text[:start]
                + "<blockquote>"
                + text[start:end]
                + "</blockquote>"
                + text[end:]
            )
        elif entity_type == "expandable_blockquote":
            text = (
                text[:start]
                + "<blockquote expandable>"
                + text[start:end]
                + "</blockquote>"
                + text[end:]
            )

    return text


def create_input_media_data_from_input(
    messages: list[Message],
) -> tuple[str, list[MediaType], LinkPreviewOptions | None]:
    text = ""
    media = []
    entities = []
    link_preview_options = None
    show_caption_above_media = False

    for message in messages:
        if message.entities:
            entities = message.entities
        if message.caption_entities:
            entities = message.caption_entities

        if message.show_caption_above_media:
            show_caption_above_media = True

        if message.text:
            text = message.text
        if message.caption:
            text = message.caption

        if message.text or message.caption:
            link_preview_options = message.link_preview_options

        if message.photo:
            media.append(
                InputMediaPhoto(
                    media=message.photo[-1].file_id,
                    has_spoiler=message.has_media_spoiler,
                )
            )
        if message.video:
            media.append(
                InputMediaVideo(
                    media=message.video.file_id,
                    has_spoiler=message.has_media_spoiler,
                    width=message.video.width,
                    height=message.video.height,
                    duration=message.video.duration,
                )
            )
        if message.document:
            media.append(InputMediaDocument(media=message.document.file_id))
        if message.audio:
            media.append(
                InputMediaAudio(
                    media=message.audio.file_id,
                    duration=message.audio.duration,
                    performer=message.audio.performer,
                    title=message.audio.title,
                )
            )
        if message.voice:
            text = message.caption
            media.append(message.voice)
        if message.video_note:
            media.append(message.video_note)

    for media_obj in media:
        if isinstance(media_obj, (InputMediaPhoto, InputMediaVideo)):
            media_obj.show_caption_above_media = show_caption_above_media

    text = apply_entities_to_html(text=text, entities=entities)

    return text, media, link_preview_options
