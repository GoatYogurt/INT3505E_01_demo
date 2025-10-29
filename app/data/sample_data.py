from app.models import Book, User

books = [
    Book(1, "Cấu trúc dữ liệu và Giải thuật", "Nguyễn Văn A", 2021, "NXB Giáo dục", "Computer Science", "978-604-123-456-7", True),
    Book(2, "Đại số tuyến tính", "Trần Thị B", 2020, "NXB Đại học Quốc gia", "Mathematics", "978-604-234-567-8", False),
    Book(3, "Hệ điều hành", "Lê Văn C", 2019, "NXB Khoa học và Kỹ thuật", "Computer Science", "978-604-345-678-9", True),
    Book(4, "Nguyên lý Máy học", "Phạm Duy D", 2022, "NXB Thông tin và Truyền thông", "Artificial Intelligence", "978-604-456-789-0", True),
    Book(5, "Mạng máy tính", "Ngô Văn E", 2018, "NXB Lao động", "Networking", "978-604-567-890-1", False)
]


users = {
    User("admin", "admin123", "admin"),
    User("user1", "user123")
}