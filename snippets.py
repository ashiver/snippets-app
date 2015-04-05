import logging, argparse, sys, psycopg2

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
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """
    Retrieve the snippet with a given name.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "select message from snippets where keyword={!r}".format(name)
    cursor.execute(command)
    message = cursor.fetchone()[0]
    connection.commit()
    logging.debug("Snippet retrieved successfully.")
    return message

def rem(name):
    """
    Delete the snippet with the given name.
    """
    logging.info("Deleting snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "delete from snippets where keyword={!r}".format(name)
    cursor.execute(command)
    connection.commit()
    logging.debug("Snippet deleted successfully.")
    return name

def edt(name, snippet):
    """
    Edits snippet with given name.
    
    If snippet exists, report old snippet and new snippet, ask for confirmation. If confirmation, replace old with new.
    
    If there is no such snippet, report that snippet does not exist.
    """
    logging.error("FIXME: Unimplemented - edt({!r}, {!r})".format(name, snippet))
    return name, snippet

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
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "rem":
        name = rem(**arguments)
        print("Deleted snippet: {!r}".format(name))
    
if __name__ == "__main__":
    main()