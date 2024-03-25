import os

from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.models import Button  # type: ignore
from bokeh.models import Div  # type: ignore
from bokeh.plotting import curdoc
from bokeh.server.server import Server

from .logger import DashboardLog
from .logger import eMessage
from .runner import runner


def run() -> None:
    log = DashboardLog()
    status, results = runner("add1", "models.models", int(div_output.text))
    if not status["pass"]:
        div_output.text = "0"
        log.log(status["errMsg"], eMessage.error)
        div_log.text = str(log)
        return
    assert len(results) == 1
    (new_number,) = results
    div_output.text = f"{new_number}"
    log.log("Function finished.", eMessage.update)
    div_log.text = str(log)


div_output = Div(text="0")
div_log = Div()
button = Button(label="Add Random Number", button_type="success")
button.on_click(run)
layout = column(row(button, div_output), row(div_log))


def bkapp(doc):
    doc.add_root(layout)


if __name__ == "__main__":
    BOKEH_SERVER = Server(
        {"/": bkapp},
        num_procs=1,
        check_unused_sessions_milliseconds=1000,
        unused_lifetime_milliseconds=1000,
        port=int(os.environ["PORT_BOKEH"]),
    )
    BOKEH_SERVER.start()
    BOKEH_SERVER.io_loop.start()
else:  # python -m bokeh serve --show --dev
    curdoc().add_root(layout)
    curdoc().title = "Planner"
