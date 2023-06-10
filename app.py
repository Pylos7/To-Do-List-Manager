from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Establish a database connection
# Replace 'your_database_url' with the actual URL of your database
engine = create_engine('models.py')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session object
session = Session()
