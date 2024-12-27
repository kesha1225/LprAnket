import datetime
from io import BytesIO

import xlsxwriter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.convertor import get_text_bool
from db.models.form import FormDB
from db.models.user import TGUser
from db.session import with_session


@with_session
async def create_excel_dump(session: AsyncSession) -> bytes:
    query = (
        select(FormDB, TGUser)
        .join(TGUser, FormDB.user_tg_id == TGUser.tg_id)
        .order_by(FormDB.id)
    )
    results = (await session.execute(query)).all()

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, options={"remove_timezone": True})
    worksheet = workbook.add_worksheet("Анкеты")

    date_format = workbook.add_format({"num_format": "hh:mm:ss dd.mm.yyyy"})

    headers = [
        "Телеграм ID",
        "Телеграм Юзернейм",
        "Телеграм Имя",
        "Телеграм Фамилия",
        "Имя",
        "Регион",
        "Хочет получать уведомления о новых мероприятиях",
        "Хочет встретиться с либертарианцами своего города",
        "Хочет заниматься около-политической активностью без привязки к какой-либо организации",
        "Хочет вступить в ЛПР или стать сторонником организации",
        "Идеи, послания, пожелания",
        "Дата заполнения формы",
        "Дата захода пользователя в бот",
    ]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    data_rows = []
    for row_num, (form, user) in enumerate(results, start=1):
        row = [
            user.tg_id,
            user.username,
            user.first_name,
            user.last_name,
            form.name,
            form.region,
            get_text_bool(form.notify),
            get_text_bool(form.meetings),
            get_text_bool(form.near_politic),
            get_text_bool(form.lpr_join),
            form.other,
            form.created_at,
            user.created_at,
        ]
        data_rows.append(row)

    for row_num, row_data in enumerate(data_rows, start=1):
        for col_num, value in enumerate(row_data):
            if isinstance(value, datetime.datetime):
                worksheet.write_datetime(row_num, col_num, value, date_format)
            else:
                worksheet.write(row_num, col_num, value)

    for col_num, header in enumerate(headers):
        max_width = max(
            len(header), max((len(str(row[col_num])) for row in data_rows), default=0)
        )
        worksheet.set_column(col_num, col_num, max_width + 2)

    workbook.close()
    return output.getvalue()
