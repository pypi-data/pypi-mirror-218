# gcd 구하는 코드
def gcd(a, b):
    if a % b == 0:
        print("q: " + str(int(a/b)) +" r1: " + str(a) + " r2: " + str(b) + " r: " + str(a % b))
        print("q:  " + " r1: " + str(b) + " r2: " + str(a % b) + " r: ")
        print("결과 값 :" + str(b))
        return b
    elif b == 0:
        print("q: " + str(int(a/b)) +" r1: " + str(a) + " r2: " + str(b) + " r: " + str(a % b))
        print("q:  " + " r1: " + str(b) + " r2: " + str(a % b) + " r: ")
        print("결과 값 :" + str(a))
        return a
    else:
        print("q: " + str(int(a/b)) +" r1: " + str(a) + " r2: " + str(b) + " r: " + str(a % b))
        return gcd(b, a % b)

#############################################################################################
# 곱셈 역원 구하는 코드
def multiply_inverse(a):
    list = []
    for i in range(a):
        if (i == 0):
            continue
        else:
            print(i, "일 때: ")
            if (simple_gcd(a, i) == 1):
                list.append(i)
    return list

#############################################################################################
#3 과제 hill함수 구할때 소문자를 유니코드 숫자로 바꾸는 함수
def hill_num(a):
    list = []
    for i in a:
        list.append(ord(i) - 97)
    return list
#############################################################################################
#4 결과값만 보여주는 gcd
def simple_gcd(a, b):
    if a % b == 0:
        print("결과 값 :" + str(b))
        return b
    elif b == 0:
        print("결과 값 :" + str(a))
        return a
    else:
        return simple_gcd(b, a % b)