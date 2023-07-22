import flet as ft

def main(page):

    def slider_changed(e):
        t.value = "Slider changed to {} Hz".format(e.control.value)
        page.update()

    t = ft.Text()
    page.add(
        ft.Text("Slider with 'on_change' event:"),
        ft.Slider(min=0.1, max=20, divisions=50, label="{value}Hz", on_change=slider_changed), t)

ft.app(target=main)