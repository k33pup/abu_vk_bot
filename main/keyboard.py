from vk_api.keyboard import VkKeyboard


def create_general_keyboard():
    menu = VkKeyboard()
    menu.add_button(label="мой бандит", color="positive")
    menu.add_line()
    menu.add_button(label="мой инвентарь", color="primary")
    menu = menu.get_keyboard()
    return menu


general_keyboard = create_general_keyboard()
