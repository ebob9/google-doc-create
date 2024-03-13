#!/usr/bin/env python3

# taken from https://ericmjl.github.io/blog/2023/3/8/how-to-automate-the-creation-of-google-docs-with-python/

import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from markdown import markdown


def document_template(content: dict):
    template_text = f"""# My Google Doc!

## Abstract

This is some introductory text.
We could have lorem ipsum'd it,
but that would be too generic for my tastes.
So instead, I have chosen to write freely from my mind.

## Section 1

- First bullet point
- Second bullet point

<hr class="pb">

## Section 2

{content["lorem ipsum"]}

| hello | world |
|:-----:|:-----:|
|  1  |  a  |
|  2  |  b  |

<hr class="pb">

"""
    return template_text


GOOGLE_CREDENTIAL_FILENAME = os.path.expanduser("~/.gdrive/creds.json")

settings = {
    "client_config_backend": "service",
    "service_config": {
        "client_json_file_path": GOOGLE_CREDENTIAL_FILENAME,
    }
}

gauth = GoogleAuth(settings=settings)
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

root_content = {"lorem ipsum": "Lorem ipsum dolor sit amet."}
text = document_template(root_content)
htmldoc = markdown(text, extensions=['tables'])

# print(htmldoc)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))

gdoc = drive.CreateFile(
    {
        "title": "My Shiny New Google Doc from Python!",
        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        # application/vnd.google-apps.document
        # "id": "file-id-here"  # to edit file, overwrite doc-id.
    }
)
gdoc.SetContentString(htmldoc)

gdoc.Upload({"convert": True})

# clone perms
# oldfile = drive.CreateFile({"id": "<doc id to clone>"})
# oldfile_permissions = oldfile.GetPermissions()
# print(oldfile['permissions'])
#
# for perm in oldfile_permissions:
#     gdoc.InsertPermission(perm)

# print(gdoc["alternateLink"])
# should give you a https:// URL to the doc!

# delete a file
# delfile = drive.CreateFile({"id": "<file id here>"})
# delfile.Delete()

# Most permissive
gdoc.InsertPermission({"type": "anyone", "role": "writer", "value": "anyone"})

# Write-access to specific email addresses
# email_addresses = ("first@person.email", "second@person.email",...)
# for email in email_addresses:
#     gdoc.InsertPermission({"type": "user", "role": "writer", "value": email})

