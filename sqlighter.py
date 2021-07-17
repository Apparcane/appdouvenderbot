import sqlite3


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT `user_id` FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(
                'SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, username, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`username`, `user_id`, `status`) VALUES(?,?,?)", (username, user_id, status))

    def update_subscription(self, username, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `name` = ? `status` = ? WHERE `user_id` = ?", (username, status, user_id))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
