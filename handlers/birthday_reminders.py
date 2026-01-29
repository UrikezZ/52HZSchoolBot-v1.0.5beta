# birthday_reminders.py - ИСПРАВЛЕННАЯ версия
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
import pytz
from config import TEACHER_IDS, get_birthday_info, is_teacher
from database import get_all_users

MOSCOW_TZ = pytz.timezone('Europe/Moscow')


async def check_and_send_birthday_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Проверяет и отправляет уведомления о днях рождения студентов ЗА 1 ДЕНЬ"""
    print("🎂 Проверяю дни рождения (за 1 день)...")

    # Текущая дата
    today = datetime.now(MOSCOW_TZ).date()
    tomorrow = today + timedelta(days=1)  # Завтра = ДР

    tomorrow_birthdays = []  # Только ДР завтра (уведомляем за 1 день)

    # Проверяем всех пользователей
    students = get_all_users(role='student')

    for student in students:
        # Пропускаем преподавателей
        if is_teacher(student['user_id']):
            continue

        # Получаем информацию о дне рождения
        birthday_info = get_birthday_info(student['user_id'])
        if not birthday_info:
            continue

        birthdate = birthday_info['birthdate']  # datetime объект

        # Проверяем, день рождения ЗАВТРА
        if birthdate.month == tomorrow.month and birthdate.day == tomorrow.day:
            tomorrow_birthdays.append({
                'user_id': student['user_id'],
                'profile': student,
                'age': birthday_info['age']
            })

    # Отправляем уведомления преподавателям только о завтрашних ДР
    await send_birthday_notifications(context, tomorrow_birthdays)


async def send_birthday_notifications(context: ContextTypes.DEFAULT_TYPE,
                                      tomorrow_birthdays: list):
    """Отправляет уведомления о днях рождения преподавателям"""

    # Только завтрашние дни рождения
    if tomorrow_birthdays:
        message = "📅 *Завтра день рождения у студентов:*\n\n"

        for student in tomorrow_birthdays:
            profile = student['profile']
            age = student['age'] + 1  # +1 потому что завтра ему исполнится

            instruments = profile.get('instruments', [])
            goals = profile.get('goals', 'Не указаны')

            message += (
                f"• *{profile['fio']}*\n"
                f"  Исполнится: {age} лет\n"
                f"  Инструмент: {', '.join(instruments) if instruments else 'Не указан'}\n"
                f"  Цели: {goals[:50]}{'...' if len(goals) > 50 else ''}\n\n"
            )

        # Отправляем всем преподавателям
        for teacher_id in TEACHER_IDS:
            try:
                await context.bot.send_message(
                    chat_id=teacher_id,
                    text=message,
                    parse_mode='Markdown'
                )
                print(f"🎂 Отправил уведомление о завтрашних днях рождения преподавателю {teacher_id}")
            except Exception as e:
                print(f"ERROR sending birthday notification to teacher {teacher_id}: {e}")

    if not tomorrow_birthdays:
        print("🎂 Завтра нет дней рождения у студентов")