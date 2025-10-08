import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # фикстура для создания экземпляра коллектора
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_book_added_with_empty_genre(self, collector):
        collector.add_new_book('Тестовая книга')
        assert 'Тестовая книга' in collector.books_genre
        assert collector.books_genre['Тестовая книга'] == ''

    @pytest.mark.parametrize('book_name', ['', 'a' * 41])
    def test_add_new_book_invalid_name_not_added(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book('Дубликат')
        collector.add_new_book('Дубликат')
        assert len(collector.books_genre) == 1

    def test_set_book_genre_valid_book_and_genre(self, collector):
        collector.add_new_book('Фантастическая книга')
        collector.set_book_genre('Фантастическая книга', 'Фантастика')
        assert collector.books_genre['Фантастическая книга'] == 'Фантастика'

    def test_set_book_genre_invalid_genre_not_set(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.books_genre['Книга'] == ''

    def test_set_book_genre_nonexistent_book_not_set(self, collector):
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre

    def test_get_book_genre_returns_correct_genre(self, collector):
        collector.add_new_book('Книга с жанром')
        collector.books_genre['Книга с жанром'] = 'Комедии'
        assert collector.get_book_genre('Книга с жанром') == 'Комедии'

    def test_get_book_genre_nonexistent_book_returns_none(self, collector):
        assert collector.get_book_genre('Несуществующая книга') is None

    def test_get_books_with_specific_genre_returns_correct_books(self, collector):
        collector.books_genre = {'Ужас1': 'Ужасы', 'Ужас2': 'Ужасы', 'Комедия1': 'Комедии'}
        horror_books = collector.get_books_with_specific_genre('Ужасы')
        assert horror_books == ['Ужас1', 'Ужас2']

    def test_get_books_with_specific_genre_invalid_genre_returns_empty_list(self, collector):
        collector.books_genre = {'Книга': 'Фантастика'}
        result = collector.get_books_with_specific_genre('Несуществующий жанр')
        assert result == []

    def test_get_books_genre_returns_current_dict(self, collector):
        test_books = {'Книга1': 'Фантастика', 'Книга2': 'Комедии'}
        collector.books_genre = test_books
        assert collector.get_books_genre() == test_books

    def test_get_books_for_children_excludes_age_rated_books(self, collector):
        collector.books_genre = {
            'Мультик': 'Мультфильмы',
            'Ужастик': 'Ужасы', 
            'Фантастика': 'Фантастика',
            'Детектив': 'Детективы'
        }
        children_books = collector.get_books_for_children()
        assert children_books == ['Мультик', 'Фантастика']

    def test_add_book_in_favorites_valid_book(self, collector):
        collector.add_new_book('Избранная книга')
        collector.add_book_in_favorites('Избранная книга')
        assert 'Избранная книга' in collector.favorites

    def test_add_book_in_favorites_nonexistent_book_not_added(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.favorites

    def test_add_book_in_favorites_duplicate_not_added(self, collector):
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert len(collector.favorites) == 1

    def test_delete_book_from_favorites_existing_book(self, collector):
        collector.add_new_book('Книга для удаления')
        collector.favorites = ['Книга для удаления']
        collector.delete_book_from_favorites('Книга для удаления')
        assert 'Книга для удаления' not in collector.favorites

    def test_delete_book_from_favorites_nonexistent_book_no_error(self, collector):
        collector.favorites = ['Другая книга']
        collector.delete_book_from_favorites('Несуществующая книга')
        assert collector.favorites == ['Другая книга']

    def test_get_list_of_favorites_books_returns_current_list(self, collector):
        test_favorites = ['Книга1', 'Книга2', 'Книга3']
        collector.favorites = test_favorites
        assert collector.get_list_of_favorites_books() == test_favorites