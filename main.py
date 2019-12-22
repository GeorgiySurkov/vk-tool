import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from ui import Ui_MainWindow
from collections import OrderedDict
from urllib.parse import urlparse

from vk_tool.users_set import UsersSet
from vk_tool.user import User

OPERATIONS_SYMBOLS = {
    'union': 'OR',
    'intersection': 'AND',
    'difference': '\\'
}

OPERATIONS_FUNCS = {
    'union': lambda a, b: a | b,
    'intersection': lambda a, b: a & b,
    'difference': lambda a, b: a - b
}

ENTER_KEY_CODE = 16777220

# APPLICATION STATES
NOTHING_SELECTED = 0
SELECTED_ASSIGN_SET = 1
SELECTED_OPERATION = 6
SELECTED_FIRST_SET = 2
SELECTED_SECOND_SET = 3
WAITING_FOR_CONFIRM = 4
WAITING_FOR_OPERATION_CHOICE = 5


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sets = OrderedDict()
        self.setup_table()
        # operations buttons clicked functions
        self.new_set_btn.clicked.connect(self.on_click_new_set_btn)
        self.new_set_from_user_friends.clicked.connect(self.on_click_new_set_from_user_friends_btn)
        self.new_set_from_community_followers.clicked.connect(self.on_click_new_set_from_community_members_btn)
        self.delete_btn.clicked.connect(self.on_click_delete_set_btn)
        self.assign_btn.clicked.connect(self.on_click_assign_btn)
        self.union_2.clicked.connect(self.on_click_union_btn)
        self.difference.clicked.connect(self.on_click_difference_btn)
        self.intersection.clicked.connect(self.on_click_intersection_btn)

        self.assign_set_btn.clicked.connect(self.on_click_assign_set_btn)
        self.first_set_btn.clicked.connect(self.on_click_first_set_btn)
        self.second_set_btn.clicked.connect(self.on_click_second_set_btn)

        self.state = None
        self.selected_assign_set = None
        self.selected_first_set = None
        self.selected_second_set = None
        self.selected_operation = None
        self.set_state(NOTHING_SELECTED)

        # for i in range(5):
        #     self.gridLayout.addWidget(QtWidgets.QPushButton(), i, 0)

    def on_click_assign_set_btn(self):
        self.sets[self.selected_assign_set][0].setEnabled(True)
        if self.selected_first_set is not None:
            self.sets[self.selected_first_set][0].setEnabled(True)
        if self.selected_second_set is not None:
            self.sets[self.selected_second_set][0].setEnabled(True)
        self.set_state(NOTHING_SELECTED)

    def on_click_first_set_btn(self):
        self.sets[self.selected_first_set][0].setEnabled(True)
        if self.selected_second_set is not None:
            self.sets[self.selected_second_set][0].setEnabled(True)
        self.set_state(SELECTED_OPERATION)

    def on_click_second_set_btn(self):
        self.sets[self.selected_second_set][0].setEnabled(True)
        self.set_state(SELECTED_FIRST_SET)

    def set_state(self, state, **kwargs):
        if state == NOTHING_SELECTED:
            self.state = state
            self.selected_assign_set = None
            self.selected_first_set = None
            self.selected_second_set = None
            self.selected_operation = None

            # disable opearations that user can't perform
            self.delete_btn.setEnabled(False)
            self.union_2.setEnabled(False)
            self.intersection.setEnabled(False)
            self.difference.setEnabled(False)
            self.assign_btn.setEnabled(False)
            self.new_set_btn.setEnabled(True)
            self.new_set_from_user_friends.setEnabled(True)
            self.new_set_from_community_followers.setEnabled(True)

            self.clear_table()
            self.hide_assign_set(False)
            self.equation_mark.setVisible(False)
            self.hide_first_set(False)
            self.now_operation_label.setVisible(False)
            self.hide_second_set(False)
            self.hint_label.setText('Выберите существующее множество или же создайте новое')
        elif state == SELECTED_ASSIGN_SET:
            self.state = state
            self.selected_assign_set = kwargs['selected_set'] or self.selected_assign_set
            self.selected_first_set = None
            self.selected_second_set = None
            self.selected_operation = None

            # disable operations that user can't perform
            self.delete_btn.setEnabled(True)
            self.union_2.setEnabled(False)
            self.intersection.setEnabled(False)
            self.difference.setEnabled(False)
            self.assign_btn.setEnabled(True)
            self.new_set_btn.setEnabled(False)
            self.new_set_from_user_friends.setEnabled(False)
            self.new_set_from_community_followers.setEnabled(False)

            self.load_table(self.selected_assign_set)
            self.assign_set_btn.setText(self.selected_assign_set)
            self.sets[self.selected_assign_set][0].setEnabled(False)
            self.hide_assign_set(True)
            self.equation_mark.setVisible(False)
            self.now_operation_label.setVisible(False)
            self.hide_first_set(False)
            self.hide_second_set(False)
            self.hint_label.setText('Выберите действие над множеством из доступных')
        elif state == WAITING_FOR_OPERATION_CHOICE:
            self.state = state
            self.selected_first_set = None
            self.selected_second_set = None
            self.selected_operation = None

            # disable operations that user can't perform
            self.delete_btn.setEnabled(False)
            self.union_2.setEnabled(True)
            self.intersection.setEnabled(True)
            self.difference.setEnabled(True)
            self.assign_btn.setEnabled(False)
            self.new_set_btn.setEnabled(False)
            self.new_set_from_user_friends.setEnabled(False)
            self.new_set_from_community_followers.setEnabled(False)

            self.load_table(self.selected_assign_set)
            self.hide_assign_set(True)
            self.equation_mark.setVisible(True)
            self.now_operation_label.setVisible(False)
            self.hide_first_set(False)
            self.hide_second_set(False)
            self.hint_label.setText('Выберите действие над множеством из доступных')
        elif state == SELECTED_OPERATION:
            self.state = state
            self.selected_first_set = None
            self.selected_second_set = None
            if 'selected_operation' in kwargs:
                self.selected_operation = kwargs['selected_operation']

            # disable operations that user can't perform
            self.delete_btn.setEnabled(False)
            self.union_2.setEnabled(False)
            self.intersection.setEnabled(False)
            self.difference.setEnabled(False)
            self.assign_btn.setEnabled(False)
            self.new_set_btn.setEnabled(False)
            self.new_set_from_user_friends.setEnabled(False)
            self.new_set_from_community_followers.setEnabled(False)

            self.load_table(self.selected_assign_set)
            self.hide_assign_set(True)
            self.equation_mark.setVisible(True)
            self.now_operation_label.setText(OPERATIONS_SYMBOLS[self.selected_operation])
            self.now_operation_label.setVisible(True)
            self.hide_first_set(False)
            self.hide_second_set(False)
            self.hint_label.setText('Выберите первое множество для действия')
        elif state == SELECTED_FIRST_SET:
            self.state = state
            if 'selected_set' in kwargs:
                self.selected_first_set = kwargs['selected_set']
            self.selected_second_set = None

            # disable operations that user can't perform
            self.delete_btn.setEnabled(False)
            self.union_2.setEnabled(False)
            self.intersection.setEnabled(False)
            self.difference.setEnabled(False)
            self.assign_btn.setEnabled(False)
            self.new_set_btn.setEnabled(False)
            self.new_set_from_user_friends.setEnabled(False)
            self.new_set_from_community_followers.setEnabled(False)

            self.load_table(self.selected_assign_set)
            self.hide_assign_set(True)
            self.equation_mark.setVisible(True)
            self.now_operation_label.setVisible(True)
            self.first_set_btn.setText(self.selected_first_set)
            self.sets[self.selected_first_set][0].setEnabled(False)
            self.hide_first_set(True)
            self.hide_second_set(False)
            self.hint_label.setText('Выберите второе множество для действия')
        elif state == SELECTED_SECOND_SET:
            self.state = state
            if 'selected_set' in kwargs:
                self.selected_second_set = kwargs['selected_set']

            # disable operations that user can't perform
            self.delete_btn.setEnabled(False)
            self.union_2.setEnabled(False)
            self.intersection.setEnabled(False)
            self.difference.setEnabled(False)
            self.assign_btn.setEnabled(False)
            self.new_set_btn.setEnabled(False)
            self.new_set_from_user_friends.setEnabled(False)
            self.new_set_from_community_followers.setEnabled(False)

            self.load_table(self.selected_assign_set)
            self.hide_assign_set(True)
            self.equation_mark.setVisible(True)
            self.now_operation_label.setVisible(True)
            self.hide_first_set(True)
            self.second_set_btn.setText(self.selected_second_set)
            self.sets[self.selected_second_set][0].setEnabled(False)
            self.hide_second_set(True)
            self.hint_label.setText('Нажмите Enter для подтверждения')

    def hide_assign_set(self, b: bool):
        self.assign_set_btn.setEnabled(b)
        self.assign_set_btn.setVisible(b)

    def hide_first_set(self, b: bool):
        self.first_set_btn.setEnabled(b)
        self.first_set_btn.setVisible(b)

    def hide_second_set(self, b: bool):
        self.second_set_btn.setEnabled(b)
        self.second_set_btn.setVisible(b)

    def set_selection_handler(self):
        clicked_btn = self.sender()
        if self.state == NOTHING_SELECTED:
            self.set_state(SELECTED_ASSIGN_SET, selected_set=clicked_btn.text())
        elif self.state == SELECTED_OPERATION:
            self.set_state(SELECTED_FIRST_SET, selected_set=clicked_btn.text())
        elif self.state == SELECTED_FIRST_SET:
            self.set_state(SELECTED_SECOND_SET, selected_set=clicked_btn.text())

    def setup_table(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(('id', 'Имя', 'Фамилия'))
        self.tableWidget.setColumnWidth(0, 90)
        self.tableWidget.setColumnWidth(1, 220)
        self.tableWidget.setColumnWidth(2, 220)
        self.clear_table()

    def load_table(self, u_set_name):
        self.set_elements_label.setText(f'Элементы множества "{u_set_name}"')
        u_set = self.sets[u_set_name][1]
        for i, user in enumerate(u_set):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(user.id)))
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(user.first_name))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(user.last_name))

    def clear_table(self):
        self.set_elements_label.setText('No set selected')
        self.tableWidget.setRowCount(0)

    def update_set_list(self):
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        for i, u_set_items in enumerate(self.sets):
            btn, u_set = self.sets[u_set_items]
            self.gridLayout.addWidget(btn, i, 0)

    def keyPressEvent(self, event):
        if event.key() == ENTER_KEY_CODE:
            if self.state == SELECTED_SECOND_SET:
                operation_func = OPERATIONS_FUNCS[self.selected_operation]
                first_set = self.sets[self.selected_first_set][1]
                second_set = self.sets[self.selected_second_set][1]
                new_set = operation_func(first_set, second_set)
                assign_set_btn, assign_set = self.sets[self.selected_assign_set]
                self.sets[self.selected_assign_set] = (assign_set_btn, new_set)

                # making all selected sets available again
                self.sets[self.selected_assign_set][0].setEnabled(True)
                self.sets[self.selected_first_set][0].setEnabled(True)
                self.sets[self.selected_second_set][0].setEnabled(True)
                self.set_state(NOTHING_SELECTED)

    def on_click_new_set_btn(self):
        name, ok_btn_pressed = QtWidgets.QInputDialog.getText(
            self,
            'Введите название',
            'Название для нового множества?'
        )
        if ok_btn_pressed and name not in self.sets:
            set_btn = QtWidgets.QPushButton()
            set_btn.setText(name)
            set_btn.clicked.connect(self.set_selection_handler)
            new_set = UsersSet(set())
            self.sets[name] = (set_btn, new_set)
            self.update_set_list()

    def on_click_new_set_from_user_friends_btn(self):
        name, ok_btn_pressed = QtWidgets.QInputDialog.getText(
            self,
            'Введите название',
            'Название для нового множества?'
        )
        if ok_btn_pressed and name not in self.sets:
            user_url, ok_btn_pressed = QtWidgets.QInputDialog.getText(
                self,
                'Ссылка',
                'Введите ссылку на пользователя'
            )
            parse_result = urlparse(user_url)
            if ok_btn_pressed and parse_result.netloc == 'vk.com' and parse_result.path.count('/') == 1:
                set_btn = QtWidgets.QPushButton()
                set_btn.setText(name)
                set_btn.clicked.connect(self.set_selection_handler)
                user = User.new_from_id(parse_result.path[1:])
                new_set = UsersSet.new_from_user_friends(user)
                self.sets[name] = (set_btn, new_set)
                self.update_set_list()

    def on_click_new_set_from_community_members_btn(self):
        name, ok_btn_pressed = QtWidgets.QInputDialog.getText(
            self,
            'Введите название',
            'Название для нового множества?'
        )
        if ok_btn_pressed and name not in self.sets:
            user_url, ok_btn_pressed = QtWidgets.QInputDialog.getText(
                self,
                'Ссылка',
                'Введите ссылку на сообщество'
            )
            parse_result = urlparse(user_url)
            if ok_btn_pressed and parse_result.netloc == 'vk.com' and parse_result.path.count('/') == 1:
                set_btn = QtWidgets.QPushButton()
                set_btn.setText(name)
                set_btn.clicked.connect(self.set_selection_handler)
                new_set = UsersSet.new_from_group_members(parse_result.path[1:])
                self.sets[name] = (set_btn, new_set)
                self.update_set_list()

    def on_click_delete_set_btn(self):
        if self.state == SELECTED_ASSIGN_SET:
            del self.sets[self.selected_assign_set]
            self.set_state(NOTHING_SELECTED)
            self.update_set_list()

    def on_click_assign_btn(self):
        self.set_state(WAITING_FOR_OPERATION_CHOICE)

    def on_click_union_btn(self):
        self.set_state(SELECTED_OPERATION, selected_operation='union')

    def on_click_intersection_btn(self):
        self.set_state(SELECTED_OPERATION, selected_operation='intersection')

    def on_click_difference_btn(self):
        self.set_state(SELECTED_OPERATION, selected_operation='difference')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
