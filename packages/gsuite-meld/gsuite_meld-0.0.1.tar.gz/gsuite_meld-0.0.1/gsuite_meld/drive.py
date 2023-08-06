import io
from typing import Union as U, NoReturn, List

from googleapiclient.http import MediaIoBaseDownload
from typing_extensions import Self

from gsuite_meld.gsuite import GoogleAPI


class Drive(object, metaclass=GoogleAPI, service='drive', version='v3'):

    def download_file(self, file_id: str, filepath: str) -> NoReturn:
        """
        Download a file given its file id.

        Note that Google Drive handles different file types in different ways.
        Google Drive files (Docs, Sheets, Slides, etc.) need to be handled by
        'Document', 'Sheet', etc.

        Other file types (pdf, jpg, txt, etc.) can be downloaded directly.

        :param file_id: id of the file to download
        :param filepath: path to save the file to
        """
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.close()

    def get_id(self, filename: str, folder: U[str, None] = None) -> str:
        """
        Find a file in GDrive by file name in an (optional) folder id.

        Returns the file id of first match or Raise IndexError if not found.

        :param filename: file name
        :param folder:  folder id
        :return: file id
        """
        params = {
            'q': f'name="{filename}" and trashed=false',
            'supportsAllDrives': True,
            'includeItemsFromAllDrives': True,
        }
        if folder:
            params['q'] += f' and parents in "{folder}"'
        res = self.service.files().list(**params).execute()
        return res['files'][0]['id']

    def get_parent(self, file_id: str) -> str:
        """
        Get the given file's parent folder id.

        Returns the parent id or Raise IndexError if not found.

        :param file_id: file id
        :return: parent id
        """
        res = self.service.files().get(fileId=file_id,
                                       supportsAllDrives=True,
                                       fields='parents').execute()
        return res['parents'][0]

    def grant_permissions(self, file_id, permission=None) -> Self:
        """
        Grant access and edit permissions to specified file.

        :param file_id: id of the file to grant access and edit permissions.
        :permission: dictionary containing permission parameters.
        """
        if permission is None:
            permission = {
                'type': 'anyone',
                'value': 'anyone',
                'role': 'writer'}

        self.service.permissions().create(
            fileId=file_id, body=permission, supportsAllDrives=True).execute()
        return self

    def list_files_in_folder(self, folder_id: str) -> List[dict]:
        """
        Lists all files in a specified folder.

        :param folder_id: Id of the folder to list files.
        :return: A list of file dictionaries.
        """
        query = f"'{folder_id}' in parents and trashed=false"
        params = {
            'q': query,
            'supportsAllDrives': True,
            'includeItemsFromAllDrives': True,
        }
        res = self.service.files().list(**params).execute()
        return res['files']

    def move_file_to_folder(self, file_id: str, folder_id: str) -> NoReturn:
        """
        Move specified file to the specified folder.

        :param file_id: Id of the file to move.
        :param folder_id: Id of the folder
        """
        # Retrieve the existing parents to remove
        file = self.service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        file = self.service.files().update(fileId=file_id, addParents=folder_id,
                                           supportsAllDrives=True,
                                           removeParents=previous_parents,
                                           fields='id, parents').execute()
        assert folder_id == file['parents'][0], f'mv failed: {file_id} -> {folder_id}'
