from src.database.db import engine, Base
from src.database import models

def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("================================")
    print("INSURANCE UNDERWRITING SYSTEM")
    print("================================")
    print("Database created successfully!")
    print("All tables are ready.")

if __name__ == "__main__":
    initialize_database()