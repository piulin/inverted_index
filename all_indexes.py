from model.entry import entry
from model.postings_list import postings_list
from utils import tokenize
from utils import normalize
from itertools import permutations, product


"""
Class containing the inverted index data and main operations.
"""
class Indexes(object):

    def __init__(self, file=None ):
        """
        Creates and empty inverted index when parameter `file` is None.
        :param file: If provided, the object is initialized by indexing the documents inside it.
        """

        self.inverted = {}
        self.docs_ = []
        self.permuterm = {}

        if (file != None):

            # Initialize the inverted index
            self.index(file)

            # Initialize permuterm index
            self.build_permuterm_index()


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
        with open(filename, "r", encoding='utf-8') as fp:

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
                self.inverted[prev_term] = curr_entry

                # update
                prev_term = term

                # set up a new entry for the new term
                curr_entry = entry(term)
                curr_entry.add_document(id)

        # the last entry is assigned here.
        self.inverted[prev_term] = curr_entry

    # Build dictionary mapping rotations of the wildcard to each term
    def build_permuterm_index(self):
        terms = list(self.inverted.keys())
        symbol = '$'

        for t in terms:
            start = 0
            end = len(t)

            while start != len(t) + 1:
                rotation = t[start:end] + symbol + t[:start]
                self.permuterm[rotation] = t
                start += 1
                end += 1

    def permuterm_lookup(self, term):

        matches = []

        # Find position(s) of wildcard(s)
        wildcard_position = [pos for pos, char in enumerate(term) if char == '*']

        # Remove wildcard symbol to look up in permuterm index
        term1_clean = term.replace('*', '')

        # *X* --> X*
        if len(wildcard_position) > 1:
            for key, value in self.permuterm.items():
                if key.startswith(term1_clean):
                    matches.append(value)
        else:
            wildcard_position = wildcard_position[0]
            # X* --> $X*
            if wildcard_position == len(term) - 1:
                for key, value in self.permuterm.items():
                    lookup = '$' + term1_clean
                    if key.startswith(lookup):
                        matches.append(value)
            # *X --> X$*
            elif wildcard_position == [0]:
                for key, value in self.permuterm.items():
                    lookup = term1_clean + '$'
                    if key.startswith(lookup):
                        matches.append(value)
            # X*Y --> Y$X*
            else:
                lookup = term[int(wildcard_position):] + '$' + term[:int(wildcard_position)]
                # Clean again, because we used the original query term with the wildcard in previous step
                lookup_clean = lookup.replace('*', '')
                for key, value in self.permuterm.items():
                    if key.startswith(lookup_clean):
                        matches.append(value)

        return matches

    def query(self, term1, term2 = None):

        """
        Performs a boolean query of `term1` in the inverted index. If term2 is also provided, then it performs a logic AND
        query of `term1` and `term2` in the inverted index.
        :param term1: Term to be searched.
        :param term2: Optionally second term of the AND query.
        :return:
        """

        # AND query branch
        if term2 is not None:

            terms = [term1, term2]
            wildcards = False
            permuterm_matches = {}

            # Check if wildcards present in query
            for t in terms:
                if '*' in t:
                    wildcards = True
                    perm_t = self.permuterm_lookup(t)
                    permuterm_matches[t] = perm_t
                else:
                    # If no wildcard, add to dict as is, in order to enable user to have wildcard in of the two terms
                    permuterm_matches[t] = [t]

            # If no wildcard was found, perform usual "AND" query
            if wildcards is False:
                return self.query_and_(term1, term2)

            else:
                # Retrieve postings results for all combinations of wildcard matches for term1 and term2
                results = []
                for t1, t2 in product(permuterm_matches[term1], permuterm_matches[term2]):
                    postings = self.query_and_(t1, t2)
                    if postings.size_ != 0:
                        results.append(postings.linked_list_)
                return results

        else:
            # Check if there is a wildcard in term1
            if '*' in term1:
                permuterm_matches = self.permuterm_lookup(term1)
                results = []
                for t in permuterm_matches:
                    postings = self.query_(t)
                    results.append(postings.linked_list_)
                return results

            return self.query_(term1)

    def query_ ( self, term ):
        """
        Retrives the postings list of `term`. If term is not found, then `None` is returned.
        :param term: term to be searched
        :return: postings list.
        """
        try:

            return self.inverted [ term].postings_list()

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

            pl1 =  self.inverted[ term1].postings_list()
            pl2 =  self.inverted[ term2].postings_list()

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


""" These seem to be working
index = Indexes('postillon.csv')

query_result1 = index.query('*wasser', 'Wasser*')
query_result2 = index.query('*wasser*', 'Wa*ser')
"""
