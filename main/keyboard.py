from vk_api.keyboard import VkKeyboard


class KeyBoards:

    def create_general_keyboard(self):
        menu = VkKeyboard()
        menu.add_button(label="мой бандит", color="positive")
        menu.add_line()
        menu.add_button(label="мой инвентарь", color="primary")
        menu = menu.get_keyboard()
        return menu

    def create_work_keyboard(self):
        menu = VkKeyboard()
        menu.add_button(label="Работа Рэкет по городу", color="positive")
        menu.add_line()
        menu.add_button(label="Работа Смена на заводе", color="positive")
        menu.add_line()
        menu.add_button(label="Работа Грабеж", color="positive")
        menu = menu.get_keyboard()
        return menu


keyboard = KeyBoards()
general_keyboard = keyboard.create_general_keyboard()
work_keyboard = keyboard.create_work_keyboard()