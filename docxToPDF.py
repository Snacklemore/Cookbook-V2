import aspose.words as aw
import glob

# Define the directory where you want to search for .doc and .docx files
directory_path = "E:\\Cookbook V2\\Recepts_docx"

# Store all the .docx and .doc files in a list
doc_files = []
for file in glob.glob(directory_path + "/*.docx"):
    doc_files.append(file)
for file in glob.glob(directory_path + "/*.doc"):
    doc_files.append(file)

# Print the list of .docx and .doc files
print("List of .docx and .doc files:")
counter = 0
for doc_file in doc_files:
    counter = counter +1 
    print(doc_file)
    doc = aw.Document(doc_file)
    doc.save(doc_file+".pdf")
    
print("Converted " + str(counter) + " files to .pdf")
