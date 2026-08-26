import torch
import torch.nn as nn
from torch.utils.data import random_split, DataLoader
import torch.optim as optim
from dataset import SubfolderDataset
from model import Model

TRAINING_SPLIT = 0.8
TEST_SPLIT = 0.2
BATCH_SIZE = 16
LEARNING_RATE = 0.001
EPOCH = 50


def main():
    dataset = SubfolderDataset()
    model = Model()

    train_dataset, test_dataset = random_split(dataset, [TRAINING_SPLIT, TEST_SPLIT])

    train_dataloader = DataLoader(train_dataset, batch_size = BATCH_SIZE, shuffle = True)
    test_dataloader = DataLoader(test_dataset, batch_size = BATCH_SIZE, shuffle = False)

    # train_features, train_labels = next(iter(train_dataloader))

    criterion = nn.CrossEntropyLoss()
    optimiser = optim.Adam(
        model.parameters(),
        lr = LEARNING_RATE
    )

    # training loop
    for epoch in range(EPOCH):
        for features, labels in train_dataloader:
            optimiser.zero_grad()
            predictions = model(features)
            loss = criterion(predictions, labels)
            loss.backward()
            optimiser.step()

        # evaluate epoch
        total_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for features, labels in test_dataloader:
                predictions = model(features)
                predicted = torch.argmax(predictions, dim = 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
                loss = criterion(predictions, labels)
                total_loss += loss.item()
            
        print(f"Epoch {epoch + 1}, Loss: {total_loss/len(test_dataloader)}, Test Accuracy: {correct/total * 100}%")

if __name__ == "__main__":
    main()
