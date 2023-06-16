import sqlite3

# Create a connection to the database
connection = sqlite3.connect('my_database.db')

# Create a cursor object
cursor = connection.cursor()

# Create a table
cursor.execute('CREATE FRIDAY_SCANS users (name TEXT, email TEXT)')

# Insert some data
cursor.execute('INSERT INTO users (name, email) VALUES ("John Doe", "johndoe@example.com")')
cursor.execute('INSERT INTO users (name, email) VALUES ("Jane Doe", "janedoe@example.com")')

# Commit the changes
connection.commit()

# Close the connection
connection.close()