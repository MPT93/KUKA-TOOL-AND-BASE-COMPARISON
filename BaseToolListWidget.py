from PyQt5.QtWidgets import QListWidget
import re


class BaseToolListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.bases_and_tools_amount = 32
        self.create_empty_tools_bases_table()
        self.set_view()

    def create_empty_tools_bases_table(self):
        self.bases_table = []
        self.tools_table = []
        for number in range(0, self.bases_and_tools_amount):
            self.bases_table.append(
                Base(number=number + 1, name='"B{}"'.format(number + 1))
            )
            self.tools_table.append(
                Tool(number=number + 1, name='"T{}"'.format(number + 1))
            )

    def set_view(self):

        self.clear()

        for base in self.bases_table:
            base_data = base.get_base_data_in_krl_syntax()
            base_name = base.get_base_name_in_krl_syntax()
            base_typ = base.get_base_typ_in_krl_syntax()

            item = f"{base_data}  {base_name}  {base_typ}"
            self.addItem(item)

        for tool in self.tools_table:
            tool_data = tool.get_tool_data_in_krl_syntax()
            tool_name = tool.get_tool_name_in_krl_syntax()
            tool_typ = tool.get_tool_typ_in_krl_syntax()

            item = f"{tool_data}  {tool_name}  {tool_typ}"
            self.addItem(item)

    def get_coordinates(self, line):
        return [
            float(coordinate)
            for coordinate in re.findall("[\d\.\d]+|[-\d\.\d]+", line)[1:]
        ]

    def get_name_or_type_value(self, line):
        return line.split("=")[1].replace("\n", "").replace("\r", "")

    def update_data(self, line):

        pattern = "^TOOL_DATA|^BASE_DATA|^TOOL_NAME|^BASE_NAME|^TOOL_TYPE|^BASE_TYPE"
        result = re.search(pattern, line)

        if result:
            base_or_tool_number = int(re.findall("[\d\.\d]+", line)[0])
            index = base_or_tool_number - 1
            if base_or_tool_number != 0:
                if result.string.startswith("BASE_DATA"):

                    base_data = self.get_coordinates(line)

                    (
                        self.bases_table[index].X,
                        self.bases_table[index].Y,
                        self.bases_table[index].Z,
                        self.bases_table[index].A,
                        self.bases_table[index].B,
                        self.bases_table[index].C,
                    ) = base_data

                if result.string.startswith("TOOL_DATA"):

                    tool_data = self.get_coordinates(line)

                    (
                        self.tools_table[index].X,
                        self.tools_table[index].Y,
                        self.tools_table[index].Z,
                        self.tools_table[index].A,
                        self.tools_table[index].B,
                        self.tools_table[index].C,
                    ) = tool_data

                if result.string.startswith("BASE_NAME"):
                    base_name = self.get_name_or_type_value(line)
                    self.bases_table[index].name = base_name

                if result.string.startswith("TOOL_NAME"):
                    tool_name = self.get_name_or_type_value(line)
                    self.tools_table[index].name = tool_name

                if result.string.startswith("BASE_TYPE"):
                    base_typ = self.get_name_or_type_value(line)
                    if base_typ == "":
                        base_typ = "#BASE"
                    self.bases_table[index].typ = base_typ

                if result.string.startswith("TOOL_TYPE"):
                    tool_typ = self.get_name_or_type_value(line)
                    if tool_typ == "":
                        tool_typ = "#BASE"
                    self.tools_table[index].typ = tool_typ

    def check_if_not_default_frame_exists(self):

        not_default_exists = False

        for base in self.bases_table:
            if not base.check_if_default():
                not_default_exists = True
                break

        for tool in self.tools_table:
            if not tool.check_if_default():
                not_default_exists = True
                break

        return not_default_exists


class Base:
    def __init__(
        self, number, name, X=0.0, Y=0.0, Z=0.0, A=0.0, B=0.0, C=0.0, typ="#NONE"
    ):
        self.number = number
        self.name = name
        self.X = X
        self.Y = Y
        self.Z = Z
        self.A = A
        self.B = B
        self.C = C
        self.typ = typ

    def get_base_data_in_krl_syntax(self):
        return f"BASE_DATA[{self.number}]={{X {self.X},Y {self.Y},Z {self.Z},A {self.A},B {self.B},C {self.C}}}"

    def get_base_name_in_krl_syntax(self):
        return f"BASE_NAME[{self.number},]={self.name}"

    def get_base_typ_in_krl_syntax(self):
        return f"BASE_TYPE[{self.number}]={self.typ}"

    def check_if_default(self):
        if (
            self.X != 0.0
            or self.Y != 0.0
            or self.Z != 0.0
            or self.A != 0.0
            or self.B != 0.0
            or self.C != 0.0
        ):
            return False
        else:
            return True

    @staticmethod
    def compare_coordinates(robot_frame, olp_frame):

        delta_X = robot_frame.X - olp_frame.X
        delta_Y = robot_frame.Y - olp_frame.Y
        delta_Z = robot_frame.Z - olp_frame.Z
        delta_A = robot_frame.A - olp_frame.A
        delta_B = robot_frame.B - olp_frame.B
        delta_C = robot_frame.C - olp_frame.C

        if (
            robot_frame.X == olp_frame.X
            and robot_frame.Y
            and olp_frame.Y
            and robot_frame.Z == olp_frame.Z
            and robot_frame.A == olp_frame.A
            and robot_frame.B == olp_frame.B
            and robot_frame.C == olp_frame.C
        ):
            frames_equal = True

        else:
            frames_equal = False

        return frames_equal, (delta_X, delta_Y, delta_Z, delta_A, delta_B, delta_C)


class Tool(Base):
    def __init__(
        self, number, name, X=0.0, Y=0.0, Z=0.0, A=0.0, B=0.0, C=0.0, typ="#NONE"
    ):
        super().__init__(number, name, X, Y, Z, A, B, C, typ)

    def get_tool_data_in_krl_syntax(self):
        return f"TOOL_DATA[{self.number}]={{X {self.X},Y {self.Y},Z {self.Z},A {self.A},B {self.B},C {self.C}}}"

    def get_tool_name_in_krl_syntax(self):
        return f"TOOL_NAME[{self.number},]={self.name}"

    def get_tool_typ_in_krl_syntax(self):
        return f"TOOL_TYPE[{self.number}]={self.typ}"
