from functions.run_python_file import run_python_file


def run_test():
    test_1 = run_python_file("calculator", "main.py")
    print("Result for test 1")
    print(test_1)

    test_2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for test 2")
    print(test_2)

    test_3 = run_python_file("calculator", "tests.py")
    print("Result for test 3")
    print(test_3)

    test_4 = run_python_file("calculator", "../main.py")
    print("Result for test 4")
    print(test_4)

    test_5 = run_python_file("calculator", "nonexistent.py")
    print("Result for test 5")
    print(test_5)

    test_6 = run_python_file("calculator", "lorem.txt")
    print("Result for test 6")
    print(test_6)


run_test()
