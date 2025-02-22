class Book:
    title = "title of the book"
    price = 0
    like_dislike = 0
    in_stock = "N/A"

    #Constructor
    #title: string of book title
    #price: float of price of book
    #star_rating: int of star rating of book
    #in_stock:
    def __init__(self, title:str, price:float, star_rating:int, in_stock):
        self.title = title
        self.price = price
        self.star_rating = star_rating
        self.in_stock = in_stock

    def get_name_of_book(self)->str:
        return f"{self.title}"

    def is_available(self)->bool:
        return True

    #Future project where the user can decide if they like a product or not
    #TODO
    def set_like_dislike(self, like_dislike):
        match like_dislike:
            case "y":
                self.like_dislike = 1
            case "n":
                self.like_dislike = -1

    #__str__ of Book class, needs work
    #TODO
    def __str__(self):
        return f"{self.title}\n\xa3 {self.price}\nStar rating: {self.star_rating}\n{self.in_stock}"
