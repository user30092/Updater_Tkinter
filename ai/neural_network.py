import numpy as np
import json
import time
import random
import os

class RandomActionNetwork:
    def __init__(self):
        # Веса для действий
        self.action_weights = {
            'move': [0.5, 0.1, 0.1, 0.1, 0.2],  # Пример весов для действий 'forward', 'back', 'left', 'right', 'stop'
            'look': [0.1, 0.1, 0.4, 0.4],        # Пример весов для действий 'up', 'down', 'left', 'right'
            'jump': [0.3, 0.7],                  # Пример весов для действий 'true', 'false'
            'sprint': [0.6, 0.4],                # Пример весов для действий 'true', 'false'
            'eat': [0.5, 0.5],                   # Пример весов для действий 'true', 'false'
            'container': [1/9] * 9               # Равные веса для контейнеров (всего 9 контейнеров)
        }
        self.actions = {
            'move': ['forward', 'back', 'left', 'right', 'stop'],
            'look': ['up', 'down', 'left', 'right'],
            'jump': ['true', 'false'],
            'sprint': ['true', 'false'],
            'eat': ['true', 'false'],
            'container': [str(i) for i in range(9)]  # Контейнеры от '0' до '8'
        }
        self.action_path = os.path.join(os.path.dirname(__file__), 'action.json')

    def generate_random_action(self):
        # Генерация действия с учетом весов
        action = {
            'move': np.random.choice(self.actions['move'], p=self.action_weights['move']),
            'look': np.random.choice(self.actions['look'], p=self.action_weights['look']),
            'jump': np.random.choice(self.actions['jump'], p=self.action_weights['jump']),
            'sprint': np.random.choice(self.actions['sprint'], p=self.action_weights['sprint']),
            'eat': np.random.choice(self.actions['eat'], p=self.action_weights['eat']),
            'container': np.random.choice(self.actions['container'], p=self.action_weights['container'])
        }
        return action

    def save_action(self, action):
        # Сохранение действия в файл для обмена с Mineflayer
        with open(self.action_path, 'w') as f:
            json.dump(action, f)

    def run(self):
        while True:
            # Генерация и сохранение случайного действия каждые 2 секунды
            action = self.generate_random_action()
            self.save_action(action)
            print("Сгенерировано действие:", action)
            time.sleep(random.uniform(1, 2))

if __name__ == "__main__":
    network = RandomActionNetwork()
    network.run()
