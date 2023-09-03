import mysql.connector

def insert_student_and_grades():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql1234",
        database="app2"
    )

    cursor = connection.cursor()

    student_number = input("Öğrencinin numarası: ")
    name = input("Öğrencinin adı: ")
    surname = input("Öğrencinin soyadı: ")

    # Öğrenciyi ekle
    insert_student_query = "INSERT INTO student(student_number, name, surname) VALUES (%s, %s, %s)"
    student_values = (student_number, name, surname)

    try:
        cursor.execute(insert_student_query, student_values)
        connection.commit()
        print("Öğrenci başarıyla eklendi.")

        # Dersler ve notları için döngü
        for i in range(3):
            lesson = input(f"{i+1}. Ders adı: ")
            score = int(input(f"{i+1}. Ders notu: "))

            # Dersi ve notu ekle
            insert_grade_query = "INSERT INTO dersler(student_number, ders_adi, ders_notu) VALUES (%s, %s, %s)"
            grade_values = (student_number, lesson, score)

            cursor.execute(insert_grade_query, grade_values)
            connection.commit()
            print(f"{lesson} dersi başarıyla eklendi.")

    except mysql.connector.Error as err:
        print("Hata:", err)
        connection.rollback()  # Hata durumunda geri alma işlemi
    finally:
        connection.close()
        print("Veritabanı bağlantısı kapatıldı.")

def display_average_grade(student_number):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql1234",
        database="app2"
    )

    cursor = db_connection.cursor()

    query = "SELECT ders_notu FROM dersler WHERE student_number = %s"
    cursor.execute(query, (student_number,))
    dersler = cursor.fetchall()

    if dersler:
        print(f"{student_number} numaralı öğrencinin ders notları:")
        for ders in dersler:
            ders_notu = ders[0]
            print(f"Ders Notu: {ders_notu}")

        # Ders notlarının ortalamasını hesapla
        notlar = [ders[0] for ders in dersler]
        ortalama_not = sum(notlar) / len(notlar)
        print(f"Öğrencinin Ders Notları Ortalaması: {ortalama_not:.2f}")

        # Ortalama not değerine göre öğrencinin durumunu belirle
        if ortalama_not >= 50:
            durum = "Geçti"
        else:
            durum = "Kaldı"
        
        print(f"Durum: {durum}")
    else:
        print(f"{student_number} numaralı öğrencinin ders kaydı bulunmuyor.")

    db_connection.close()

def get_student_by_number(student_number):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql1234",
        database="app2"
    )

    cursor = db_connection.cursor()

    query = "SELECT * FROM student WHERE student_number = %s"
    cursor.execute(query, (student_number,))
    student = cursor.fetchone()

    if student:
        student_number, name, surname = student
        print(f"Öğrenci Numarası: {student_number}, Adı: {name}, Soyadı: {surname}")
    else:
        print(f"{student_number} numaralı öğrenci bulunamadı.")

    db_connection.close()

def list_students():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql1234",
        database="app2"
    )

    cursor = db_connection.cursor()

    query = "SELECT student_number, name, surname FROM student"
    cursor.execute(query)
    students = cursor.fetchall()

    if students:
        print("Tüm öğrenciler:")
        for student in students:
            student_number, name, surname = student
            print(f"Öğrenci Numarası: {student_number}, Adı: {name}, Soyadı: {surname}")
    else:
        print("Veritabanında kayıtlı öğrenci bulunmuyor.")

    db_connection.close()

while True:
    choice = input("Öğrenci eklemek için 'ekle', not ortalaması görmek için 'ortalama', öğrenci bilgilerini getirmek için 'getir', tüm öğrencileri listelemek için 'liste', çıkmak için 'q' girin: ")

    if choice == "ekle":
        insert_student_and_grades()
    elif choice == "ortalama":
        student_number = input("Öğrenci numarasını girin: ")
        display_average_grade(student_number)
    elif choice == "getir":
        student_number = input("Öğrenci numarasını girin: ")
        get_student_by_number(student_number)
    elif choice == "liste":
        list_students()
    elif choice == "q":
        print("Programdan çıkılıyor...")
        break
    else:
        print("Geçersiz seçenek. Lütfen 'ekle', 'ortalama', 'getir', 'liste' veya 'q' girin.")
