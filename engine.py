from all_indexes import Indexes
from teletype import teletype

"""
Defines the main logic of the program
"""
class engine(object):

    def __init__(self, args ):
        """
        Sets up the inverted index
        :param args: command-line arguments
        """
        self.args_ = args
        self.ii_ = Indexes(args['documents'])


    def run(self) :
        """
        Ansers command-line queries or interactive queries.
        """

        # Check out command-line queries
        if ( self.args_ [ 'q' ] != None ):


            # loop the queries
            for query in self.args_ [ 'q' ]:


                self.solve_query( query.split(" ") )

            exit(0)

        else:

            # Set up a prompt
            tt = teletype()

            while True:

                # Request interactively queries to user
                query = tt.request_query ( )

                self.solve_query( query )


    def solve_query ( self, query ):
        """
        Queries the inverted index.
        :param query: list containing up to two terms being queried.
        """

        # Obtain the resulting postings list of the query
        pl = self.ii_.query(*query)

        # Show it to the user.
        print(f"Query: \"{query}\". Postings list: {pl}")



