import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import json

# Папка с CSV
CSV_DIR = Path('./dataset_raw')
CARDS_DIR = Path('./cards')
CARDS_DIR.mkdir(exist_ok=True, parents=True)


def generate_cards(
        table: Optional[str] = None,
        status: Optional[List[str]] = None,
        priority: Optional[List[str]] = None,
        department: Optional[List[str]] = None,
        assigned_user: Optional[List[str]] = None
) -> List[Dict]:
    cards = []

    # Загружаем таблицы
    tasks_df = pd.read_csv(CSV_DIR / 'tasks.csv') if table in (None, 'tasks') else None
    users_df = pd.read_csv(CSV_DIR / 'users.csv') if table in (None, 'users') else None
    departments_df = pd.read_csv(CSV_DIR / 'departments.csv') if table in (None, 'departments') else None
    companies_df = pd.read_csv(CSV_DIR / 'companies.csv') if table in (None, 'companies') else None
    task_history_df = pd.read_csv(CSV_DIR / 'task_history.csv') if table in (None, 'task_history') else None
    task_dependencies_df = pd.read_csv(CSV_DIR / 'task_dependencies.csv') if table in (
    None, 'task_dependencies') else None

    # Словари для быстрых ссылок
    if users_df is not None:
        users_df['full_name'] = users_df['first_name'].fillna('') + ' ' + users_df['last_name'].fillna('')
        users_df['position_clean'] = users_df['"position"'].fillna('')
        users_map = dict(zip(users_df['id'], users_df['full_name']))
    else:
        users_map = {}

    depts_map = dict(zip(departments_df['id'], departments_df['name'])) if departments_df is not None else {}
    dept_to_company = dict(
        zip(departments_df['id'], departments_df['company_id'])) if departments_df is not None else {}
    companies_map = dict(zip(companies_df['id'], companies_df['name'])) if companies_df is not None else {}
    tasks_map = dict(zip(tasks_df['id'], tasks_df['title'])) if tasks_df is not None else {}

    # Задачи
    if tasks_df is not None:
        df = tasks_df.copy()
        if status:
            df = df[df['status'].isin(status)]
        if priority:
            df = df[df['priority'].isin(priority)]
        if assigned_user:
            df['assigned_name'] = df['assigned_user_id'].map(users_map)
            df = df[df['assigned_name'].isin(assigned_user)]
        if department:
            df['assigned_dept_name'] = df['assigned_department_id'].map(depts_map)
            df = df[df['assigned_dept_name'].isin(department)]

        for _, row in df.iterrows():
            assigned_name = users_map.get(row.get('assigned_user_id'), 'Не назначен')
            dept_name = depts_map.get(row.get('assigned_department_id'), 'Не указано')
            company_name = companies_map.get(dept_to_company.get(row.get('assigned_department_id')), 'Не указана')

            text = (
                f"Название: {row.get('title', '')}. "
                f"Описание: {row.get('description', '')}. "
                f"Статус: {row.get('status', '')}. "
                f"Приоритет: {row.get('priority', '')}. "
                f"Исполнитель: {assigned_name}. "
                f"Подразделение: {dept_name}. "
                f"Компания: {company_name}."
            )

            cards.append({
                'id': row.get('id'),
                'table': 'tasks',
                'text': text,
                'created_by': row.get('created_by_user_id'),
                'assigned_to': row.get('assigned_user_id'),
                'department_id': row.get('assigned_department_id'),
                'company_id': dept_to_company.get(row.get('assigned_department_id')),
                'due_date': row.get('due_date'),
                'start_date': row.get('start_date'),
                'completed_date': row.get('completed_date')
            })

    # Пользователи
    if users_df is not None:
        df = users_df.copy()
        if department:
            df['department_name'] = df['department_id'].map(depts_map)
            df = df[df['department_name'].isin(department)]

        for _, row in df.iterrows():
            dept_name = depts_map.get(row.get('department_id'), 'Не указано')
            company_name = companies_map.get(dept_to_company.get(row.get('department_id')), 'Не указана')

            text = (
                f"Имя: {row.get('full_name', '')}. "
                f"Email: {row.get('email', '')}. "
                f"Должность: {row.get('position_clean', '')}. "
                f"Подразделение: {dept_name}. "
                f"Компания: {company_name}."
            )

            cards.append({
                'id': row.get('id'),
                'table': 'users',
                'text': text,
                'department_id': row.get('department_id'),
                'company_id': dept_to_company.get(row.get('department_id')),
                'is_manager': row.get('is_manager', False),
                'active': row.get('is_active', True)
            })

    # Подразделения
    if departments_df is not None:
        df = departments_df.copy()
        for _, row in df.iterrows():
            company_name = companies_map.get(row.get('company_id'), 'Не указана')
            text = (
                f"Подразделение: {row.get('name', '')}. "
                f"Описание: {row.get('description', '')}. "
                f"Компания: {company_name}."
            )
            cards.append({
                'id': row.get('id'),
                'table': 'departments',
                'text': text,
                'company_id': row.get('company_id'),
                'parent_id': row.get('parent_department_id')
            })

    # Компании
    if companies_df is not None:
        df = companies_df.copy()
        for _, row in df.iterrows():
            text = f"Компания: {row.get('name', '')}. Описание: {row.get('description', '')}."
            cards.append({
                'id': row.get('id'),
                'table': 'companies',
                'text': text
            })

    # История задач
    if task_history_df is not None:
        df = task_history_df.copy()
        for _, row in df.iterrows():
            text = (
                f"Задача ID: {row.get('task_id')}. "
                f"Изменено поле: {row.get('field_name')}. "
                f"Старое значение: {row.get('old_value')}. "
                f"Новое значение: {row.get('new_value')}. "
                f"Изменено пользователем: {users_map.get(row.get('changed_by_user_id'), 'Неизвестно')}."
            )
            cards.append({
                'id': row.get('id'),
                'table': 'task_history',
                'text': text,
                'task_id': row.get('task_id'),
                'changed_by': row.get('changed_by_user_id'),
                'changed_at': row.get('changed_at')
            })

    # Зависимости задач
    if task_dependencies_df is not None:
        df = task_dependencies_df.copy()
        for _, row in df.iterrows():
            task1_name = tasks_map.get(row.get('task_id_1'), 'Неизвестна')
            task2_name = tasks_map.get(row.get('task_id_2'), 'Неизвестна')
            text = f"Задача '{task1_name}' зависит от задачи '{task2_name}'."
            cards.append({
                'id': row.get('id'),
                'table': 'task_dependencies',
                'text': text,
                'task_id_1': row.get('task_id_1'),
                'task_id_2': row.get('task_id_2'),
                'created_by': row.get('created_by_user_id'),
                'created_at': row.get('created_at')
            })

    return cards


def save_cards_json(cards: List[Dict], filename: str):
    path = CARDS_DIR / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    print(f"Сохранил {len(cards)} карточек в {path}")


if __name__ == '__main__':
    # Все карточки без фильтров
    all_cards = generate_cards()
    save_cards_json(all_cards, 'all_cards.json')
    # Пример: задачи в работе с высоким приоритетом
    filtered_cards = generate_cards(status=['in_progress'], priority=['high'])
    save_cards_json(filtered_cards, 'tasks_in_progress_high.json')
