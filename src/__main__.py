#!/usr/bin/python3

from bs4 import BeautifulSoup
from book import Book
from difflib import SequenceMatcher
import requests

#List of books
books = []

TEXT_MAIN = r"""
---------------------------------------------------------------------------------------
___       ___    _____   ______     _____     ____   ______       ____     _____  
(  (       )  )  / ___/  (_   _ \   / ____\   / ___) (   __ \     (    )   (  __ \ 
 \  \  _  /  /  ( (__      ) (_) ) ( (___    / /      ) (__) )    / /\ \    ) )_) )
  \  \/ \/  /    ) __)     \   _/   \___ \  ( (      (    __/    ( (__) )  (  ___/ 
   )   _   (    ( (        /  _ \       ) ) ( (       ) \ \  _    )    (    ) )    
   \  ( )  /     \ \___   _) (_) )  ___/ /   \ \___  ( ( \ \_))  /  /\  \  ( (     
    \_/ \_/       \____\ (______/  /____/     \____)  )_) \__/  /__(  )__\ /__\        
---------------------------------------------------------------------------------------
Please select a function:
[s] : search for books by title
[r] : get books by rating
[p] : get books by price
"""

TEXT_AVAILABILITY = """
---------------------------------------------------------------------------------------
Would you like to see books that are not in stock right now?
[y] : Yes
[n] : No
---------------------------------------------------------------------------------------
"""

TEXT_NAME_SEARCH_INPUT = """
---------------------------------------------------------------------------------------
Enter the name of the book you'd like to see!
---------------------------------------------------------------------------------------
"""

TEXT_RATING = """
---------------------------------------------------------------------------------------
What is the minimum rating of books that you would like to see?
---------------------------------------------------------------------------------------
"""

#Creating a list of Book objects based on the information provided by "https://books.toscrape.com/"
def main():


    for i in range(1,51):
        page_to_scrape = requests.get(f"https://books.toscrape.com/catalogue/page-{i}.html")
        soup = BeautifulSoup(page_to_scrape.text,"html.parser")
        ol = soup.find("ol")
        articles = ol.find_all("article",attrs={"class":"product_pod"})

        for article in articles:
            title = article.find("img", attrs={"class":"thumbnail"}).attrs["alt"]
            rating = article.find("p").attrs["class"][1]
            price = article.find("div", attrs={"class":"product_price"}).find("p",attrs={"class":"price_color"}).text[1:]
            price = float(price[1:])
            in_stock = article.find("div", attrs={"class":"product_price"}).find("p",attrs={"class":"instock availability"}).text.strip()
            match rating:
                case "One":
                    rating = 1
                case "Two":
                    rating = 2
                case "Three":
                    rating = 3
                case "Four":
                    rating = 4
                case "Five":
                    rating = 5
                case _:
                    rating = 0
            books.append(Book(title, price, rating, in_stock))

    print(f"Total books scraped: {len(books)}, {books[1].get_name_of_book()}")


    #function/method calls
    selection = menu()
    if selection[0] == "s":
        if selection[1] == "y":
            result = search_for_book(input(TEXT_NAME_SEARCH_INPUT),"y")
            for i in range(0, len(result)):
                print(result[i])
        elif selection[1] == "n":
            result = search_for_book(input(TEXT_NAME_SEARCH_INPUT), "n")
            for i in range(0, len(result)):
                print(result[i])
    elif selection[0] == "r":
        if selection[1] == "y":
            result = books_of_star_rating(int(input(TEXT_RATING)))
            for i in range(0,len(result)):
                print(result[i])
        elif selection[1] == "n":
            result = books_of_star_rating(int(input(TEXT_RATING)))
            for i in range(0,len(result)):
                print(result[i])


#Menu that gives user information about options
#returs: tuple
#[1] : main options (what the user wants to do (only s implemented))
#[2] : stock options (if the user wants to see books that are not available)
def menu()->(str, str):
    main_options = ["s","r","p"]
    stock_options = ["y","n"]
    option = input(TEXT_MAIN)
    if option not in main_options:
        retry_text(1)
    s_option = input(TEXT_AVAILABILITY)
    if s_option not in stock_options:
        retry_text(2)

    return option, s_option

#In the case of the user not providing a useful option this function is called.
#returns: string for the recheck
def retry_text(question:int)->str:
    match question:
        case 1:
            return """
---------------------------------------------------------------------------------------
Input for the main functionality question
is not sufficient please try one of these:
[s] : search for books by title
[r] : get books by rating
[p] : get books by price
---------------------------------------------------------------------------------------
"""
        case 2:
            return """
---------------------------------------------------------------------------------------
Input for the question whether or not you would like to see
books that aren't in stock, is not sufficient please try one of these:
[y] : Yes
[n] : No
---------------------------------------------------------------------------------------
"""

#Gets a list to print
def printer(books_printer:list):
    if not books_printer:
        print("No books found.")
    for book in books_printer:
        print(book)

#Searches for the book that the user inputs, not finished
#returns: list of results
#TODO
def search_for_book(title: str, stock: str) -> list:
    search_list = []
    for book in books:
        book_title = book.get_name_of_book()
        similarity = SequenceMatcher(None, title.lower(), book_title.lower()).ratio()
        if similarity > 0.5555:
            if stock == "y" and book.is_available():
                search_list.append(book)
            elif stock == "n":
                search_list.append(book)
    return search_list

#Method that returns books based on an input of star rating
#returns: list of books
def books_of_star_rating(rating:int)->list:
    list_of_books_with_star_rating = [book for book in books if book.get_rating() == rating]
    return list_of_books_with_star_rating





if __name__ == "__main__":
    main()
