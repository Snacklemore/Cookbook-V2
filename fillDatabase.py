import psycopg2
import glob
import os
from db import conn
# Establish a connection to the PostgreSQL database
#redacted

# Define the directory where you want to search for .pdf files
directory_path = "E:\\Cookbook V2\\Recepts_pdf"

# Store all the .docx and .doc files in a list
pdf_files = [] #NO FILEPOINTER ! STRING/Path
for file in glob.glob(directory_path + "/*.pdf"):
    pdf_files.append(file)

# Print the list of .docx and .doc files
print("List of .pdf files:")
counter = 0
for pdf_file in pdf_files:
    counter = counter +1 
    print(pdf_file)
    
    # Open the PDF file
    with open(pdf_file, 'rb') as pdf_file:
        file_name = os.path.basename(pdf_file.name)
        print( os.path.basename(pdf_file.name))
        pdf_data = pdf_file.read()

    # Insert the PDF data into the database
    cur = conn.cursor()
    vals = [(psycopg2.Binary(pdf_data),file_name)]
    cur.execute("CREATE TABLE IF NOT EXISTS pdf_storage (id SERIAL PRIMARY KEY, name VARCHAR(150), pdf_data BYTEA)")
    cur.executemany("INSERT INTO pdf_storage (pdf_data,name) VALUES (%s,%s)", vals)
    

    # Commit the transaction and close the connection
    conn.commit()
cur.close()
conn.close()