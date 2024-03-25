from dash import callback
from dash import Dash
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash.exceptions import PreventUpdate

from .logger import DashboardLog
from .logger import eMessage
from .runner import runner

app = Dash(__name__)

input = dcc.Input(type="number", step=1)
div_output = html.Div()
div_log = html.P(
    children="Session start",
    style={
        "backgroundColor": "grey",
        "color": "white",
        "fontSize": "15px",
        "padding": "15px 15px 15px 15px",
    },
)

app.layout = html.Div(children=[input, div_output, div_log])


@callback(
    Output(div_log, "children"),
    Output(div_log, "style"),
    Output(div_output, "children"),
    Input(input, "value"),
)
def update(num: int) -> tuple[str, dict[str, str], int]:
    if num is None:
        raise PreventUpdate

    log = DashboardLog()
    status, results = runner("add1", "models.models", int(num))
    if not status["pass"]:
        log.log(status["errMsg"], eMessage.error)
        return *log.for_plotly(), 0
    assert len(results) == 1
    (new_number,) = results
    log.log("Function finished.", eMessage.update)
    return *log.for_plotly(), new_number


if __name__ == "__main__":
    app.run(debug=False)
