import re

class postings_list(object):
    """
    Structure that holds the postings list.
    """


    def __init__(self):
        """
        Initialize the size and an empty mock linked list.
        """

        self.size_ = 0
        self.linked_list_ = []


    def add_document ( self, doc_id ):
        """
        add a document id to the mock linked list.
        :param doc_id:
        :return:
        """

        self.size_ += 1
        self.linked_list_.append( doc_id )

    def linked_list(self):
        """
        :return: Retrieves the linked list.
        """

        return self.linked_list_

    def begin(self):
        """
        :return: Retrieves a front iterator of the mock linked list.
        """

        return iter(self.linked_list_)

    def size(self):
        """
        :return: Current size of the mock linked list.
        """

        return self.size_

    def __str__(self):
        """
        operator <<
        :return: representation of the object as a string.
        """
        return re.sub(r"((,.*){10})", "\\1\n", self.linked_list_.__str__(), 0, re.DOTALL)



