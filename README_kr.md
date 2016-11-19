# Mohr_Envelope
Visualize Mohr Circle and Failure Envelope 
for Python 3.5.2

왜 만듬?
-------------
지질공학 레포트를 쓰는데, triaxial test 자료를 해석해야 하기 때문에 Mohr circle과 그 공통접선을 그려야 하는데, 엑셀로는 후자는 할 수 없었기 때문에 매트랩용 스크립트를 사용하던지, 손으로 그리던지 해야 했는데 매트랩은 없고 손으로는 그리기 싫어서, numpy와 scipy를 사용해서 그렸음. 내 후배들도 비슷한 어려움을 겪을 것 같아서 이 코드를 공개함. 컴퓨터공학과가 아니라서 코드가 지저분하겠지만 어쨌든 돌아감 ㅇㅇ



원리
-------------
Mohr Circle을 모르는 사람이 이걸 볼리는 없지만 일단 [이걸][mohr] 보면 알 수 있음.
[mohr]:https://en.wikipedia.org/wiki/Mohr's_circle
1.  σ1(major principle stress) σ3(minor principle stress)을 통해 Mohr Circle을 그리고, Mohr circle과 접선이 만나는 점 (x1-rcos(a),rsin(a))을 결정한다.
2. 이 점들을 최소자승법을 통해 직선으로 만들어낸다.
3. 이 직선과 원의 중점 사이의 거리들, 그리고 원의 반지름들 간의 차이의 평균을 구한다.
4. 각도 a를 늘려서(1~90) 반복하고, 3에서 구한 값이 가장 적은 점을 a 각도로 정한다. 이 때 직선의 y절편이 Cohesion이고, (180-(90+a))이 내부마찰각이다.
5. Mohr circle과 failure envelope를 그린다.


사용법
-------------
[numpy], [scipy], [matplotlib] 가 설치되어있어야 한다
[numpy]:http://www.numpy.org/
[scipy]:https://www.scipy.org/
[matplotlib]:http://matplotlib.org/

쉘이나 명령 프롬프트에서  python mohr.py filename.csv 으로 입력한다.

입력 포맷
-------------
csv 파일
>아무거나,σ3,σ1

엑셀 사용중이라면 column A에 아무거나 넣고 σ3은 column B, 그리고 σ1은 column C에 넣는다.

출력 포맷
-------------
in Output.txt:
 >Internal Friction Angle : 00.00° <br>
 >Cohesion : 00.00 MPa <br>
 >Failure Envelope equation : y=00.00x+00.00 

in Fig.png:<br>
![graph](Fig.png)
