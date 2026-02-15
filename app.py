'''
print("Hello, World!")
print("*" * 10)
print(2 + 1)

x = 10
y = 1
unit_price = 8
total_price = unit_price * x
print("Total price:", total_price)
if total_price > 50:
    print("You get a discount!")
else:
    print("No discount for you.")

student_counts = 100
rating = 4.99
is_published = False
course_name = "Python for Beginners"
print("Number of students:", student_counts)

message = """
Hi Friends, hope you are doing well. I am learning Python and it's really fun! I can't wait to build some amazing projects with it. Let's keep learning together!
"""
print(len(message))
print(course_name[0:7]+course_name[7:11])

print("Python" in course_name )
print("Java" in course_name )

print("Python \"Programming\"")
print("Python\nProgramming")
print("Python\tProgramming")
course = "Python Programming"
print(course.count("g"))
print(course.find("P"))
print(course.replace("Python", "Java"))
print(course)

first = "Shrikant"
last = "Lambe"
full_name = f"{first.upper()} {last.upper()}"   
print(full_name)
'''
import math
print(1 + 2 * 3 - 4 / 2)
print(10 % 3)
print(10 // 3)
print(2 ** 3)
x = 1
x += 3
print(x)
math.sqrt(16)   