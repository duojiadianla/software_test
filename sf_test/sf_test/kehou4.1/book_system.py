class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []


class Book:
    def __init__(self, book_id, title, author, stock):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.stock = stock


class Library:
    def __init__(self):
        self.users = {}
        self.books = {}
        self._initialize_data()

    def _initialize_data(self):
        # 初始化用户数据
        self.users[1] = User(1, "张三")
        self.users[2] = User(2, "李四")
        self.users[3] = User(3, "王五")

        # 初始化图书数据
        self.books[101] = Book(101, "Python编程", "John Doe", 3)
        self.books[102] = Book(102, "数据结构", "Jane Smith", 2)
        self.books[103] = Book(103, "算法导论", "Bob Johnson", 0)  # 库存为0
        self.books[104] = Book(104, "机器学习", "Alice Brown", 1)

    def borrow_book(self, user_id, book_id):
        """
        借书功能

        Args:
            user_id: 用户ID
            book_id: 图书ID

        Returns:
            bool: 借书成功返回True

        Raises:
            ValueError: 当用户不存在、图书不存在或库存不足时
        """
        # 检查用户是否存在
        if user_id not in self.users:
            raise ValueError("用户不存在")

        # 检查图书是否存在
        if book_id not in self.books:
            raise ValueError("图书不存在")

        book = self.books[book_id]
        user = self.users[user_id]

        # 检查库存是否充足
        if book.stock <= 0:
            raise ValueError("图书库存不足")

        # 执行借书操作
        book.stock -= 1
        user.borrowed_books.append(book_id)

        return True

    def get_user_borrowed_books(self, user_id):
        """获取用户借阅的图书列表"""
        if user_id not in self.users:
            raise ValueError("用户不存在")

        return self.users[user_id].borrowed_books

    def get_book_stock(self, book_id):
        """获取图书库存"""
        if book_id not in self.books:
            raise ValueError("图书不存在")

        return self.books[book_id].stock


# 创建全局图书馆实例
library = Library()