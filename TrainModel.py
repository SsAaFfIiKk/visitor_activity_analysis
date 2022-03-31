import sys
import torch
import time
import torch.nn.functional as F


class TrainModel:
    def __init__(self, model, train_dl, valid_dl, optimizer, certrion, scheduler, num_epochs, device):
        self.num_epochs = num_epochs
        self.model = model
        self.scheduler = scheduler
        self.train_dl = train_dl
        self.valid_dl = valid_dl
        self.optimizer = optimizer
        self.certrion = certrion
        self.device = device
        self.loss_history = []
        self.best_acc_valid = 0.0
        self.best_wieght = None
        self.training()

    def training(self):
        valid_acc = 0
        for epoch in range(self.num_epochs):
            print('Epoch %2d/%2d' % (epoch + 1, self.num_epochs))
            t0 = time.time()

            train_acc = self.train_model()
            valid_acc = self.valid_model()

            if self.scheduler:
                self.scheduler.step()
            t1 = time.time() - t0
            print('  Training complete in: %.0fm %.0fs' % (t1 // 60, t1 % 60))
            print('| val_acc | val_l1_loss | acc  | l1_loss |')
            print('| %.3f   | %.3f     | %.3f| %.3f   |' % (valid_acc[0], valid_acc[1], train_acc[0], train_acc[1]))
            print("------------------------------------------")

            if valid_acc[0] > self.best_acc_valid:
                self.best_acc_valid = valid_acc[1]
                self.best_wieght = self.model.state_dict().copy()
        return

    def train_model(self):
        self.model.train()
        N = len(self.train_dl.dataset)
        step = N // self.train_dl.batch_size
        avg_loss = 0.0
        acc = 0.0
        loss = 0.0

        for data, target in self.train_dl:
            data = data.to(self.device)
            target = target.to(self.device)
            # forward
            pred = self.model(data)
            # loss
            loss = self.certrion(pred, target)
            # backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # statistics of model training
            acc += accuracy(pred, target)
            loss += l1loss(pred, target)
            self.loss_history.append(avg_loss)
            # report statistics
            sys.stdout.flush()

        sys.stdout.flush()
        return torch.tensor([acc, loss]) / N

    def valid_model(self):
        self.model.eval()
        N = len(self.valid_dl.dataset)
        step = N // self.valid_dl.batch_size
        acc = 0.0
        loss = 0.
        with torch.no_grad():
            for data, target in self.train_dl:
                data = data.to(self.device)
                target = target.to(self.device)

                score = self.model(data)
                acc += accuracy(score, target)
                loss += l1loss(score, target)

        return torch.tensor([acc, loss]) / N


def accuracy(input, targs):
    pred = (input[:, 1]).int()
    y = targs
    return torch.sum(pred == y)


def l1loss(input, targs):
    #loss = F.cross_entropy(input[:, 1].int, targs[:, 0])
    loss = F.l1_loss(input, targs).mean()
    return loss