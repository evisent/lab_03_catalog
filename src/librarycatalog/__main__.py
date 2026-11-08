import argparse
import sys
  
from .catalog import Catalog
from .errors import CatalogError
from .models import make_book
from .storage import load_catalog, save_catalog
  
  
def main(argv=None):
    parser = argparse.ArgumentParser(prog="librarycatalog")
    sub = parser.add_subparsers(dest="command", required=True)
   
    p_add = sub.add_parser("add", help="add book")
    p_add.add_argument("--file", required=True)
    p_add.add_argument("--id", required=True)
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--year", required=True, type=int)
    p_add.add_argument("--author", required=True)
    p_add.add_argument("--isbn", required=True)
  
    p_list = sub.add_parser("list", help="list all books")
    p_list.add_argument("--file", required=True)
  
    p_get = sub.add_parser("get", help="get book by id")
    p_get.add_argument("--file", required=True)
    p_get.add_argument("--id", required=True)
  
    p_remove = sub.add_parser("remove", help="remove book by id")
    p_remove.add_argument("--file", required=True)
    p_remove.add_argument("--id", required=True)
  
    p_find = sub.add_parser("find", help="find by name or category")
    p_find.add_argument("--file", required=True)
    p_find.add_argument("--name")
    p_find.add_argument("--category")
  
    args = parser.parse_args(argv)
  
    catalog = Catalog()
    try:
        load_catalog(catalog, args.file)
    except CatalogError:
        pass
  
    try:
        if args.command == "add":
            book = make_book(
                args.id, args.title, args.category,
                args.year, args.author, args.isbn,
            )
            catalog.add(book)
            save_catalog(catalog, args.file)
            print("added:", book.id)
  
        elif args.command == "list":
            for book in catalog:
                print(book.id, "|", book.title, "|", book.author)
  
        elif args.command == "get":
            book = catalog.get(args.id)
            print(book)
  
        elif args.command == "remove":
            catalog.remove(args.id)
            save_catalog(catalog, args.file)
            print("removed:", args.id)
  
        elif args.command == "find":
            if args.name:
                for book in catalog.find_by_name(args.name):
                    print(book.id, "|", book.title)
            elif args.category:
                for book in catalog.find_by_category(args.category):
                    print(book.id, "|", book.title)
            else:
                print("error: specify --name or --category", file=sys.stderr)
                return 2
  
    except CatalogError as e:
        print("error:", e, file=sys.stderr)
        return 2
  
    return 0
  
  
if __name__ == "__main__":
    raise SystemExit(main())
  