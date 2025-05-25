from .database_setup import get_database_connection, print_all
from typing import List, Tuple

def add_user(discord_id: str, steam_id : str):
    cursor, connection = get_database_connection()
    cursor.execute("INSERT INTO users (discord_id, steam_id) VALUES (%s, %s)",(discord_id, steam_id))
    connection.commit()
    print_all()
    cursor.close()
    connection.close()

def user_registered(discord_id : str):
    cursor, connection = get_database_connection()
    cursor.execute("SELECT steam_id FROM users WHERE discord_id = %s;", (str(discord_id),))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    return None

def add_score(discord_id : str, score : int):
    cursor, connection = get_database_connection()
    cursor.execute("""
                UPDATE users 
                SET score = %s, last_updated = NOW()
                WHERE discord_id = %s::text
                """,
                (score, discord_id))
    connection.commit()
    print_all()
    cursor.close()
    connection.close()

def get_score(discord_id: str) -> int:
    cursor, connection = get_database_connection()
    cursor.execute("""
                SELECT score
                FROM users
                WHERE discord_id = %s::text
                """,
                (discord_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    
def get_steam_id(discord_id: str)-> str:
    cursor, connection = get_database_connection()
    cursor.execute("""
                   SELECT steam_id
                   FROM users
                   WHERE discord_id = %s::text 
                   """,
                   (discord_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    
def get_steam_ids_sorted_by_points() -> List[Tuple[str, int]]:
    cursor, connection = get_database_connection()
    cursor.execute("""
                   SELECT steam_id, CAST(score as INTEGER) as score_int
                   FROM users
                   WHERE score IS NOT NULL
                   ORDER BY score_int DESC
                   """)
    result = cursor.fetchall()
    connection.close()
    return result

def remove_user(discord_id : str):
    cursor, connection = get_database_connection()
    cursor.execute("""
                   DELETE FROM users
                   WHERE discord_id = %s
                   """, (str(discord_id),))
    connection.commit()
    cursor.close()
    connection.close()