import numpy as np

def test_generated_gpx(generated_track, mean_coords, std_coords):
    if generated_track is None or len(generated_track) == 0:
        print("Generated track is empty.")
        return

    # 将生成的轨迹数据逆归一化回原始的坐标值
    generated_track_unnormalized = generated_track * std_coords + mean_coords
    
    # 计算生成轨迹的均值和标准差
    mean_generated = np.mean(generated_track_unnormalized, axis=0)
    std_generated = np.std(generated_track_unnormalized, axis=0)

    print("Generated GPX track statistics:")
    print(f"Mean coordinates: {mean_generated}")
    print(f"Standard deviation of coordinates: {std_generated}")

    # 这里可以添加更多的评估方法，例如与实际轨迹的对比，或者定量评估生成轨迹的质量