from datetime import datetime
import csv
import matplotlib.pyplot as plt

FILENAME = 'expenses.csv'

def show_menu():
    print("\n=== โปรแกรมรายรับรายจ่าย ===")
    print("1. เพิ่มรายการ")
    print("2. ดูรายการทั้งหมด")
    print("3. คำนวณยอดคงเหลือ")
    print("4. ออกจากโปรแกรม")
    print("5. ลบรายการ")
    print("6. แสดงกราฟรายรับ/รายจ่าย")



def add_expense():
    name = input("ชื่อรายการ: ")
    amount = float(input("จำนวนเงิน (+รายรับ, -รายจ่าย): "))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # <-- เพิ่มตรงนี้
    
    with open(FILENAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, amount])  # <-- เพิ่ม timestamp
    print("✅ บันทึกเรียบร้อย")


def view_expenses():
    print("\n--- รายการทั้งหมด ---")
    try:
        with open(FILENAME, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"{row[0]} | {row[1]} : {row[2]} บาท")  # <-- แสดงวันเวลา
    except FileNotFoundError:
        print("ยังไม่มีข้อมูล")


def calculate_balance():
    total = 0
    try:
        with open(FILENAME, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                total += float(row[2])  # เปลี่ยนจาก row[1] เป็น row[2]
        print(f"\n💰 ยอดคงเหลือ: {total:.2f} บาท")
    except FileNotFoundError:
        print("ยังไม่มีข้อมูล")

def delete_expense():
    try:
        with open(FILENAME, mode='r', encoding='utf-8') as file:
            reader = list(csv.reader(file))

        if not reader:
            print("ยังไม่มีข้อมูลให้ลบ")
            return

        print("\n--- รายการทั้งหมด ---")
        for idx, row in enumerate(reader):
            if len(row) >= 3:  # ตรวจว่ามีครบ 3 ช่องหรือไม่
                print(f"{idx+1}. {row[0]} | {row[1]} : {row[2]} บาท")
            else:
                print(f"{idx+1}. 🚫 แถวข้อมูลไม่สมบูรณ์: {row}")

        to_delete = int(input("เลือกรายการที่ต้องการลบ (ตัวเลข): ")) - 1

        if 0 <= to_delete < len(reader):
            deleted = reader.pop(to_delete)
            with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(reader)
            if len(deleted) >= 3:
                print(f"🗑️ ลบรายการเรียบร้อย: {deleted[1]} {deleted[2]} บาท")
            else:
                print(f"🗑️ ลบรายการที่ข้อมูลไม่สมบูรณ์: {deleted}")
        else:
            print("❌ หมายเลขไม่ถูกต้อง")

    except FileNotFoundError:
        print("ยังไม่มีข้อมูล")
    except ValueError:
        print("❌ กรุณาใส่ตัวเลขเท่านั้น")
def show_graph():
    try:
        with open(FILENAME, mode='r', encoding='utf-8') as file:
            reader = list(csv.reader(file))

        if not reader:
            print("ยังไม่มีข้อมูลสำหรับแสดงกราฟ")
            return

        labels = []
        values = []
        colors = []

        for row in reader:
            if len(row) >= 3:
                labels.append(row[1])  # ชื่อรายการ
                amount = float(row[2])
                values.append(amount)
                colors.append('green' if amount > 0 else 'red')

        plt.figure(figsize=(10, 5))
        plt.bar(labels, values, color=colors)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.title("กราฟรายรับ/รายจ่าย")
        plt.xlabel("รายการ")
        plt.ylabel("จำนวนเงิน (บาท)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("ยังไม่มีข้อมูล")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

# โปรแกรมหลัก
while True:
    show_menu()
    choice = input("เลือกเมนู (1-6): ")
    
    if choice == '1':
        add_expense()
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        calculate_balance()
    elif choice == '4':
        print("👋 ออกโปรแกรมแล้ว")
        break
    elif choice == '5':
        delete_expense()
    elif choice == '6':
        show_graph()

    else:
        print("กรุณาเลือก 1-6 เท่านั้น")
