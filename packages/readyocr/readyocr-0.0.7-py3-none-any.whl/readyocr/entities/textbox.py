from readyocr.entities.bbox import BoundingBox
from readyocr.entities.page_entity import PageEntity


class TextBox(PageEntity):
    """
    To create a new :class:`TextBox` object we need the following

    :param id: Unique identifier of the TextBox entity.
    :type id: str
    :param bbox: Bounding box of the TextBox entity.
    :type bbox: BoundingBox
    :param text: Transcription of the TextBox object.
    :type text: str
    :param confidence: value storing the confidence of detection out of 100.
    :type confidence: float
    """

    def __init__(   
        self,
        id: str,
        bbox: BoundingBox,
        text: str="",
        language: str="",
        confidence: float=0
    ):
        super().__init__(id, bbox)
        self._text = text
        self._language = language
        self.confidence = confidence

    @property
    def text(self) -> str:
        """ 
        :return: Returns the text transcription of the Word entity.
        :type: str
        """
        return self._text
    
    @text.setter
    def text(self, text: str):
        """ 
        Sets the text attribute of the Word entity.

        :param text: Text transcription of the Word entity.
        :type text: str
        """
        self._text = text

    @property
    def language(self) -> str:
        """ 
        :return: Returns the language of the Word entity.
        :type: str
        """
        return self._language
    
    @language.setter
    def language(self, language: str):
        """ 
        Sets the language attribute of the Word entity.

        :param language: Language of the Word entity.
        :type language: str
        """
        self._language = language