import json
from typing import Union as U
from typing_extensions import Self

from gsuite_meld.gsuite import GoogleAPI


class Document(object, metaclass=GoogleAPI, service='docs', version='v1'):

    def __init__(self, document_id: U[str, None] = None):
        self.document_id = document_id
        self.content = []

    def __iter__(self):
        # return the content of the next line
        yield from map(self._read_structural_element, self.content)

    def as_txt(self) -> str:
        # return the entire content of document as a blob of text
        return str.join('', self)

    def as_json(self):
        # return the entire content of document as a python dict
        return json.loads(self.as_txt())

    def create(self, document_name: str) -> Self:
        # create a new google document in user's root directory
        body = {'title': document_name}
        doc = self.service.documents().create(body=body).execute()
        self.document_id = doc['documentId']
        return self

    def download(self, document_id: U[str, None] = None) -> Self:
        # load document content into memory
        if not document_id:
            document_id = self.document_id
        doc = self.service.documents().get(documentId=document_id).execute()
        self.document_id = document_id
        self.content = doc.get('body', {}).get('content', [])
        return self

    def upload(self, content: str, document_id: U[str, None] = None) -> Self:
        """
        Overwrite current document's content with given `content`.

        :param document_id: document_id or use self assigned document id
        :param content: str
        """
        if not document_id:
            document_id = self.document_id
        doc = self.service.documents().get(documentId=document_id).execute()
        elements = doc.get('body', {}).get('content', [])
        requests = [{'deleteContentRange': {
            'range': {
                'startIndex': 1,
                'endIndex': elements[-1]['endIndex'] - 1,
            }
        }}] if elements[-1]['endIndex'] > 2 else []
        requests.append(
            {'insertText': {
                'location': {'index': 1},
                'text': content
            }}
        )
        self.service.documents().batchUpdate(
            documentId=self.document_id, body={'requests': requests}).execute()
        return self

    def _read_structural_element(self, element):
        # read the content of a single element
        text = ''
        if 'paragraph' in element:
            elements = element['paragraph']['elements']
            for elem in elements:
                text += self._read_paragraph_element(elem)
        elif 'table' in element:
            # The text in table cells are in nested Structural Elements and
            # tables may be nested.
            table = element['table']
            for row in table['tableRows']:
                cells = row['tableCells']
                for cell in cells:
                    text += self._read_structural_elements(cell['content'])
        elif 'tableOfContents' in element:
            # The text in the TOC is also in a Structural Element.
            toc = element['tableOfContents']
            text += self._read_structural_elements(toc['content'])
        return text

    def _read_structural_elements(self, elements):
        """
        Recurses through a list of Structural Elements to read a google doc's
        text where text may be in nested elements.
        """
        text = ''
        for element in elements:
            text += self._read_structural_element(element)
        return text

    def _read_paragraph_element(self, element):
        # Returns the text in the given ParagraphElement.
        text_run = element['textRun']
        if not text_run:
            return ''
        return text_run['content']