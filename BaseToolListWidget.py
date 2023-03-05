from PyQt5.QtWidgets import QListWidget


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
                Base(number=number + 1, name='"B{}"'.format(number+1)))
            self.tools_table.append(
                Tool(number=number + 1, name='"T{}"'.format(number+1)))

    def set_view(self):

        self.clear()

        for base in self.bases_table:
            base_data = base.get_base_data_in_krl_syntax()
            base_name = base.get_base_name_in_krl_syntax()
            base_typ = base.get_base_typ_in_krl_syntax()

            item = f'{base_data}  {base_name}  {base_typ}'
            self.addItem(item)

        for tool in self.tools_table:
            tool_data = tool.get_tool_data_in_krl_syntax()
            tool_name = tool.get_tool_name_in_krl_syntax()
            tool_typ = tool.get_tool_typ_in_krl_syntax()

            item = f'{tool_data}  {tool_name}  {tool_typ}'
            self.addItem(item)


class Base():
    def __init__(self, number, name, X=0.0, Y=0.0, Z=0.0, A=0.0, B=0.0, C=0.0, typ="#NONE"):
        self.number = number
        self.name = name
        self.X = X
        self.Y = Y
        self.Z = Z
        self.A = A
        self.B = B
        self. C = C
        self.typ = typ

    def get_base_data_in_krl_syntax(self):
        return f'BASE_DATA[{self.number}]={{X {self.X},Y {self.Y},Z {self.Z},A {self.A},B {self.B},C {self.C}}}'

    def get_base_name_in_krl_syntax(self):
        return f'BASE_NAME[{self.number},]={self.name}'

    def get_base_typ_in_krl_syntax(self):
        return f'BASE_TYPE[{self.number}]={self.typ}'


class Tool (Base):
    def __init__(self, number, name, X=0.0, Y=0.0, Z=0.0, A=0.0, B=0.0, C=0.0, typ="#NONE"):
        super().__init__(number, name, X, Y, Z, A, B, C, typ)

    def get_tool_data_in_krl_syntax(self):
        return f"TOOL_DATA[{self.number}]={{X {self.X},Y {self.Y},Z {self.Z},A {self.A},B {self.B},C {self.C}}}"

    def get_tool_name_in_krl_syntax(self):
        return f'TOOL_NAME[{self.number},]={self.name}'

    def get_tool_typ_in_krl_syntax(self):
        return f'TOOL_TYPE[{self.number}]={self.typ}'
