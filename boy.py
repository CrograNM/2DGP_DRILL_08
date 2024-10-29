from pico2d import load_image, get_time

from state_machine import time_out, space_down, right_down, right_up, left_down, left_up, start_event, a_down
from state_machine import StateMachine

class Idle:
    @staticmethod
    # ^^^ : 데코레이트(장식한다, 꾸민다) : 함수의 기능을 조금 바꾼다
    # 클래스 내 함수에 self 파라미터를 안넣는다?
    # ^^^ 스태틱메소드 함수로 간주한다. -> 멤버함수x, 클래스 안에 들어있는 객체와 관계없는 그냥 함수로 간주
    # 왜 클래스 안에서 함수를 선언하는가? 이 Idle클래스는 객체를 찍어내기위한 클래스가 아니라, '그룹화'를 위한 클래스
    # 따라서, 이 클래스의 이름으로 함수들을 묶어주는것
    def enter(boy,e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif time_out(e): #AutoRun에서 타이머 이벤트를 받아 들어왔을 때
            if boy.dir == 1: #boy의 이동 방향에 따라 Idle 상태의 변수 지정
                boy.action = 3
                boy.face_dir = 1
            else :
                boy.action = 2
                boy.face_dir = -1

        boy.dir = 0 # 정지 상태를 나타낸다
        boy.frame = 0
        # 현재 시각을 저장(idle이 시작된 시점)
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy): # boy는 상태에 해당하는 객체를 의미하는 파라미터일 뿐이다. boy자체가 아님
        if boy.delayCount < 5:
            boy.delayCount += 1
        else :
            boy.delayCount = 0
            boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
    # entry, exit, do, draw -> 4가지 정보로 상태state를 표현
    # Idle이란 클래스는 그저 4개의 함수로 이루어져 있는 '상태'이다.

class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.face_dir = 1
            boy.action = 3
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if boy.delayCount < 5:
            boy.delayCount += 1
        else:
            boy.delayCount = 0
            boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                            3.141592 / 2,  # 파이/2 = 90도 회전
                                            '',  # 상하좌우 반전하지 않는다 : ''.   반전 시 : 'v', 'h'
                                            boy.x - 25, boy.y - 25, 100, 100)
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                          -3.141592 / 2,  # 파이/2 = 90도 회전
                                          '',  # 상하좌우 반전하지 않는다 : ''.   반전 시 : 'v', 'h'
                                          boy.x + 25, boy.y - 25, 100, 100)

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir = 1
            boy.action = 1
        elif left_down(e) or right_up(e):
            boy.dir = -1
            boy.action = 0
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if boy.delayCount < 5:
            boy.delayCount += 1
        else :
            boy.delayCount = 0
            boy.frame = (boy.frame + 1) % 8

        if 0 + 25 <= boy.x <= 800 - 25  :
            boy.x += boy.dir * 5

        if boy.x < 0 + 25: # 소년이 벽에 닿으면 더 이상 이동 x
            boy.x = 0 + 25
        elif boy.x > 800 - 25: # 소년이 벽에 닿으면 더 이상 이동 x
            boy.x = 800 - 25

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100, boy.action*100, 100, 100,
            boy.x,boy.y
        )

class AutoRun:
    @staticmethod
    def enter(boy, e):
        #idle상태에서 a를 누를 때, idle의 방향과 같은 방향으로 시작
        if boy.face_dir == 1:
            boy.dir = 1
            boy.action = 1
        else :
            boy.dir = -1
            boy.action = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if boy.delayCount < 5:
            boy.delayCount += 1
        else :
            boy.delayCount = 0
            boy.frame = (boy.frame + 1) % 8
        if boy.x - 50 < 0 : # 벽에 얼굴이 부딪힐 때, 반전
            boy.dir = 1
            boy.action = 1
        elif boy.x + 50 > 800 : # 벽에 얼굴이 부딪힐 때, 반전
            boy.dir = -1
            boy.action = 0
        boy.x += boy.dir * 10

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y + 25, 200, 200
        )

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1 # face_dir 변수 추가 1:오른쪽, -1:왼쪽, 초기 상태 : 오른쪽
        self.action = 3
        self.delayCount = 0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 state machine 생성, self 인자로 생성자의 파라미터들도 스테이트 머신에 넘겨준다.
        self.state_machine.start(Idle) # 초기 상태가 idle, 스테이트 머신이 최초에 idle을 처리하게된다.
        self.state_machine.set_transitions(
            {   #상태 변환 테이블 : 더블 Dict로 구현
                #Run : {}, #{}:Run 상태에서 어떤 이벤트가 들어와도 처리하지 않겠다.
                AutoRun: {time_out : Idle},
                Idle : {right_down : Run, left_down : Run, right_up : Run, left_up : Run, time_out : Sleep, a_down : AutoRun },
                Run : {right_down : Idle, left_down : Idle, right_up : Idle, left_up : Idle },
                Sleep : {right_down : Run, left_down : Run, right_up : Run, left_up : Run, space_down : Idle }
            }
        )

    def update(self):
        self.state_machine.update() # 스테이트 머신이 업데이트를 담당하게 된다.
        #self.frame = (self.frame + 1) % 8 # 이제 이건 필요가 없음

    def handle_event(self, event):
        #소년이 날리는 입력 이벤트들을 스테이트 머신이 리스트에 차곡차곡 저장할 수 있게 해야한다.
        # event : 입력 이벤트 - key, mouse 등
        # 우리가 state machine에 전달해야하는 것은 튜플 ('종류',실제값)
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
