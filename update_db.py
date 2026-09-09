import sqlite3


DATABASE = "instance/skilltrack.db"


columns = [
    ("age", "INTEGER"),
    ("gender", "VARCHAR(30)"),
    ("district", "VARCHAR(100)"),
    ("education", "VARCHAR(150)"),
    ("training_program", "VARCHAR(150)"),
    ("training_provider", "VARCHAR(150)"),
    ("training_start_date", "DATE"),
    ("training_completion_date", "DATE"),
    ("certificate_status", "VARCHAR(50)")
]


connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()


# Get existing columns
cursor.execute("PRAGMA table_info(trainees)")

existing_columns = {
    row[1]
    for row in cursor.fetchall()
}


for column_name, column_type in columns:

    if column_name not in existing_columns:

        sql = (
            f"ALTER TABLE trainees "
            f"ADD COLUMN {column_name} {column_type}"
        )

        cursor.execute(sql)

        print(
            f"Added column: {column_name}"
        )

    else:

        print(
            f"Already exists: {column_name}"
        )


connection.commit()

connection.close()


print()
print("Database update completed successfully.")