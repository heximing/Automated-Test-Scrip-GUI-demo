import numpy as np
import time
import random
import matplotlib
import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import tracemalloc
matplotlib.use("svg")
tracemalloc.start()


class GreeterControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.button1 = ft.ElevatedButton(text="Start Test", on_click=self.start_clicked, disabled=False)
        self.button2 = ft.ElevatedButton(text="Stop Test", on_click=self.stop_clicked, disabled=False)
        self.test_var = {}
        for i in range(1, 11, 1):
            random.seed()
            self.test_var["Input_Var_" + str(i)] = random.randrange(0, 99, 1)
        self.chart = None  # to store MatplotlibChart instance
        self.input_field = {}  # to store TextField instances
        self.c_box = []  # to store input Checkbox instances
        self.ch_check = []  # to store checked Checkbox keys
        self.is_running = False  # bool

    def build(self):
        left_col = ft.Column()
        right_col = ft.Column()
        a_row = ft.Row(controls=[left_col, right_col], alignment=ft.MainAxisAlignment.START,
                       vertical_alignment=ft.CrossAxisAlignment.START)

        self.c_box = []
        for key, value in self.test_var.items():
            self.input_field[key] = ft.TextField(label=key, value=value)
            left_col.controls.append(self.input_field[key])
        for i in range(0, 10, 1):
            self.c_box.append(ft.Checkbox(label="Checkbox_" + str(i), value=False))
            a_cont = ft.Container(content=self.c_box[-1],
                                  bgcolor=ft.colors.YELLOW, padding=ft.padding.symmetric(horizontal=50), margin=5,
                                  width=333, height=45, border_radius=5, border=ft.border.all(2, ft.colors.BLUE))
            right_col.controls.append(a_cont)
        # print("self.c_box:", self.c_box)

        return ft.Column(controls=[a_row, self.button1], horizontal_alignment=ft.CrossAxisAlignment.START)

    def create_graph(self):
        data_row = ft.Row(
            controls=[
                ft.Text(value="(Some Live Data here 111)", bgcolor=ft.colors.RED_100, text_align=ft.TextAlign.RIGHT),
                ft.Text(value="(Some Live Data here 222)", bgcolor=ft.colors.RED_100, text_align=ft.TextAlign.RIGHT),
                ft.Text(value="(Some Live Data here 333)", bgcolor=ft.colors.RED_100, text_align=ft.TextAlign.RIGHT),
                ft.Text(value="(Some Live Data here 444)", bgcolor=ft.colors.RED_100, text_align=ft.TextAlign.RIGHT),
            ], alignment=ft.MainAxisAlignment.CENTER
        )
        try:
            plt.close(self.chart.figure)
        except AttributeError:
            pass
        fig, axs = plt.subplots(2, 1)
        axs[0].plot([0, 1, 2, 3, 4, 5], [5, 1, 4, 2, 3, 0])
        axs[0].set(xlim=(0, 5), title="Fixed Chart demo", xlabel="x-axis", ylabel="y-axis")
        axs[0].grid(True)
        # axs[0].relim()
        # axs[0].autoscale(True)


        pi_shift = 2  # 0 ~ 2
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(np.pi * t - np.pi * pi_shift)
        axs[1].plot(t, s, lw=2)
        axs[1].annotate('local max', xy=(pi_shift, 1), xytext=(2.2, 1.5),
                        arrowprops=dict(facecolor='black', shrink=0.05))
        axs[1].set(ylim=(-1, 1.8), title="Live Plot demo", xlabel="Time", ylabel="Y-value")

        fig.tight_layout()

        self.chart = MatplotlibChart(figure=fig, expand=True, isolated=True, original_size=True)

        return ft.Column(
            controls=[
                data_row,
                ft.Container(content=self.chart, margin=5, padding=5, border=ft.border.all(1, ft.colors.BLUE_500),
                             alignment=ft.alignment.center, bgcolor=ft.colors.GREEN_300, border_radius=10),
                ft.Row(controls=[self.button1, self.button2], alignment=ft.MainAxisAlignment.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def start_clicked(self, e):
        self.button1.disabled = True
        self.update()
        dummy_def("Start")
        self.save_inputs()
        self.controls.pop()  # same as self.controls = []
        self.controls.append(self.create_graph())
        self.update()
        self.is_running = True
        self.test_run()

    def stop_clicked(self, e):
        self.is_running = False
        self.button1.disabled = False
        self.controls.pop()  # same as self.controls = []
        self.controls.append(self.build())
        self.update()
        self.write_txt()

    def save_inputs(self):
        for key, textfield in self.input_field.items():
            self.test_var[key] = textfield.value
            print(key, "=", textfield.value, end="; ")
        print("")
        self.ch_check = []
        for i in range(0, len(self.c_box), 1):
            if self.c_box[i].value:
                self.ch_check.append(self.c_box[i].label)
        print("self.ch_check:", self.ch_check)

    def test_run(self):
        counter = 0
        self.chart.figure.axes[1].cla()
        line = None  # to store line
        ann = None  # to store annotate
        t = np.arange(0.0, 5.0, 0.01)
        while self.is_running:
            if line:
                pi_shift = 0.01 * counter
                line.set_ydata(np.cos(np.pi * t + np.pi * pi_shift))
                ann.xy = (2 - pi_shift, 1)
                self.chart.update()
                counter += 1
                if counter > 200:
                    counter = 0
            else:
                s = np.cos(np.pi * t)
                self.chart.figure.axes[1].set(ylim=(-1, 1.8), title="Live Plot demo", xlabel="Time", ylabel="Y-value")
                (line,) = self.chart.figure.axes[1].plot(t, s)
                ann = self.chart.figure.axes[1].annotate('Local-peak', xy=(0, 1), xytext=(2.2, 1.5),
                                                         arrowprops=dict(facecolor='black', shrink=0.05))
                self.chart.update()
            # time.sleep(0.1)
        else:
            pass

    def write_txt(self):
        f = open(time.strftime("main_memory_%Y_%m_%d.txt", time.localtime()), "a", encoding="utf-8")
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        f.write("[ Top 10 ]\n")
        for stat in top_stats[:10]:
            f.write(str(stat)+"\n")
        current, peak = tracemalloc.get_traced_memory()
        print('Current and peak memory usage: {} {}'.format(current, peak))
        f.write('Current and peak memory usage: {} {}\n'.format(current, peak))
        f.write("↑↑↑" + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "↑↑↑\n\n")
        f.close()


def main(page: ft.Page):
    page.title = "Automated Test Scrip GUI demo"
    page.scroll = "always"
    page.window_width = 777
    page.window_height = 666
    page.bgcolor = "#FFFFF8E1"
    page.add(
        ft.Row(controls=[ft.Text(value="(Title) *** (Title)", italic=False, selectable=False,
                                 style=ft.TextThemeStyle.DISPLAY_MEDIUM)], alignment=ft.MainAxisAlignment.CENTER),
        GreeterControl(),
        ft.Row(controls=[ft.Text(value="(Bottom) *** (Bottom)", italic=False, selectable=False,
                                 style=ft.TextThemeStyle.DISPLAY_SMALL)], alignment=ft.MainAxisAlignment.CENTER),
    )


def dummy_def(in_msg):
    print("This is dummy_def(), meaning \"" + in_msg + "\" button is clicked")


if __name__ == '__main__':
    ft.app(target=main)
    tracemalloc.stop()
    print("exiting...")