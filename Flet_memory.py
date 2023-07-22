import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import tracemalloc
matplotlib.use("svg")

class GreeterControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.button1 = ft.ElevatedButton(text="Start Test", on_click=self.start_clicked, disabled=False)
        self.button2 = ft.ElevatedButton(text="Stop Test", on_click=self.stop_clicked, disabled=False)
        self.test_var = {}
        for i in range(0, 11, 1):
            self.test_var["Some_Var_" + str(i)] = i
        self.chart = None  # to store MatplotlibChart instance
        self.input_field = {}  # to store TextField instances
        self.c_box = []  # to store input Checkbox instances
        self.ch_check = []  # to store checked Checkbox keys

    def build(self):
        left_col = ft.Column()
        right_col = ft.Column()

        self.c_box = []
        for key, value in self.test_var.items():
            self.input_field[key] = ft.TextField(label=key, value=value)
            left_col.controls.append(self.input_field[key])
            self.c_box.append(ft.Checkbox(label="Checkbox_" + str(value), value=False))
            right_col.controls.append(self.c_box[-1])

        return ft.Row(
            controls=[
                left_col,
                right_col,
                self.button1,
            ]
        )

    def create_graph(self):
        data_row = ft.Row(
            controls=[
                ft.Text(value="(Some Live Data here 111)", bgcolor=ft.colors.RED_300, text_align=ft.TextAlign.RIGHT),
                ft.Text(value="(Some Live Data here 222)", bgcolor=ft.colors.RED_300, text_align=ft.TextAlign.RIGHT),
                ft.Text(value="(Some Live Data here 333)", bgcolor=ft.colors.RED_300, text_align=ft.TextAlign.RIGHT),
                ft.Text(value="(Some Live Data here 444)", bgcolor=ft.colors.RED_300, text_align=ft.TextAlign.RIGHT),
            ]
        )
        try:
            plt.close(self.chart.figure)
        except AttributeError:
            pass
        fig, axs = plt.subplots(2, 1)
        axs[0].plot([1, 2, 3, 4], [1, 4, 2, 3])
        axs[0].set_xlim(0, 5)
        axs[0].set_xlabel("time")
        axs[0].set_ylabel("s1 and s2")
        axs[0].grid(True)

        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        axs[1].plot(t, s, lw=2)
        axs[1].annotate('local max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05))
        axs[1].set_ylabel("y-label")

        fig.tight_layout()

        self.chart = MatplotlibChart(figure=fig, expand=True, isolated=True, original_size=True)

        return ft.Column(
            controls=[
                data_row,
                ft.Container(content=self.chart, margin=5, padding=5, border=ft.border.all(1, ft.colors.BLUE_500),
                             alignment=ft.alignment.center, bgcolor=ft.colors.GREEN_300, border_radius=10),
                self.button1,
                self.button2,
            ],
            alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def start_clicked(self, e):
        self.button1.disabled = True
        self.button2.disabled = True
        self.update()
        dummy_def("Start")
        self.save_inputs()

        counter_1 = 1
        counter_2 = 1
        f = open(time.strftime("Flet_memory_%Y_%m_%d.txt", time.localtime()), "a", encoding="utf-8")
        f.write("\nRemove/re-build {} each for {} times:\n".format(counter_2, counter_1))
        f.close()
        tracemalloc.start()
        for x in range(0, counter_1, 1):  # repeat the Flet memory leak test for X times; each time save to a txt file.
            for y in range(0, counter_2, 1):  # re-build GUI for Y times.
                self.controls.pop()  # same as self.controls = []
                self.controls.append(self.create_graph())
                self.update()  # to speed up, do not update GUI
            self.update()  # to speed up, do not update GUI
            self.write_txt()
        tracemalloc.stop()
        # self.chart.update()
        self.button1.disabled = False
        self.button2.disabled = False
        self.update()

    def stop_clicked(self, e):
        self.controls.pop()  # same as self.controls = []
        self.controls.append(self.build())
        self.update()

    def save_inputs(self):
        for key,textfield in self.input_field.items():
            self.test_var[key] = textfield.value
        self.ch_check = []
        for i in range(0, len(self.c_box), 1):
            if self.c_box[i].value:
                self.ch_check.append(self.c_box[i].label)

    def write_txt(self):
        f = open(time.strftime("Flet_memory_%Y_%m_%d.txt", time.localtime()), "a", encoding="utf-8")
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
    page.title = "Flet Memory"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
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
    print("exiting...")