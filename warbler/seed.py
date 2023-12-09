"""Seed the database"""
# DATABASE     : From CLI type createdb warbler
# MAIN DIR     : cd <path/to/warbler/main/dir>
# SEED         : from CLI python3 seed.py
# STOP SERVER  : ctrl c to stop server

# Note: there is logic that auto starts the server after seeding

# to rerun server, either:
# python3 seed.py (This will drop all data and start fresh)
# or 
# flask run -p 8801 (This will not drop data and you can continue)

import sys
from csv import DictReader  
from models import db, User, Message, Follows
from app import app

# Seed database
with app.app_context():
    if db is None:
        db.create_all("warbler")
    else:
        db.drop_all()
        db.create_all()
    
    # Insert data from CSV files into tables
    with open('generator/users.csv') as users:
        db.session.bulk_insert_mappings(User, DictReader(users))

    with open('generator/messages.csv') as messages:   
        db.session.bulk_insert_mappings(Message, DictReader(messages))

    with open('generator/follows.csv') as follows:
        db.session.bulk_insert_mappings(Follows, DictReader(follows))

    # Commit changes
    db.session.commit() 

# Start web server
    try:
        app.run(host='127.0.0.1', port=8800, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    sys.exit()





