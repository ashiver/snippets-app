import logging, argparse, sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.
    
    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """
    Retrieve the snippet with a given name.
    
    If there is no such snippet, report that snippet does not exist.
    
    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def rem(name):
    """
    Delete the snippet with the given name.
    
    If snippet exists, report snippet and asks for confirmation. If confirmation, delete snippet.
    
    If there is no such snippet, report that snippet does not exist.
    """
    logging.error("FIXME: Unimplemented - rem({!r})".format(name))
    return ""

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
    
    arguments = parser.parse_args(sys.argv[1:])
    
if __name__ == "__main__":
    main()