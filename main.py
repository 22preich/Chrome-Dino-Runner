import math
import random
import numpy as np

import chromedino


class Neuron:
    def __init__(self, numinputs=1):
        self.inputs = numinputs
        self.weights = [1] * numinputs
        self.biases = [0] * numinputs

    @staticmethod
    def from_weights_and_biases(weights, biases):
        ret = Neuron(numinputs=len(weights))
        ret.weights = weights
        ret.biases = biases
        return ret

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(np.float32(-x)))

    def eval(self, data):
        if len(data) != self.inputs:
            raise RuntimeError

        returns = [0] * self.inputs

        for i in range(self.inputs):
            returns[i] = self.weights[i] * (data[i] + self.biases[i])

        return self.sigmoid(sum(returns)), sum(returns)

    def copy(self):
        return self.from_weights_and_biases(self.weights, self.biases)


class Trainer:
    def __init__(self):
        self.neuron = Neuron(numinputs=3)
        self.bestparams = None
        self.bestval = 0

    def evaluate(self, neuro=None, render=False, times=1, limit=True, fps=36, debug=False):
        neuron = neuro
        if not neuron:
            neuron = self.neuron
        rewards = []

        for _ in range(times):
            game = chromedino.Game()
            reward = 0
            last_observation = game.step(0, render=render, fps=fps, debug=debug)
            while not game.game_over:
                reward += 1
                action, raw = neuron.eval(last_observation)
                # print(action)
                last_observation = game.step(action, render=render, fps=fps, raw=raw, debug=debug)
                if limit and reward > 10000:
                    game.game_over = True
            rewards.append(reward)

        return sum(rewards) / len(rewards)

    def random_gen(self, threshold):
        return random.uniform(-threshold, threshold)

    def train(self, epochs):
        for _ in range(epochs):
            current_reward = self.evaluate(times=10)
            print(f"epoch {_}: {current_reward}")
            resulting_nns = []
            results = []
            for i in range(10):
                nn = self.neuron.copy()
                nn.weights = list(map(lambda x: x + self.random_gen(1), nn.weights))
                nn.biases = list(map(lambda x: x + self.random_gen(10), nn.biases))
                results.append(self.evaluate(neuro=nn, times=10))
                resulting_nns.append(nn)
                # print(nn.weights)

            results.append(self.evaluate(self.neuron, times=10))
            resulting_nns.append(self.neuron)

            print(results)
            max_val = max(results)
            if max_val > current_reward:
                self.neuron = resulting_nns[results.index(max_val)]

            if max_val > self.bestval:
                self.bestparams = [self.neuron.weights, self.neuron.biases]
                self.bestval = max_val

            print(self.neuron.weights)
            print(self.neuron.biases)

        print(self.bestparams, self.bestval)


if __name__ == '__main__':

    tr = Trainer()
    tr.train(100)

    tr.evaluate(neuro=Neuron.from_weights_and_biases(tr.bestparams[0], tr.bestparams[1]), render=True)
    # print(tr.bestparams)
    # print(Neuron(numinputs=3).eval([0, -1, 1]))
    """
    tr.evaluate(neuro=Neuron.from_weights_and_biases(
        [4.007663389057198, -2.210182816498185, -0.6505211865118545],
        [-7.765510222293187, 28.880266361373277, 56.547958427943115]), render=True)"""

    """
    tr.evaluate(neuro=Neuron.from_weights_and_biases(
        [4.007663389057198, -2.210182816498185, -0.6505211865118545],
        [-7.765510222293187, 28.880266361373277, 56.547958427943115]), render=True)"""
