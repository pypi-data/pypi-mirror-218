# gsuite-meld
'gsuite-meld' is an Python package designed to facilitate seamless integration with a variety of GSuite services, 
including Google Sheets, Docs, and Drive, and is extensible to accommodate future GSuite additions. 
The package leverages the power of Python's metaclasses to simplify interfacing with Google APIs, 
thus allowing users to effortlessly build and manage multi-service workflows.

## Core Features
- **Unified GSuite Interface:** Our package encapsulates the functionality of Google Sheets, Google Docs, and Google Drive into three primary classes: Sheet, Document, and Drive. These classes are endowed with a rich set of methods, enabling users to handle various operations such as downloads, uploads, deletions, and updates.
- **Batch Operations:** We recognize that efficiency is paramount in managing your data. Therefore, we've designed gsuite-meld to perform operations in batches, providing significant time savings for large-scale data handling.
- **Iterative Content Access:** With gsuite-meld, users can iterate over the content of sheets and documents, thus simplifying data manipulation within the Python environment.
- **Dynamic API Builder:** The GoogleAPI metaclass dynamically builds the API service needed for each object. This feature takes advantage of Python's metaclass capabilities to reduce the redundancy in API creation and to keep the codebase clean and efficient.
- **Flexible Credentials Management:** To ensure secure and flexible integration, gsuite-meld requires users to supply GSuite credentials, which can be provided as a file, a dictionary, or a JSON parseable string set as an environment variable.

# Limitations
- Gsuite-meld is not a general-purpose Google API package; it specifically targets GSuite services.
- While we strive to cover a wide range of functions, some more complex features may not be supported by this package.
- Users need to be familiar with Google Sheets, Google Docs, and Google Drive IDs and understand how to obtain them.

Overall, gsuite-meld offers a user-friendly and effective way to navigate the diverse ecosystem of GSuite services. Whether you're managing data in Sheets, creating documents, or organizing files on Drive, gsuite-meld can streamline your workflow.

# Requirements
- Python 3.6 or higher
- google-auth 1.6.3 or higher
- google-auth-httplib2 0.0.3 or higher
- google-auth-oauthlib 0.4.1 or higher
- google-api-python-client 1.7.11 or higher

# Installation
- Use the package manager pip to install gsuite_meld.

```bash
pip install gsuite_meld
```

# Usage
The `gsuite_meld` package contains tree modules: `Sheet`, `Document` and `Drive`.

## Drive.py
```python
from gsuite_meld import Drive

drive = Drive()
drive.download_file("file_id", "/path/to/save")
```

## Document.py
```python
from gsuite_meld import Document

doc = Document() # Create an instance of the Document class
doc.create("My New Document") # Create a new Google Document with a specified name
doc.download() # Download the contents of the newly created document into memory
```

### Creating Multiple Documents:
```python
for i in range(5):
    doc.create(f"My Document {i+1}")
```

### Getting a Document's JSON Representation:
```python
doc.create("My New Document")
doc.download()
json_content = doc.as_json()
print(json_content)
```

### Overwriting Multiple Documents with New Content:
```python
document_ids = ["id1", "id2", "id3"]
new_content = "This is the new content of the document"
for document_id in document_ids:
    doc.upload(content=new_content, document_id=document_id)
```

### Combining Multiple Documents' Content into One Document:
```python
document_ids = ["id1", "id2", "id3"]
combined_content = ""
for document_id in document_ids:
    doc.download(document_id=document_id)
    combined_content += doc.as_txt()
doc.create("Combined Document")
doc.upload(content=combined_content)
```

### Accessing the Content of a Document Line by Line:
```python
doc.create("My New Document")
doc.upload("Line 1\nLine 2\nLine 3")
doc.download()
for line in doc:
    print(line)
```

## Sheet.py
```python
from gsuite_meld import Sheet

sheet = Sheet()
sheet.download("spreadsheet_id", "worksheet_name")
```

### Download a Worksheet:
```python
sheet = Sheet()
sheet.download("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", "Data")
```

### Download Multiple Worksheets:
```python
sheet = Sheet()
sheets_content = sheet.batch_download("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", ["Data", "Description"])
```

### Create a Google Spreadsheet:
```python
sheet = Sheet()
body = {
    'properties': {
        'title': 'New Google Sheet'
    }
}
sheet.create(body)
```

### Add Multiple Worksheets:
```python
sheet = Sheet()
sheet.batch_add("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", ["Worksheet 1", "Worksheet 2"])
```

### Clear a Worksheet:
```python
sheet = Sheet()
sheet.clear("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", "Worksheet 1")
```

### Update a Worksheet:
```python
sheet = Sheet()
new_data = [['John', 'Doe', '123 Street', 'City'], ['Jane', 'Doe', '456 Street', 'City']]
sheet.update("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", "Worksheet 1", new_data)
```

### Protect a Worksheet:
```python
sheet = Sheet()
body = {
    "requests": [
        {
            "addProtectedRange": {
                "protectedRange": {
                    "range": {
                        "sheetId": 1,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1
                    },
                    "description": "Protecting date column from changes.",
                    "warningOnly": True,
                }
            }
        }
    ]
}
sheet.protect("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", body)
```

### Delete Multiple Worksheets:
```python
sheet = Sheet()
sheet.batch_delete("1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms", [0, 1])
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# License
Apache 2.0