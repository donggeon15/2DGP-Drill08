
from pico2d import *


# event ( 종료 문자열, 실제 값)
def start_event(e):
    return e[0] == 'START'

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

# 상태 머신을 처리 해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o # boy self가 전달 self.o 는 상태 머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는

    def update(self):
        self.cur_state.do(self.o) #Idle do 호출
        if self.event_que: # 이벤트 큐값에 뭔가 있으면 true로 처리
            e = self.event_que.pop(0) # 리스트에 첫번째 요소를 꺼낸다.
            for event_check, next_state in self.transitions[self.cur_state].items():
                if event_check(e):  # e가 지금 check_event이면 space_down
                    self.cur_state.exit(self.o, e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'ENTER into {self.cur_state}')
                    return

    def start(self, state):
        # 현재 상태를 시작 상태로 만듦
        self.cur_state = state
        # 시작 상태에서 엔터 액션 해줘야함
        self.cur_state.enter(self.o, ('START', 0))
        print(f'ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, e):
        self.event_que.append(e) # 상태 머신용 이벤트 추가
        print(f'   DEBUG: new event {e} is added to event Que')
