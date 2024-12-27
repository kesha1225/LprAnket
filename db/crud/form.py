from sqlalchemy.ext.asyncio import AsyncSession

from db.models import FormDB
from db.session import with_session


@with_session
async def create_new_form(
    tg_id: int,
    form_dict: dict[str, str | bool | None],
    session: AsyncSession,
):
    prefix = "FormGroup:"

    cleaned_data = {
        key[len(prefix) :]: value
        for key, value in form_dict.items()
        if key.startswith(prefix)
    }

    form = FormDB(
        user_tg_id=tg_id,
        name=cleaned_data.get("name"),
        region=cleaned_data.get("region"),
        notify=cleaned_data.get("notify"),
        meetings=cleaned_data.get("meetings"),
        near_politic=cleaned_data.get("near_politic"),
        lpr_join=cleaned_data.get("lpr_join"),
        other=cleaned_data.get("other"),
    )

    session.add(form)
    await session.commit()

    return form
