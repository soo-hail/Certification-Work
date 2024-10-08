from cs50 import get_int


def main():
    num = get_int("Number: ")
    val = num
    count = 0
    ftd = 0  # TO STORE FIRST TWO-DIGITS

    while val != 0:
        count += 1
        val = val // 10

        if val < 100 and val > 10:
            ftd = val

    if (count == 13 or count == 16) and (ftd >= 40 and ftd <= 49):
        visa(num)
    elif (count == 15 and (ftd == 34 or ftd == 37)):
        americanCard(num)
    elif (count == 16 and (ftd > 50 and ftd < 56)):
        masterCard(num)
    else:
        print("INVALID")


def checkSum(n):
    sum1 = 0
    sum2 = 0

    val = n

    i = 1
    while val != 0:
        rem = val % 10
        val = val // 10

        if i % 2 == 0:
            currDigit = rem * 2

            if currDigit > 9:
                while currDigit != 0:
                    rem = currDigit % 10
                    currDigit = currDigit // 10
                    sum1 += rem
            else:
                sum1 += currDigit
        else:
            sum2 += rem
        i += 1

    total = sum1 + sum2

    if total % 10 == 0:
        return True
    else:
        return False


def americanCard(n):
    if checkSum(n):
        print("AMEX")
    else:
        print("INVALID")


def masterCard(n):
    if checkSum(n):
        print("MASTERCARD")
    else:
        print("INVALID")


def visa(n):
    if checkSum(n):
        print("VISA")
    else:
        print("INVALID")


main()
