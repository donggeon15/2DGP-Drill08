from pico2d import load_image

from pico2d import *
from state_machine import *


class Idle:
    @staticmethod
    def enter(boy, e):
        if right_up(e) or right_down(e) or start_event(e) or boy.face_dir == 1:
            boy.action = 3
            boy.face_dir = 1
        elif left_up(e) or left_down(e) or boy.face_dir == -1:
            boy.action = 2
            boy.face_dir = -1
        boy.frame = 0
        boy.wait_time = get_time() #시작 시간을 기록
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.wait_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                        3.141592 / 2, # 회전 각도
                        '', # 좌우 상하 반전 X
                        boy.x - 25, boy.y - 25, 100, 100)
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                        -3.141592 / 2,  # 회전 각도
                        '',  # 좌우 상하 반전 X
                        boy.x + 25, boy.y - 25, 100, 100)

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
            boy.face_dir = 1
        elif left_down(e) or right_up(e):
            boy.action = 0
            boy.dir = -1
            boy.face_dir = -1
        boy.frame = 0
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class AutoRun:
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == 1:
            boy.action = 1
            boy.dir = 1
            boy.face_dir = 1
        else:
            boy.action = 0
            boy.dir = -1
            boy.face_dir = -1
        boy.frame = 0
        boy.auto_run_time = get_time()
        boy.size = 100
        boy.speed = 1
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed
        boy.speed += 0.2
        boy.size += 1
        if boy.x > 800:
            boy.action = 0
            boy.dir = -1
            boy.face_dir = -1
        elif boy.x < 0:
            boy.action = 1
            boy.dir = 1
            boy.face_dir = 1
        if get_time() - boy.auto_run_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y + ((boy.size - 100)/3), boy.size, boy.size)
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체를 위한 #어떤 객체를 위한 상태머신이지 알려줄 필요가 있다
        self.state_machine.start(Idle) #객체를 생성한것이 아니고 직접 Idle라는 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle: {time_out: Sleep, left_down: Run, left_up: Run, right_down: Run, right_up: Run, a_down: AutoRun},
                Sleep: {space_down: Idle, left_down: Run, left_up: Run, right_down: Run, right_up: Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : input event
        # state machine event : (이벤트 종류, 값)
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()