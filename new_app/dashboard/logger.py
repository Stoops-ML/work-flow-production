import re
from enum import auto
from enum import Enum


class eMessage(Enum):
    uninitialised = auto()  # no messages
    update = auto()
    error = auto()
    warning = auto()


class DashboardLog:
    def __init__(self) -> None:
        self._messages: list[str] = []
        self._e_types: list[eMessage] = []

    def __add__(self, log: "DashboardLog") -> "DashboardLog":
        self._messages.extend(log._messages)
        self._e_types.extend(log._e_types)
        return self

    def greatest_type(self) -> eMessage:
        if len(self._e_types) == 0:
            return eMessage.uninitialised
        return eMessage(max([e.value for e in self._e_types]))

    def log(self, message: str, e_type: eMessage = eMessage.update) -> None:
        self._messages.append(message)
        self._e_types.append(e_type)

    def __str__(self) -> str:
        if len(self._messages) == 0 or len(self._e_types) == 0:
            return ""

        divs = [
            # f"""<div style="background-color:rgb(96,96,96);color:white;font-size:25px;padding: 15px 15px 15px 15px;">Log@{datetime.now().strftime('%H:%M:%S')}> </div>"""
        ]
        for message, e_type in zip(self._messages, self._e_types):
            if len(message) > 0 and message[-1] == ".":
                message = message[:-1]
            message = re.sub(f"(.{180})", "\\1<br>", message, 0, re.DOTALL)
            match e_type:
                case eMessage.update:
                    rgb_background = "96,96,96"
                case eMessage.warning:
                    rgb_background = "255,128,0"
                case eMessage.error:
                    rgb_background = "255,0,0"
            divs.append(
                f"""<div style="background-color:rgb({rgb_background});color:white;font-size:15px;padding: 15px 15px 15px 15px;">{message}</div>"""
            )
        return "".join(divs)

    def for_plotly(self) -> tuple[str, dict[str, str]]:
        match self.greatest_type():
            case eMessage.update:
                rgb_background = "grey"
            case eMessage.warning:
                rgb_background = "orange"
            case eMessage.error:
                rgb_background = "red"
        return "".join(self._messages), {
            "backgroundColor": rgb_background,
            "color": "white",
            "fontSize": "15px",
            "padding": "15px 15px 15px 15px",
        }
