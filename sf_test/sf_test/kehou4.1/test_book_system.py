import pytest
from book_system import library, Library


class TestLibrary:
    def setup_method(self):
        """每个测试方法前重置图书馆状态"""
        self.library = Library()

    def test_borrow_book_success(self):
        # ** *测试正常借书功能 ** *
        # 测试正常借书
        result = self.library.borrow_book(1, 101)
        assert result == True

        # 验证库存减少
        stock = self.library.get_book_stock(101)
        assert stock == 2

        # 验证用户借阅记录
        borrowed_books = self.library.get_user_borrowed_books(1)
        assert 101 in borrowed_books

    def test_borrow_book_user_not_exist(self):
        # ** *测试用户不存在的情况 ** *
        # 测试不存在的用户
        with pytest.raises(ValueError, match="用户不存在"):
            self.library.borrow_book(999, 101)

    def test_borrow_book_not_exist(self):
        # ** *测试图书不存在的情况 ** *
        # 测试不存在的图书
        with pytest.raises(ValueError, match="图书不存在"):
            self.library.borrow_book(1, 999)

    def test_borrow_book_out_of_stock(self):
        # ** *测试库存不足的情况 ** *
        # 测试库存为0的图书
        with pytest.raises(ValueError, match="图书库存不足"):
            self.library.borrow_book(1, 103)

    def test_borrow_book_multiple_times(self):
        # ** *测试多次借阅同一本书 ** *
        # 第一次借阅成功
        result1 = self.library.borrow_book(1, 102)
        assert result1 == True
        assert self.library.get_book_stock(102) == 1

        # 第二次借阅成功
        result2 = self.library.borrow_book(2, 102)
        assert result2 == True
        assert self.library.get_book_stock(102) == 0

        # 第三次借阅失败（库存不足）
        with pytest.raises(ValueError, match="图书库存不足"):
            self.library.borrow_book(3, 102)

    def test_borrow_book_different_users(self):
        # ** *测试不同用户借阅不同书籍 ** *
        # 用户1借书101
        result1 = self.library.borrow_book(1, 101)
        assert result1 == True
        assert 101 in self.library.get_user_borrowed_books(1)

        # 用户2借书104
        result2 = self.library.borrow_book(2, 104)
        assert result2 == True
        assert 104 in self.library.get_user_borrowed_books(2)

        # 验证各自的借阅记录不互相影响
        assert 104 not in self.library.get_user_borrowed_books(1)
        assert 101 not in self.library.get_user_borrowed_books(2)

    def test_get_user_borrowed_books_invalid_user(self):
        # ** *测试获取不存在的用户的借阅记录 ** *
        with pytest.raises(ValueError, match="用户不存在"):
            self.library.get_user_borrowed_books(999)

    def test_get_book_stock_invalid_book(self):
        # ** *测试获取不存在的图书库存 ** *
        with pytest.raises(ValueError, match="图书不存在"):
            self.library.get_book_stock(999)


def test_global_library():
    # ** *测试全局图书馆实例 ** *
    # 使用全局实例测试
    result = library.borrow_book(1, 101)
    assert result == True

    # 验证库存减少
    stock = library.get_book_stock(101)
    assert stock == 2  # 初始库存是3，借出一本后应该是2


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])