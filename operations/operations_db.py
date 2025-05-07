import csv
import os
from dev_parcial2.data.models import UserCreate, UserOut

CSV_FILE = "users.csv"
FIELDNAMES = ["id", "name", "is_active", "is_premium"]


def init_db():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_all_users():
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_all_users(users):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(users)


def get_new_id(users):
    if users:
        last_id = max(int(user["id"]) for user in users)
    else:
        last_id = 0
    return last_id + 1


def create_user(data: UserCreate) -> UserOut:
    users = read_all_users()
    new_id = get_new_id(users)
    new_user = {
        "id": str(new_id),
        "name": data.name,
        "is_active": "True",
        "is_premium": str(data.is_premium if data.is_premium else False)
    }
    users.append(new_user)
    write_all_users(users)
    return convert_to_response(new_user)


def get_user_by_id(user_id: int) -> UserOut | None:
    users = read_all_users()
    for user in users:
        if int(user["id"]) == user_id:
            return convert_to_response(user)
    return None


def update_user_field(user_id: int, field: str, value: str) -> UserOut | None:
    users = read_all_users()
    updated = None
    for user in users:
        if int(user["id"]) == user_id:
            user[field] = value
            updated = user
            break
    if updated:
        write_all_users(users)
        return convert_to_response(updated)
    return None


def delete_user(user_id: int) -> UserOut | None:
    users = read_all_users()
    deleted = None
    for user in users:
        if int(user["id"]) == user_id:
            user["is_active"] = "False"
            user["is_premium"] = "False"
            deleted = user
            break
    if deleted:
        write_all_users(users)
        return convert_to_response(deleted)
    return None


def filter_users(is_active=None, is_premium=None):
    users = read_all_users()
    filtered = []
    for user in users:
        # Convertimos los valores a booleanos de forma segura
        user_is_active = user.get("is_active", "").lower() == "true"
        user_is_premium = user.get("is_premium", "").lower() == "true"

        if is_active is not None and user_is_active != is_active:
            continue
        if is_premium is not None and user_is_premium != is_premium:
            continue
        filtered.append(convert_to_response(user))
    return filtered


def convert_to_response(user):
    return UserOut(
        id=int(user["id"]),
        name=user["name"],
        is_active=(user["is_active"].lower() == "true"),
        is_premium=(user["is_premium"].lower() == "true")
    )
