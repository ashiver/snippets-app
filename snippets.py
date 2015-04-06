import logging, argparse, sys, psycopg2, os

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet):
    """
    Store a snippet with an associated name.
    """
    logging.info("Storing snippet {!r}: {!r})".format(name, snippet))
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
    except psycopg2.IntegrityError:
        with connection, connection.cursor() as cursor:
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """
    Retrieve the snippet with a given name.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name, ))
        message = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    if not message:
        return "no snippet named {!r}.".format(name)
    else:
        return "{!r}.".format(message[0])

def rem(name):
    """
    Delete the snippet with the given name.
    """
    logging.info("Deleting snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name, ))
        message = cursor.fetchone()
    if not message:
        logging.debug("Tried to delete snippet. No snippet by that name.")
        return "no snippet named {!r}.".format(name)
    else:
        with connection, connection.cursor() as cursor:
            cursor.execute("delete from snippets where keyword={!r}".format(name))
        logging.debug("Snippet deleted successfully.")
        return "deleted snippet with name {!r}.".format(name)
    
def catalog():
    """
    Displays all snippet names.
    """
    logging.info("Displaying all snippet names")
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets order by keyword asc")
        names = []
        output = cursor.fetchall()
        for tup in output:
            names.append(tup[0])
    return names

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    # Subparser for the rem command
    logging.debug("Constructing rem subparser")
    rem_parser = subparsers.add_parser("rem", help="Delete a snippet")
    rem_parser.add_argument("name", help="The name of the snippet")
    
    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Display all snippet names")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Snippets: stored snippet {!r} under name {!r}.".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Snippets: " + snippet)
    elif command == "rem":
        name = rem(**arguments)
        print("Snippets: " + name)
    elif command == "catalog":
        names = catalog(**arguments)
        print("Snippets: " + ' '.join(names))
    
if __name__ == "__main__":
    main()
    os.popen("rm ~/thinkful/projects/snippets-app/snippets.log") # Deletes log file if main succeeds