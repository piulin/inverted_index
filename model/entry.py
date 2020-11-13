from model.postings_list import postings_list


class entry(object):
    """
    Defines each entry of the dictionary. As it is, it's not very useful. It decouples the postings list from the actual entry.
    """


    def __init__(self, term):
        """
        Creates an empty postings list and assigns the term to the entry.
        :param term:
        """

        self.term_ = term
        self.postings_list_ = postings_list()


    def add_document(self, doc_id):
        """
        Adds a document id to the postings list.
        :param doc_id: document id
        """

        self.postings_list_.add_document( doc_id )


    def postings_list(self):
        """
        :return: Posting list.
        """

        return self.postings_list_