from functions.get_file_content import get_file_content


def run_test():
    test_1 = get_file_content("calculator", "lorem.txt")
    print("Result for 'lorem.txt':")
    print(f"Length of string {len(test_1)}")
    print(test_1[10000:])

    test_2 = get_file_content("calculator", "main.py")
    print("Result for 'main.py':")
    print(test_2)

    test_3 = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py':")
    print(test_3)

    test_4 = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat':")
    print(test_4)

    test_5 = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'pkg/does_not_exist.py':")
    print(test_5)


run_test()
