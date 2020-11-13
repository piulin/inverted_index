import sys

"""
Program prompt
"""
class teletype(object):


    def __init__(self):
        """
        Informs the user of the required format of the queries.
        """

        print("Please, insert your boolean queries. Admitted queries: [<term> | <term1> <term2>]")

    def request_query ( self ):
        """
        Requests the user a query
        :return: list containing up to two words.
        """

        # request the terms
        inp =  input("q: ")

        # split the queries. 1 term -> single query. 2 terms -> AND query.
        inp = inp.split(" ")

        # if there is something different than expect show an error.
        if len(inp) > 2 or inp[0]  == '' :
            print("Wrong query. Try again.", file=sys.stderr)
            return self.request_query()

        return inp

