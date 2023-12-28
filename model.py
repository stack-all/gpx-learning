# model.py
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import ModelCheckpoint

# 设计 LSTM 模型
def build_model(input_shape, units=64, dropout=0.3):
    model = Sequential()
    model.add(LSTM(units, input_shape=input_shape, return_sequences=True))
    model.add(LSTM(units, return_sequences=False))
    model.add(Dense(units, activation='relu'))
    model.add(Dense(2))  # 预测纬度和经度
    model.compile(optimizer='adam', loss='mse')
    return model

# 训练模型并保存
# epochs 代表训练模型时整个数据集将被遍历迭代的次数。每一次遍历完整个数据集并进行一次前向传播和后向传播的过程被称为一个epoch。
def train_model(model, sequences, next_points, epochs=100, batch_size=64, model_path='model.h5'):
    checkpoint = ModelCheckpoint(model_path, save_best_only=True, monitor='val_loss', mode='min')
    model.fit(sequences, next_points, batch_size=batch_size, epochs=epochs, callbacks=[checkpoint], validation_split=0.2)
    model.save(model_path)
    return model

# 使用模型生成轨迹，num_points 代表生成的轨迹的点的数量
def generate_gpx(model, seed, num_points=100):
    generated_points = []
    current_seq = seed
    for _ in range(num_points):
        predicted_point = model.predict(current_seq)
        generated_points.append(predicted_point[0])
        current_seq = np.concatenate((current_seq[0][1:], predicted_point.reshape(1, -1)), axis=0).reshape(1, current_seq.shape[1], current_seq.shape[2])
    return np.array(generated_points)