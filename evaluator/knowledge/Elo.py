import math
import os

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm


# 计算一次battle中预计胜值得分
def expected_score(rating1, rating2):
    return 1 / (1 + 10 ** ((rating2 - rating1) / 400))


# 计算battle后的Elo分数,score1为1代表rating1赢，返回Elo变化值
def calculate_elo(rating1, rating2, score1, K):
    expected1 = expected_score(rating1, rating2)
    return K * (score1 - expected1)


# 通过平均胜率来计算预估ELO值
def compute_expected_elo(rating, prob_of_winning):
    return rating + 400 * math.log10(prob_of_winning)
    # return rating + 400 * np.log10(1 / prob_of_winning - 1)


def get_all_file_name(path):
    files = []
    # 遍历指定路径下的所有文件和文件夹
    files_and_dirs = os.listdir(path)
    for item in files_and_dirs:
        # 拼接文件的完整路径
        item_path = os.path.join(path, item)
        files.append(item_path)
    return files


def locate_idx_of_name(player_names, name):
    for i in range(len(player_names)):
        if (player_names[i] == name):
            return i

def visualization(history_df,expected_elo,window_size=20):
    # Create a colormap
    plt.style.use('dark_background')
    colors = plt.get_cmap('Set3')  # tab10

    # Apply running average filter
    history_df_smooth = history_df.rolling(window_size).mean()

    # Plotting the ELO ratings over time with bias factors and more rounds
    plt.figure(figsize=(10, 6))
    for i, player in enumerate(history_df_smooth.columns):
        # Plot smoothed data
        plt.plot(history_df_smooth[player], label=player + ' (Smoothed)', color=colors(i))
        # Plot original data with lower opacity
        plt.plot(history_df[player], alpha=0.3, color=colors(i))
        # Plot expected Elo rating
        plt.axhline(y=expected_elo[i], linestyle='--', color=colors(i))  # , label=player + ' (Expected)'

    plt.xlabel('Round')
    plt.ylabel('Elo Rating')
    plt.title(f'Simulated Elo Ratings, Smoothed')
    plt.legend()
    # plt.grid(True)
    plt.show()

def get_elo_scores(path, initial_elo, K):
    csv_files = get_all_file_name(path)
    # 读取所有 CSV 文件并合并
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file, header=None, index_col=None)
        dfs.append(df)
    # 合并数据框
    merged_df = pd.concat(dfs, ignore_index=True)
    # 获取 '1' 和 '2' 列的唯一值
    unique_values_1 = merged_df[0].unique()
    unique_values_2 = merged_df[1].unique()
    # 将唯一值列表合并，并去重
    player_names = list(set(unique_values_1) | set(unique_values_2))
    # 打印去重后的名称列表
    print(player_names)
    rating = [initial_elo for i in range(len(player_names))]  # 初始化分数
    # 记录所有分数变化情况
    history = [list(rating)]
    # 使用 zip() 函数将两个列表组合成字典
    elo_dict = dict(zip(player_names, rating[::]))
    for player in elo_dict.keys():
        elo_dict[player] = [elo_dict[player], 0, 0]  # elo score, win count, all count
    print(f"init elo dict:{elo_dict}")
    # 遍历交战记录，更新得分
    for index, row in tqdm(merged_df.iterrows(), total=merged_df.shape[0]):
        name_1 = row[0]
        name_2 = row[1]
        result = row[2]
        elo_1, win_count1, all_count1 = elo_dict[name_1]
        elo_2, win_count2, all_count2 = elo_dict[name_2]

        floating_elo = calculate_elo(rating1=elo_1, rating2=elo_2, score1=result, K=K)
        new_elo_1 = elo_1 + floating_elo
        new_elo_2 = elo_2 - floating_elo
        # 更新elo字典
        if (result == 1):
            win_count1 += 1
        if (result == 0):
            win_count2 += 1
        elo_dict[name_1] = [new_elo_1, win_count1, all_count1 + 1]
        elo_dict[name_2] = [new_elo_2, win_count2, all_count2 + 1]

        # Record ratings after this round
        i, j = locate_idx_of_name(player_names, name_1), locate_idx_of_name(player_names, name_2)
        rating[i] = new_elo_1
        rating[j] = new_elo_2
        history.append(list(rating))

    print(f"res elo dict:{elo_dict}")

    # Convert history to DataFrame for easy plotting
    history_df = pd.DataFrame(history, columns=player_names)

    expected_elo = [compute_expected_elo(initial_elo, elo_dict[name][1]/elo_dict[name][2]) for name in player_names]

    visualization(history_df, expected_elo)
    return elo_dict