from typing_extensions import Self

from gsuite_meld.gsuite import GoogleAPI


class Sheet(object, metaclass=GoogleAPI, service='sheets', version='v4'):

    def __init__(self):
        self.headers = []
        self.content = []
        self.spreadsheet_id = None

    def __iter__(self):
        yield from self.content

    def download(self, spreadsheet_id: str, worksheet: str) -> Self:
        """
        Download a worksheet (tab) into memory. Can access a row by iterating
        over the object.

        :param spreadsheet_id: file id
        :param worksheet: tab name
        :return:
        """
        res = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=worksheet).execute()
        self.headers = res['values'][0]
        self.content = res['values'][1:]
        self.spreadsheet_id = spreadsheet_id
        return self

    def batch_download(self, spreadsheet_id: str, worksheets: list) -> dict:
        """
        Download multiple worksheets (tabs) using a single batch request.
        """
        res = self.service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id, ranges=worksheets,
            valueRenderOption='FORMATTED_VALUE').execute()
        all_values = {}
        for i, value_range in enumerate(res['valueRanges']):
            if value_range.get('values', None):
                all_values[worksheets[i]] = {
                    'headers': value_range['values'][0],
                    'content': value_range['values'][1:],
                }
        return all_values

    def create(self, body: dict) -> Self:
        """
        Create a new google spreadsheet document in user's root directory
        with given body.
        """
        spreadsheet = self.service.spreadsheets().create(body=body).execute()
        self.spreadsheet_id = spreadsheet['spreadsheetId']
        return self

    def batch_add(self, spreadsheet_id: str, sheet_names: list) -> Self:
        """
        Add multiple worksheets (tabs) with the given sheet names using
        a single batch request.
        """
        body = {
            "requests": []
        }

        for name in sheet_names:
            request = {
                "addSheet": {
                    "properties": {
                        "title": name
                    }
                }
            }
            body["requests"].append(request)

        res = self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        return self

    def clear(self, spreadsheet_id: str, worksheet: str) -> Self:
        """
        Clear all cells of a worksheet (tab).
        """
        spreadsheet = self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=worksheet).execute()
        return self

    def batch_clear(self, spreadsheet_id: str, worksheets: list, body=None) -> Self:
        """
        Clear all cells of muliple worksheets (tabs) using a single batch
        request.
        """
        if body is None:
            body = {
                "ranges": worksheets
            }
        res = self.service.spreadsheets().values().batchClear(
            spreadsheetId=spreadsheet_id, body=body).execute()
        return self

    def update(self, spreadsheet_id: str, worksheet: str, sheet_rows: list, body=None) -> Self:
        """
        Update all cells of a specified worksheet (tab) with given values.
        """
        if body is None:
            body = {
                "range": worksheet,
                "values": sheet_rows
            }
        res = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=worksheet,
            valueInputOption='USER_ENTERED', body=body).execute()
        return self

    def batch_update(self, spreadsheet_id: str, worksheets: list, multiple_sheet_rows: dict,
                     body=None) -> Self:
        """
        Update all cells of multiple worksheets (tabs) with given values.
        """
        if body is None:
            body = {
                "valueInputOption": 'USER_ENTERED',
                "data": [{"range": worksheet, "values": multiple_sheet_rows[worksheet]} for
                         worksheet in worksheets]
            }
        res = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        return self

    def protect(self, spreadsheet_id: str, body=None) -> Self:
        """
        Protect range of a spreadsheet with range specified in body.
        """
        if body is None:
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

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        return self

    def batch_delete(self, spreadsheet_id: str, worksheet_ids: list) -> Self:
        """
        Delete multiple worksheets (tabs) with the given worksheet ids.
        """
        body = {
            "requests": []
        }

        for id in worksheet_ids:
            request = {
                "deleteSheet": {
                    "sheetId": id
                }
            }
            body["requests"].append(request)

        res = self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        return self

    def sheet_list(self, spreadsheet_id: str) -> dict:
        """
        Return a dict of all worksheets (tabs) contained in spreadsheet
        where keys are worksheet (tab) names, and values are sheet ids.
        """
        res = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_lst = {}
        all_sheet_objects = res.get('sheets', [])
        for sheet_object in all_sheet_objects:
            title = sheet_object.get('properties', {}).get('title', None)
            sheet_id = sheet_object.get('properties', {}).get('sheetId', None)
            sheet_lst[title] = sheet_id
        return sheet_lst