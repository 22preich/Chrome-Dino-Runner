from main import Trainer, Neuron

tr = Trainer()

print(tr.evaluate(neuro=Neuron.from_weights_and_biases(
    [0.8220667268375865, -1.034498357156245, 0.11243816940092954],
    [-3.9629052523856103, 3.6996214508729874, 22.257449403087456]), render=True, limit=False, fps=5))

