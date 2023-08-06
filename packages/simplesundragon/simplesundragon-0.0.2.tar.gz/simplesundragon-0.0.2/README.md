# SimpleSunDragon
서경대학교 2023 컴퓨터공학과 여름특강 과제로 만든 간단한 라이브러리이다.
<hr/>
개발 언어: python
<hr/>
라이브러리 내부에는 4개의 코드가 있다.<br>
1. 최대공약수(gcd) 결과값만 나오는 코드
2. 최대공약수(gcd) 풀이도 나오는 코드
3. 곱셈 역원의 쌍을 구하는 코드
4. 소문자를 a부터 0로 바꾸는 코드
<hr/>
1, 2번: gcd 코드<br>
말 그대로 최대 공약수를 구하는 코드이다.

<hr/>
3번: 곱셈 역원 구하는 코드<br>
역원은 어떤 'a'에 대해서 다른 수 'b'와의 곱을 통해 1을 얻을 수 있는 수이다. 즉 '(a * b) mod m = 1'을 만족하는 수 'b'를 찾는 것이다.<br>

곱셉 역원을 구할 때 찾으려는 값(a)을 1부터 a-1까지 gcd가 1이 되는 값들들 구하면 된다.<br>

위의 말을 풀어서 코드로 적어보면 아래와 같이 된다.<br>
```
for i range(a): # a-1까지
    if (i == 0):
        continue
    else:
        gcd(gcd(a, i==1)): # gcd가 1이면
            list.append(i) # list에 넣기
```
여기서 구한 값을 통해 역원의 쌍도 쉽게 구할 수 있다.
<hr/>
4. 소문자를 숫자에 대입하여 바꾸는 함수
컴퓨터가 문자를 저장할 때에는 문자를 유니코드 형식으로 저장한다.<br>
a의 유니코드는 97이므로 'ord(a)-97'을 하게 되면 a는 0이되고, b는 1이된다.<br>
이러한 방식으로 소문자를 0부터 숫자에 대입 시켜준다.<br>
이를 통해 hill 함수를 구할 때 소문자를 숫자로 대입하기 쉽게 만들어 주었다.
<hr/>
코드르 라이브러리화 해주기 위해 PYPI 사이트를 통해 코드를 올렸다.
https://pypi.org/project/simplesundragon
<br>
<img src="./img/pypi_uplaod.jpg">
그런데 pip install은 되는데 python에서 import가 안된다.<br>
<img src="./img/pycharm_load.jpg">
<br>
<hr/>
내가 구현한 파이썬 코드는 simplesundragon 파일 내부에 있으니 파이썬 코드를 사용하려면 파일 내부의 코드만 다운받아 사용하면 될 것 같다.<br>
- 코드를 받아 사용하는 방법<br>
1. simplesundragon.py를 다운받는다
2. 필요한 파이썬 파일 내부에 넣는다.
3. import simplesundragon as dragon
4. 내부에 있는 코드를 사용한다.
ex.
1.gcd
<img src="./img/1.jpg">
2.simple_gcd
<img src="./img/2.jpg">
3.multiply_inverse
<img src="./img/3.jpg">
4.hill_num
<img src="./img/4.jpg">