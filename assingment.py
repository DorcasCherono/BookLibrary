import mysql.connector as mysql


class Student:
    def __init__(self, id, reg_no, name):
        self.id = id
        self.reg_no = reg_no
        self.name = name

    def borrow_book(self, book, db):
        cursor = db.cursor()

        query = "SELECT * FROM `books`"
        cursor.execute(query)

        if cursor.rowcount < 3:
            query = "INSERT INTO `borrowed_books`(`student_id`, `book_id`) VALUES (%s, %s)"
            values = (self.id, book.id)
            cursor.execute(query, values)

            query = "UPDATE `books` SET `copies`=%s WHERE `id`=%s"
            values = (book.copies - 1, book.id)
            cursor.execute(query, values)

            db.commit()

            print("{} borrowed".format(book.title))
        else:
            print("Books borrowed should not exceed 3")

    def return_book(self, book, db):
        cursor = db.cursor()

        query = "SELECT * FROM `borrowed_books` WHERE `student_id`=%s"
        values = (self.id)
        cursor.execute(query, values)

        if cursor.rowcount > 0:
            query = "DELETE FROM `borrowed_books` WHERE `student_id`=%s AND `book_id`=%s"
            values = (self.id, book.id)
            cursor.execute(query, values)

            query = "UPDATE `books` SET `copies`=%s WHERE `id`=%s"
            values = (book.copies + 1, book.id)
            cursor.execute(query, values)

            db.commit()

            print("{} returned".format(book.title))
        else:
            print("Book return is not in the list of borrowed books")

    def list_borrowed_books(self, db):
        cursor = db.cursor()

        query = "SELECT `books`.`id`, `books`.`title`, `books`.`author`, `books`.`copies` FROM `borrowed_books` " \
                "INNER JOIN `books` ON `books`.`id`=`borrowed_books`.`id` WHERE `student_id`=1"
        values = (self.id)
        cursor.execute(query, values)
        books_tuple = cursor.fetchall()

        books = []
        for book_tuple in books_tuple:
            books.append(Book(book_tuple[0], book_tuple[1], book_tuple[2],
                              book_tuple[3]))

        index = 1
        for book in books:
            print("{}. {} by {}".format(index, book.title, book.author))


class Book:
    def __init__(self, id, title, author, copies):
        self.id = id
        self.title = title
        self.author = author
        self.copies = copies


if __name__ == "__main__":
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="library"
    )

    cursor = db.cursor()

    while True:
        action_one = input("\nWhat do you want to do?\n1. Register student.\n2. Select student.\n3. Exit\n\n> ")
        if action_one.isdigit():
            try:
                action_one = int(action_one)
                if action_one == 1:
                    reg_no = input("\nRegistration No: ")
                    name = input("Name: ")

                    query = "INSERT INTO `students`(`name`, `reg_no`) VALUES (%s, %s)"
                    values = (name, reg_no)
                    cursor.execute(query, values)
                    db.commit()
                elif action_one == 2:
                    query = "SELECT * FROM `students`"
                    cursor.execute(query)
                    students_tuple = cursor.fetchall()

                    students = []
                    for student_tuple in students_tuple:
                        students.append(Student(student_tuple[0], student_tuple[2], student_tuple[1]))

                    index = 0
                    for student in students:
                        print("{}. {}".format(index, student.name))
                        index += 1

                    action_two = input("\nEnter index: ")
                    if action_two.isdigit():
                        try:
                            action_two = int(action_two)
                            selected_student = students[action_two]
                            print("\n{} selected".format(selected_student.name))

                            action_three = input("\nWhat do you want to do?\n1. Borrow book.\n2. Return book."
                                                 "\n3. List borrowed books\n\n> ")
                            if action_three.isdigit():
                                try:
                                    action_three = int(action_three)
                                    if action_three == 1:
                                        query = "SELECT * FROM `books`"
                                        cursor.execute(query)
                                        books_tuple = cursor.fetchall()

                                        books = []
                                        for book_tuple in books_tuple:
                                            books.append(Book(book_tuple[0], book_tuple[1], book_tuple[2],
                                                              book_tuple[3]))

                                        index = 0
                                        for book in books:
                                            print("{}. {} by {} ({} {}".format(index, book.title, book.author,
                                                                               book.copies,
                                                                               "copy" if book.copies == 1 else "copies")
                                                  )

                                        action_four = input("\n Enter index: ")
                                        if action_four.isdigit():
                                            try:
                                                action_four = int(action_four)
                                                selected_book = books[action_four]
                                                selected_student.borrow_book(selected_book, db)
                                            except ValueError:
                                                print("Invalid entry")
                                            except IndexError:
                                                print("Invalid index")
                                        else:
                                            print("Invalid entry")
                                    elif action_three == 2:
                                        query = "SELECT * FROM `books`"
                                        cursor.execute(query)
                                        books_tuple = cursor.fetchall()

                                        books = []
                                        for book_tuple in books_tuple:
                                            books.append(Book(book_tuple[0], book_tuple[1], book_tuple[2],
                                                              book_tuple[3]))

                                        index = 0
                                        for book in books:
                                            print("{}. {} by {} ({} {}".format(index, book.title, book.author,
                                                                               book.copies,
                                                                               "copy" if book.copies == 1 else "copies")
                                                  )

                                        action_four = input("\n Enter index: ")
                                        if action_four.isdigit():
                                            try:
                                                action_four = int(action_four)
                                                selected_book = books[action_four]
                                                selected_student.return_book(selected_book, db)
                                            except ValueError:
                                                print("Invalid entry")
                                            except IndexError:
                                                print("Invalid index")
                                        else:
                                            print("Invalid entry")
                                    else:
                                        selected_student.list_borrowed_books(db)
                                except ValueError:
                                    print("Invalid entry")
                            else:
                                print("Invalid entry")
                        except ValueError:
                            print("Invalid entry")
                        except IndexError:
                            print("Invalid index")
                    else:
                        print("Invalid entry")
                else:
                    break
            except ValueError:
                print("Invalid entry")
        else:
            print("Invalid entry")

    db.close()
