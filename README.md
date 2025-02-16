# 2024-2_ROKEYBOOTCAMP_Collaborative_robot_project_2
두산 로보틱스의 협동로봇인 M0609를 활용하여 다양한 상황의 과제를 해결하는 프로젝트를 진행하였다.

## ✨ Key Features

**Optimization(최적화)**

- 관절 각도로 인한 특이점 위치를 분석하고, 이를 회피하기 위한 전략을 고안하면서 경로를 추정하는 알고리즘을 구현할 것이다.

**Advanced Path Planning Algorithms(고급 경로 계획 알고리즘)**

- 선형 및 곡선 경로뿐만 아니라 스플라인 곡선을 활용하여 최적의 움직임을 설계하여 부드럽고 효율적인 로봇 동작 구현할 것이다.

<br>

## 겪었던 문제사항과 해결 방법들

  - <과제 2 - 기어 사이 기어 넣기>를 진행하던 도중, 힘 제어와 회전 제어를 같이 쓸 경우, 로봇의 모터 제어가 꺼지면서 협동 로봇이 꺼지는 현상이 발생함 이를 풀기 위해 하나씩 가설을 세우며 실험함
    - 가설 1. 동기식 회전 제어와 힘 제어를 쓰면 된다. -> 하지만 동기식 회전을 힘 제어와 같이 쓸 경우, 동기식 회전에서 코드가 넘어가지 않아서 다음 코드를 읽어서 진행해야하는데 못함, 이는 두산 협동로봇에서 동기식 회전과 힘제어를 같이 사용하도록 지원해주지 않아서 발생하는 문제이다. -> 다른 가설 추론
    - 가설 2. 비동기식 회전 제어와 힘 제어를 쓰면 된다. -> 계속해서 비동기식 회전 제어를 부르기 때문에 로봇이 오버랩 되어 진행되지 않는다.
    - 가설 3. 강사님이 제공하는 코드를 보고 이에 맞게 구조를 맞춰서 해결한다. -> 동작원리는 동일하나 동작하지 않음
    - 가설 4. 단위를 쪼개서 그냥 회전 제어 말고, 힘 제어만을 이용해서 기어가 부딪치는 상황없이 실험한다. -> 그래도 로봇이 꺼지는 현상 발생
    - 가설 5. 힘 제어를 잠깐 키고 끄는 상황을 실험한다. -> 로봇이 꺼지는 현상 발생
    - 가설 6. 힘 제어가 어느부분에서 셧다운 되는 지를 print로 찍어 확인한다. -> 문제 발견 - 힘 제어를 끄는 부분에서 get_current_posx()라는 함수를 사용할 경우 죽는 상황 발생
    - 가설 7. get_current_posx()라는 현재 위치를 가져와서 일정 높이를 비교하는 구문을 삭제하고 check_position_contision()함수를 사용하여 일정 높이에 있는지 체크하여 동기식 회전 제어와 힘 제어를 사용  -> 기어 사이 기어 넣기를 성공
  - <과제 3 - 누워있는 젠가 세우기>를 진행하던 도중, parallel_axis가 x,y,z축 정렬만 하고, 축으로 부터 몇도 떨어져서 정렬 되지 않는다는 것을 몰라 헤맴,x,y,z축의 회전 경우, 티칭으로 해결하는 것이 더 빠르다.
## 🎥 Demo Video
  - [과제 1(homework1) - 무작위 블럭 배열을 인위적인 배열로 정렬 <유튜브>](https://youtu.be/ztsOVRzARyI)
  - [과제 2(homework2) - 기어 사이 기어 넣기 <유튜브>](https://youtu.be/jz2EHEQGh78)
  - [과제 3(homework3) - 누워있는 젠가 세우기 <유튜브>](https://youtu.be/uzCFj7mDgfo)
  - [과제 4(homework4) - 컵 3개 세우기 <유튜브>](https://youtu.be/pcc3xkfMvAg)
  - [과제 5(제출 과제) - 컵 10개 쌓고, 마지막에 뒤집어서 쌓기 <유튜브>](https://youtu.be/tilhtvge_kU)

### Source
 - src/dosan_pkg 내부에 제공해준 패키지를 넣어 사용한다.
https://github.com/Juwan-s/doosan-robot2

## 프로젝트 문제점과 해결할 방안
|이름|문제점|개선할 방안|역할|
|---|---|---|---|
|[이선우](https://github.com/malenwater)|더미|더미|알고리즘 코드 작성, 테스팅|
|[류승기](https://github.com/RyuSeunggi)|더미|더미|알고리즘 설계, 테스팅|
|[최민호](https://github.com/ccccmh)|더미|더미|알고리즘 설계, 테스팅|
