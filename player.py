import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# DQN 신경망 클래스
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# DQN 에이전트를 Player 클래스에 통합
class Player:
    def __init__(self, board, name='', state_size=128, action_size=10):
        self.pawn = None
        self.board = board
        self.name = name
        self.score = 0
        
        # DQN 관련 초기화
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # 할인율
        self.epsilon = 1.0   # 탐험 초기 확률
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = DQN(state_size, action_size)
        self.target_model = DQN(state_size, action_size)
        self.update_target_model()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model(torch.FloatTensor(state))
        return torch.argmax(act_values[0]).item()

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model(torch.FloatTensor(state)).detach()
            if done:
                target[action] = reward
            else:
                t = self.target_model(torch.FloatTensor(next_state)).detach()
                target[action] = reward + self.gamma * torch.max(t).item()

            self.optimizer.zero_grad()
            outputs = self.model(torch.FloatTensor(state))
            loss = nn.functional.mse_loss(outputs, target)
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def set_pawn(self, pawn):
        self.pawn = pawn

    def play(self):
        state = self.board.get_state(self.pawn)  # 현재 보드 상태 가져오기, 구현 필요
        state = np.reshape(state, [1, self.state_size])
        done = False
        total_reward = 0

        while not done:
            action = self.act(state)
            next_state, reward, done, _ = self.board.step(action, self.pawn)  # 환경 상호작용, 구현 필요
            total_reward += reward
            next_state = np.reshape(next_state, [1, self.state_size])
            self.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                self.update_target_model()
                print(f"{self.name} finished the game with a score of: {total_reward}")
                break
            self.replay(32)

    def move(self, direction):
        res = self.board.move_player(direction, self.pawn)
        return res

    def wall(self, r, c, direction):
        res = self.board.put_wall(r, c, direction, self.pawn)
        return res


# class Player:
#     def __init__(self, board, name=''):
#         self.pawn = None
#         self.board = board
#         self.name = name
#         self.score = 0

#     def set_pawn(self, pawn):
#         self.pawn = pawn

#     def play(self):
#         """Win the game"""
#         return

#     def move(self, direction):
#         res = self.board.move_player(direction, self.pawn)
#         return res

#     def wall(self, r, c, direction):
#         res = self.board.put_wall(r,c,direction,self.pawn)
#         return res