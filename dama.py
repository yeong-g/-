# 모듈 import
import os

# gui모듈
import tkinter
import tkinter.filedialog

# 이미지모듈
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import datetime


# 스케줄 객체를 만듬
# type : 과제, 개인일정, main : 본문, finish_state : 마감여부 확인

class sc_main:
    def __init__(self, types, main):
        self.types = types
        self.main = main
        self.number = 0
        self.finish_state = 0


class scheduler:

    # 초기값 설정
    def __init__(self):

        # 초기 window 프레임 제작
        self.window = tkinter.Tk()
        self.window.title("스케쥴러")
        self.window.geometry("440x400+100+200")

        # 창 사이즈 조절되게 설정
        self.window.resizable(True, True)
        self.window.configure(bg='gray')

        # 기본 버튼들 셋업
        button_file = tkinter.Button(self.window, text='일정입력', command=self.make_scedule, bg="black", fg="white")
        button_file.place(x=10, y=50, width=80, height=20)
        button_bg = tkinter.Button(self.window, text='다마고치', command=self.dama, bg="black", fg="white")
        button_bg.place(x=10, y=100, width=80, height=20)

        # 우선순위 정렬을 위한 초기 리스트 선언
        self.homework_list = []
        self.personalwork_list = []

        # 오늘날짜 변수
        self.date_today = str(datetime.date.today())

        self.radio_list = []
        self.radio_check = []

        # 초기에 score파일이 없으면 해당날짜 기준으로 데이터 형성 , 초기값 60
        # 일정에 대한 연산을 위하여 last_number를 선언
        if os.path.isfile("score.txt") == True:
            with open("score.txt", 'r') as data:
                self.last_number = int(data.readlines()[-1].strip().split(",")[-1])
        else:
            with open("score.txt", 'w') as data:
                data.write(str(datetime.datetime.now()) + "," + "60\n")
            self.last_number = 60

        time_string = time.strftime('%I:%M %p')
        self.message = tkinter.Label(self.window, text=time_string, font="Helvetica 10")
        self.message.place(x=180, y=10)
        self.update_time()
        self.window.mainloop()

    # 스케줄 업데이트를 위한 함수선언
    # 과제와 개인일정인지 구분
    # 입력방식은 [과제/개인일정, 해야할 일] 순서
    def make_scedule(self):
        self.text_button = tkinter.Text(self.window, height=10)
        self.text_button.place(x=100, y=50, width=170, height=20)

        self.ex_label = tkinter.Label(self.window, text='ex)과제/개인일정, 해야할 일', height=10)
        self.ex_label.configure(bg='gray')
        self.ex_label.place(x=100, y=80, width=210, height=20)

        self.ex_label2 = tkinter.Label(self.window, text='완료여부', height=10)
        self.ex_label2.configure(bg='gray')
        self.ex_label2.place(x=240, y=100, width=210, height=20)

        self.btnRead = tkinter.Button(self.window, height=1, width=10, text="입력", command=self.getTextInput, bg="black",
                                      fg="white")
        self.btnRead.place(x=280, y=50, width=30, height=20)


    # 일정입력을 받는 함수
    # 일정 입력이 완료되면 지움, 과제와 개인일정은 split을 이용하여 ,를 기준으로 구분
    def getTextInput(self):
        self.text_input = self.text_button.get(1.0, tkinter.END + "-1c")
        self.text_button.delete('1.0', tkinter.END)
        self.types = self.text_input.split(",")[0]
        self.main = self.text_input.split(",")[1]

        # 과제 인지 개인 일정인지에 따라 다르게 리스트에 저장
        new_sc = sc_main(self.types, self.main)
        if self.types == '과제':
            self.personalwork_list.append(new_sc)
        elif self.types == '개인일정':
            self.homework_list.append(new_sc)

        self.total = self.personalwork_list + self.homework_list

        # 최종 저장된 리스트를 보여주기위한 함수실행
        self.show_sc_list()

    # 다마고치를 만드는함수
    def dama(self):

        # 새로운 윈도우를 띄운다 self.newWindow 변수에 저장
        self.newWindow = tkinter.Toplevel(self.window)
        self.newWindow.title("^_^")
        self.newWindow.configure(bg='gray')
        self.newWindow.geometry("200x100+800+200")

        # 초기 이미지 회색 바탕으로 설정
        # 최종적으로 저장할 경우에 resize해서 80x80형태로 저장
        self.basig_img = Image.new('RGB', (80, 80), color='white')

        # 생성 이미지를 tkinter에서 인식할수 있도록 이미지 저장
        self.converted_image = ImageTk.PhotoImage(self.basig_img)
        (self.canvas_width, self.canvas_height) = (80, 80)

        # canvas 모듈을 이용하여 tkinter상에서 이미지를 띄울수 있게 셋업
        self.canvas = tkinter.Canvas(self.newWindow, width=self.canvas_width, height=self.canvas_height)

        # 이미지를 업로드
        self.canvas.create_image(0, 0, image=self.converted_image, anchor='nw')

        self.canvas.place(x=10, y=10)

        # 점수대에 맞게 다른 다마고치 이미지
        if self.total_number > 80:
            file_path = './dama/1.jpg'
        elif self.total_number >= 70:
            file_path = './dama/2.jpg'
        elif self.total_number >= 60:
            file_path = './dama/3.jpg'
        elif self.total_number >= 50:
            file_path = './dama/4.jpg'
        else:
            file_path = './dama/5.jpg'

        self.concept_img = Image.open(file_path)
        self.concept_img = self.concept_img.resize((80, 80))
        self.concet_convert_img = ImageTk.PhotoImage(self.concept_img)
        self.canvas.create_image(0, 0, image=self.concet_convert_img, anchor='nw')
        self.canvas.place(x=10, y=10)

        self.new_label = tkinter.Label(self.newWindow, text='score : ' + str(self.total_number), height=10)
        self.new_label.place(x=110, y=45, width=70, height=20)

    # 일자가 바뀐 후 최종스코어를 저장하는 함수
    def update_score(self):
        print([x.get() for x in self.radio_check])
        for i, value in enumerate(self.radio_check):
            if value.get() == i + 1:
                self.total_number += 5
            else:
                self.total_number -= 5

        with open("score.txt", 'a') as data:
            data.write(str(datetime.datetime.now()) + "," + str(self.total_number) + "\n")

    # 초마다 시간업데이트
    # 날짜가 바뀐순간 저장 함수를 실행한다.
    def update_time(self):
        global time_string

        time_string = time.strftime('%I:%M:%S %p')
        if str(datetime.date.today()) != self.date_today:
            self.message.config(text='update_score')
            self.update_score()
        else:
            self.message.config(text=time_string)
            self.window.after(1000, self.update_time)

    # 체크를 위한 라디오 버튼
    def show_sc_list(self):
        n = 1
        self.radio_list = []
        self.radio_check = []
        self.total_number = self.last_number

        for v in range(len(self.total)):
            self.radio_check.append(tkinter.IntVar())

        for i, value in enumerate(self.total):

            if self.total[i].types == '과제':
                text = "%d . %-8s, %s " % (n, self.total[i].types, self.total[i].main)
                self.new_label = tkinter.Label(self.window, text=text, height=10, anchor="w")
                self.new_label.place(x=100, y=120 + 20 * i, width=210, height=20)
                radio1 = tkinter.Radiobutton(self.window, value=i + 1, variable=self.radio_check[i],
                                             command=self.change_radio)
                radio1.configure(bg='gray')
                radio1.place(x=330, y=120 + 20 * i)


            elif self.total[i].types == '개인일정':
                text = "%d . %-8s, %s " % (n, self.total[i].types, self.total[i].main)
                self.new_label = tkinter.Label(self.window, text=text, height=10, anchor="w")
                self.new_label.place(x=100, y=120 + 20 * i, width=210, height=20)
                radio1 = tkinter.Radiobutton(self.window, value=i + 1, variable=self.radio_check[i],
                                             command=self.change_radio)
                radio1.configure(bg='gray')
                radio1.place(x=330, y=120 + 20 * i)
            n += 1
    #command 활성화를 위한 함수 실행
    def change_radio(self):
        pass

# 전체실행
a = scheduler()