from model.entry import entry
from model.postings_list import postings_list
from utils import tokenize
from utils import normalize

"""
Class containing the inverted index data and main operations.
"""
class inverted_index(object):

    def __init__(self, file=None ):
        """
        Creates and empty inverted index when parameter `file` is None.
        :param file: If provided, the object is initialized by indexing the documents inside it.
        """

        self.dict_ = {}

        self.docs_ = []

        if (file != None):


            # Initialize the inverted index
            self.index(file)


    def index (self, filename):
        """
        Initializes the inverted index given a file with documents.
        :param filename: CSV with one document per row. Format: <id>\t<url>\t<pub_date>\t<title>\t<document_content>\n
        """

        # retrieve the overall sorted term list
        alltermsid_index = self.create_sorted_token_ids_index( filename )

        # Initialize the dictionary and postings lists from the sorted term list.
        self.build_inverted_index( alltermsid_index )



    def create_sorted_token_ids_index ( self, filename ):
        """
        Create a sorted term list from all documents in a CSV.
        :param filename: CSV with one document per row.
        :return: sorted term list.
        """

        # sorted term list
        alltermsid = []

        # open the CSV file
        with open(filename, "r") as fp:

            # discard the header
            fp.readline()

            # iterate the lines
            for line in fp:

                # retrieve the data and metadata of each document
                id, url, pub_date, title, content = line.split("\t")


                # tokenize the content of the document.
                tokens = tokenize(content)

                # normalize the tokens
                terms = normalize(tokens)

                # add them to the term list (not sorted yet)
                alltermsid.extend([[term, int(id)] for term in terms])

        # this is quite expensive
        alltermsid.sort()

        return alltermsid

    def build_inverted_index (self, alltermsid_index ):
        """
        Initializes the inverted index from a sorted term list.
        :param alltermsid_index: sorted term list.
        """

        # Assign values of the first iteration and create the first entry of the dictionary.
        first_term, first_id = alltermsid_index[0]
        prev_term = first_term
        curr_entry = entry(first_term)
        curr_entry.add_document(first_id)

        # Loop all the terms in the sorted term list, starting from the second term.
        for term, id in alltermsid_index[1:]:

            # if the term is the same as the previous one, just add the document id to the the postings list of the current entry.
            if prev_term == term:

                curr_entry.add_document(id)


            # We are done with the current entry, set up the next one
            else:

                # Add the current entry using the last term as key.
                self.dict_[prev_term] = curr_entry

                # update
                prev_term = term

                # set up a new entry for the new term
                curr_entry = entry(term)
                curr_entry.add_document(id)

        # the last entry is assigned here.
        self.dict_[prev_term] = curr_entry

    def query(self, term1, term2 = None):

        """
        Performs a boolean query of `term1` in the inverted index. If term2 is also provided, then it performs a logic AND
        query of `term1` and `term2` in the inverted index.
        :param term1: Term to be searched.
        :param term2: Optionally second term of the AND query.
        :return:
        """

        # AND query branch
        if  term2 != None:

            return self.query_and_(term1,term2)

        else:

            return self.query_(term1)


    def query_ ( self, term ):
        """
        Retrives the postings list of `term`. If term is not found, then `None` is returned.
        :param term: term to be searched
        :return: postings list.
        """
        try:

            return self.dict_ [ term ].postings_list()

        except :

            return postings_list()

    def query_and_ (self, term1, term2):

        """
        Performs an AND query in the inverted list. I
        :param term1: Left argument of the AND.
        :param term2: Right argument of the AND.
        :return: intersected postings list.
        """

        # create the an empty postings list to store the result.
        result = postings_list()

        # try to retrieve the postings list for each term
        try:

            pl1 =  self.dict_[ term1 ].postings_list()
            pl2 =  self.dict_[ term2 ].postings_list()

        # If it's not possible for either of them, then the intersection is just empty.
        except:

            return result

        # Otherwise, iterate the elements of the postings list and do the intersection
        try:

            # iterator of the postings list of term1
            it1 = pl1.begin()
            # first document id in the postings list of term1
            doc1 = next(it1)
            # iterator of the postings list of term2
            it2 = pl2.begin()
            # first document id in the postings list of term2
            doc2= next(it2)

            # Iterate postings lists.
            while True:

                # if documents match, then add that document to the result and move the pointers forward.
                if doc1 == doc2:

                    result.add_document( doc1 )
                    doc1 = next( it1 )
                    doc2 = next( it1 )

                # if doc1's id is higher than doc2's, get the next document id of term2.
                elif doc1 > doc2:

                    doc2 = next( it2 )

                # otherwise do the opposite.
                else:
                    doc1 = next( it1 )

        # If you reach the end of any list, just return the current result.
        except StopIteration:
            pass

        return result

