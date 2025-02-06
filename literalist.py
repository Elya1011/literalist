import sqlalchemy as sq, os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, aliased
from models import create_tables, Sale, Stock, Book, Shop, Publisher

load_dotenv()
user_SQL = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

DNS = f'postgresql://{user_SQL}:{password}@localhost:5432/literalist'
engine = sq.create_engine(DNS)


create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='Пушкин')
book1 = Book(title='Капитанская дочка', publisher=publisher1)
book2 = Book(title='Руслан и Людмила', publisher=publisher1)
book3 = Book(title='Евгений Онегин', publisher=publisher1)
shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
stock1 = Stock(book=book1, shop=shop1, count=1)
stock2 = Stock(book=book2, shop=shop1, count=1)
stock3 = Stock(book=book1, shop=shop2, count=1)
stock4 = Stock(book=book3, shop=shop3, count=1)
sale1 = Sale(price=600, date_sale='09-11-2022', stock=stock1, count=1)
sale2 = Sale(price=500, date_sale='08-11-2022', stock=stock2, count=1)
sale3 = Sale(price=580, date_sale='05-11-2022', stock=stock3, count=1)
sale4 = Sale(price=490, date_sale='02-11-2022', stock=stock4, count=1)
sale5 = Sale(price=600, date_sale='26-10-2022', stock=stock1, count=1)

session.add_all([publisher1, book1, book2, book3, shop1, shop2, shop3, stock1, stock2, stock3, stock4,
                 sale1, sale2, sale3, sale4, sale5])
session.commit()

def get_shops(id_or_name):
    result = (
        session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
        .select_from(Shop)
        .join(Stock, Stock.shop_id == Shop.id) # соединили Shop и Stock
        .join(Book, Book.id == Stock.book_id)  # соединили Book и Stock
        .join(Publisher, Publisher.id == Book.publisher_id)  # соединяем Publisher и Book
        .join(Sale, Sale.stock_id == Stock.id)  # Соединяем Sale и Stock
    )
    if id_or_name.isdigit():
        res = result.filter(Publisher.id == id_or_name).all()
    else:
        res = result.filter(Publisher.name == id_or_name).all()
    for book_name, shop_name, sale, data_sale in res:
        print(f"{book_name: <20} | {shop_name: <12} | {sale: <5} | {data_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    id_or_name = input('Введите имя или id автора: ')
    get_shops(id_or_name)
    session.close()