import torch
import pandas as pd

input = torch.randn(5, 3, 10)




class MyDataset():

    def __init__(self, filename):
        price_df = pd.read_csv(filename)
        self.data=filename
        x = price_df.iloc[0:7, 0].values
        y = price_df.iloc[7:, 0].values

        self.x_train = torch.tensor(x, dtype=torch.float32)
        self.y_train = torch.tensor(y, dtype=torch.float32)

        print(self.x_train,self.y_train)

    def __len__(self):
        return len(self.y_train)

    def __getitem__(self, idx):
        return self.x_train[idx], self.y_train[idx]


print(MyDataset("Uplink.csv"))