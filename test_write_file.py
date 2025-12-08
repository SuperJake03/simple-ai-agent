from functions.write_file import write_file


def run_test():
    test_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Result for 'lorem.txt':")
    print(test_1)

    test_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result for 'pkg/morelorem.txt':")
    print(test_2)

    test_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result for '/tmp/temp.txt':")
    print(test_3)


run_test()
