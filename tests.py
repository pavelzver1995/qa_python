import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_book_added_with_empty_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        assert 'Тестовая книга' in collector.books_genre
        assert collector.books_genre['Тестовая книга'] == ''

    @pytest.mark.parametrize('book_name', ['', 'a' * 41])
    def test_add_new_book_invalid_name_not_added(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Дубликат')
        collector.add_new_book('Дубликат')
        assert len(collector.books_genre) == 1

    def test_set_book_genre_valid_book_and_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Фантастическая книга')
        collector.set_book_genre('Фантастическая книга', 'Фантастика')
        assert collector.get_book_genre('Фантастическая книга') == 'Фантастика'

    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Книга') == ''

    def test_get_books_with_specific_genre_returns_correct_books(self):
        collector = BooksCollector()
        collector.add_new_book('Ужас1')
        collector.add_new_book('Ужас2')
        collector.add_new_book('Комедия1')
        
        collector.set_book_genre('Ужас1', 'Ужасы')
        collector.set_book_genre('Ужас2', 'Ужасы')
        collector.set_book_genre('Комедия1', 'Комедии')
        
        horror_books = collector.get_books_with_specific_genre('Ужасы')
        assert len(horror_books) == 2
        assert 'Ужас1' in horror_books
        assert 'Ужас2' in horror_books

    def test_get_books_for_children_excludes_age_rated_books(self):
        collector = BooksCollector()
        collector.add_new_book('Мультик')
        collector.add_new_book('Ужастик')
        collector.add_new_book('Фантастика')
        
        collector.set_book_genre('Мультик', 'Мультфильмы')
        collector.set_book_genre('Ужастик', 'Ужасы')
        collector.set_book_genre('Фантастика', 'Фантастика')
        
        children_books = collector.get_books_for_children()
        assert 'Мультик' in children_books
        assert 'Фантастика' in children_books
        assert 'Ужастик' not in children_books

    def test_add_and_remove_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Избранная книга')
        
        collector.add_book_in_favorites('Избранная книга')
        assert 'Избранная книга' in collector.get_list_of_favorites_books()
        
        collector.delete_book_from_favorites('Избранная книга')
        assert 'Избранная книга' not in collector.get_list_of_favorites_books()

    def test_add_to_favorites_nonexistent_book_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_add_duplicate_to_favorites_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert len(collector.get_list_of_favorites_books()) == 1