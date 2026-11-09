from src.database.db import engine, Base
from src.database import models

Base.metadata.create_all(bind=engine)

print("Insurance database created successfully!")
print("All tables are ready.")