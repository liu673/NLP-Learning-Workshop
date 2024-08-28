# -*- coding: utf-8 -*-
import torch
from torch import nn  # nn contains all of PyTorch's building blocks for neural networks
import matplotlib.pyplot as plt
from pathlib import Path

# Check PyTorch version
# print(torch.__version__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("数据加载和处理".center(100, "-"))
# Create *known* parameters
weight = 0.7
bias = 0.3
print(f"Parameters:\n\tweight: {weight}\n\tbias: {bias}")

# Create data
start = 0
end = 1
step = 0.02
X = torch.arange(start, end, step).unsqueeze(dim=1)
y = weight * X + bias

# X[:10], y[:10]
print(f"X的shape为：{X.shape}, y的shape为：{y.shape}")
print(f"X的维度为：{X.ndim}, y的维度为：{y.ndim}")
train_split = int(0.8 * len(X))

# Split the data into training & test sets
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]
print(f"X_train的shape为：{X_train.shape} y_train的shape为：{y_train.shape}")


# print(f"X_test的shape为：{X_test.shape} y_test的shape为：{y_test.shape}")


def plot_predictions(train_data=X_train,
                     train_labels=y_train,
                     test_data=X_test,
                     test_labels=y_test,
                     predictions=None):
    plt.figure(figsize=(10, 7))
    plt.scatter(train_data, train_labels, c="b", s=4, label="Training data")
    plt.scatter(test_data, test_labels, c="g", s=4, label="Testing data")
    if predictions is not None:
        plt.scatter(test_data, predictions, c="r", s=4, label="Predictions")

    plt.xlabel("x-values")
    plt.ylabel("y-values")
    plt.legend(loc="upper left")
    plt.show()


class LinearRegressionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.weights = nn.Parameter(torch.randn(1,
                                                requires_grad=True,
                                                dtype=torch.float))
        self.bias = nn.Parameter(torch.randn(1,
                                             requires_grad=True,
                                             dtype=torch.float))
        # self.linear = nn.Linear(1, 1)  # 1 input, 1 output

    # def forward(self, x: torch.Tensor) -> torch.Tensor:
    #     out = self.linear(x)
    #     return out
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.weights * x + self.bias


print("模型构建".center(100, "-"))

torch.manual_seed(42)
model = LinearRegressionModel()
print("模型参数: \t", list(model.parameters()), end="\n\n")
print("模型转态: \t", model.state_dict())
print("模型参数所在设备: \t", next(model.parameters()).device)
# print("Model's named_parameters: \n", model.named_parameters())
print("要确保模型的参数在同一个设备上".center(30, "-"))
model.to(device)
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)
print("模型参数所在设备: \t", next(model.parameters()).device)
print(f"模型状态：{model.state_dict()} ")
print(f"数据集所在设备：{X_train.device}")

criterion = nn.MSELoss()  # loss function (Mean Squared Error)
learning_rate = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

epoch_count_list = []
train_loss_list = []
test_loss_list = []


def train_model(model, criterion, optimizer, model_path=None, epochs=2000):
    for epoch in range(epochs):
        model.train()
        y_pred = model(X_train)
        loss = criterion(y_pred, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.inference_mode():
            y_test_pred = model(X_test)
            test_loss = criterion(y_test_pred, y_test)
        if (epoch + 1) % 100 == 0:
            epoch_count_list.append(epoch + 1)
            train_loss_list.append(loss.item())
            test_loss_list.append(test_loss.item())
            print(f'Epoch: {epoch + 1}, Loss: {loss.item():.4f}, Test Loss: {test_loss.item():.4f}')

    print(f"模型训练最终参数: {model.state_dict()}")
    torch.save(model.state_dict(), model_path)


MODEL_PATH = Path("models")
MODEL_PATH.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "01_pytorch_workflow_model.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME

print("训练模型并保存".center(100, "-"))
train_model(model, criterion, optimizer, MODEL_SAVE_PATH)


plt.plot(epoch_count_list, train_loss_list, label='Training Loss')
plt.plot(epoch_count_list, test_loss_list, label='Test Loss')
plt.legend()
plt.show()

print("加载模型".center(100, "-"))
load_model = LinearRegressionModel()
load_model.load_state_dict(torch.load(MODEL_SAVE_PATH))
print("模型加载的参数: \t", load_model.state_dict())

print("模型预测".center(100, "-"))
load_model.eval()
with torch.inference_mode():
    predictions = load_model(X_test).cpu().numpy()
    plot_predictions(X_train, y_train, X_test, y_test, predictions)
