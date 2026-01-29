# test_all_lessons.py
import sys

sys.path.append('.')
from database import get_confirmed_lessons
from datetime import datetime, timedelta


def test_lessons():
    lessons = get_confirmed_lessons()

    print("📋 Все занятия в базе:")
    print("=" * 60)

    for lesson in lessons:
        print(f"ID: {lesson.get('id')}")
        print(f"Студент: {lesson.get('user_id')}")
        print(f"Slot ID: {lesson.get('slot_id')}")
        print(f"Slot Name: {lesson.get('slot_name')}")
        print(f"Тип: {'Ручное' if lesson.get('is_manual') else 'Обычное'}")
        print(f"Reminder Sent: {lesson.get('reminder_sent')}")
        print(f"Payment Type: {lesson.get('payment_type')}")
        print("-" * 40)

    # Проверяем даты
    print("\n🔍 Проверка дат:")
    today = datetime.now().date()
    in_2_days = today + timedelta(days=2)
    in_3_days = today + timedelta(days=3)

    print(f"Сегодня: {today.strftime('%d.%m.%Y')}")
    print(f"Через 2 дня: {in_2_days.strftime('%d.%m.%Y')}")
    print(f"Через 3 дня: {in_3_days.strftime('%d.%m.%Y')}")


test_lessons()