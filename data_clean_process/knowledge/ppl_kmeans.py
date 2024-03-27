## Used to get the ppl and emb for the whole input
def get_perplexity_and_embedding_whole_text(tokenizer, model, text, max_length):

    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=max_length).to(device)
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids.contiguous())
    loss = outputs.loss
    perplexity = torch.exp(loss)
    hidden_states = outputs.hidden_states
    embeddings = hidden_states[-1]
    sentence_embedding = embeddings.mean(dim=1)
    return perplexity.to('cpu'), sentence_embedding.to('cpu')

def do_clustering(args, high_dim_vectors):
    clustering_algorithm = args.cluster_method
    if clustering_algorithm == 'kmeans':
        clustering = KMeans(n_clusters=args.kmeans_num_clusters, random_state=0).fit(high_dim_vectors)
    return clustering

def sample_middle_confidence_data(cluster_labels, confidences, n, low_th=25, up_th=75):
    num_clusters = len(np.unique(cluster_labels))
    # Get the indices for each cluster
    cluster_indices = {i: np.where(cluster_labels == i)[0] for i in range(num_clusters)}
    # Create a dictionary to store the indices of the middle level confidence samples
    middle_confidence_samples = {}
    for i in range(num_clusters):
        # 对类中心的数据点排序
        sorted_indices = cluster_indices[i]
        # 如果某个类数据不够，全采
        if len(sorted_indices) < n:
            middle_confidence_samples[i] = sorted_indices
            continue
        # 获取这个类别的的置信度，置信度来自于样本的ppl值
        cluster_confidences = confidences[sorted_indices]
        ## 获取最低的ppl阈值和最大的阈值
        lower_threshold = np.percentile(cluster_confidences, low_th)
        upper_threshold = np.percentile(cluster_confidences, up_th)
        ## 将最低阈值和最大阈值之间的数据作为中间数据上
        middle_indices = sorted_indices[(cluster_confidences >= lower_threshold) & (cluster_confidences <= upper_threshold)]
        ## 如果中间阈值过滤数据量不够采样数量，则全部使用
        if len(middle_indices) < n:
            middle_confidence_samples[i] = middle_indices
        else:
            ## 否则切分成n份进行采样
            step_size = len(middle_indices) // n
            # Select evenly from the middle level confidence samples
            middle_confidence_samples[i] = middle_indices[::step_size][:n]
    return middle_confidence_samples

def main():
    args = parse_args()
    pt_data = torch.load(args.pt_data_path, map_location=torch.device('cpu'))
    with open(args.json_data_path, "r") as f:
        json_data = json.load(f)
    emb_list = []
    ppl_list = []
    ## 获取每个数据的embedding，用于kmeans聚类别；
    ## 获取每个数据的ppl值，也就是loss
    for i in tqdm(range(len(pt_data))):
        data_i = pt_data[i]
        sent_emb_list = data_i['sent_emb']
        emb_list.append(sent_emb_list[args.sent_type])
        ppl_list.append(data_i['ppl'][args.ppl_type].item())

    high_dim_vectors = torch.cat(emb_list,0).numpy()
    ppl_array = np.array(ppl_list)

    ## 使用kmeans进行聚类
    clustering = do_clustering(args, high_dim_vectors)
    cluster_labels = clustering.labels_

    ## 获取中间置信度的数据
    def get_json_sample(middle_confidence_samples):
        json_samples = []
        for k in middle_confidence_samples.keys():
            ids_list = middle_confidence_samples[k].tolist()
            for id_i in ids_list:
                ori_sample = json_data[id_i]
                json_samples.append(ori_sample)
        return json_samples

    middle_confidence_samples = sample_middle_confidence_data(cluster_labels, ppl_array, args.sample_num, args.low_th, args.up_th)
    new_data = get_json_sample(middle_confidence_samples)
    print('New data len \n',len(new_data))
    with open(args.json_save_path, "w") as fw:
        json.dump(new_data, fw, indent=4)
    pass


# Tokenize the input text
instruct_i_input_ids = tokenizer.encode(instruct_i, return_tensors="pt", truncation=True,
                                        max_length=args.max_length).to('cpu')
instruct_i_len = instruct_i_input_ids.shape[1]


def get_loss_part_text(tokenizer, text, target_span, max_length, loss_list_):
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=max_length).to('cpu')
    start_index = text.rfind(target_span)
    text_temp = text[:start_index]
    token_id_temp = tokenizer.encode(text_temp)
    start_token = len(token_id_temp)
    end_token_real = input_ids.shape[1]
    loss_list = loss_list_[start_token - 1:end_token_real - 1]
    return end_token_real - start_token, input_ids[0][start_token:end_token_real], np.array(loss_list)


# if args.max_length - instruct_i_len > 0:
#     len_1, token_ids_1, loss_list_1 = get_loss_part_text(tokenizer, direct_answer_text, output_i,
#                                                          args.max_length - instruct_i_len + 4, loss_1_list)
#     len_2, token_ids_2, loss_list_2 = get_loss_part_text(tokenizer, whole_text, output_i, args.max_length, loss_2_list)
#     if len_1 <= 0 or len_2 <= 0:
#         continue
#     if instruct_i_len + len_1 > args.max_length:
#         continue
#     mean_1 = loss_list_1.mean()
#     mean_2 = loss_list_2.mean()
#     mean_rate = mean_2 / mean_1
#     if mean_rate > 1:
#         continue
#     mean_rate_list.append((mean_rate, i))
#     mean_list_1.append((mean_1, i))
#     mean_list_2.append((mean_2, i))
# else:
#     continue


import numpy as np
from .strategy import Strategy
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm


class KCenterGreedy(Strategy):
    def __init__(self, dataset, net):
        super(KCenterGreedy, self).__init__(dataset, net)

    def query(self, n):
        labeled_idxs, train_data = self.dataset.get_train_data()
        embeddings = self.get_embeddings(train_data)
        embeddings = embeddings.numpy()

        dist_mat = np.matmul(embeddings, embeddings.transpose())
        sq = np.array(dist_mat.diagonal()).reshape(len(labeled_idxs), 1)
        dist_mat *= -2
        dist_mat += sq
        dist_mat += sq.transpose()
        dist_mat = np.sqrt(dist_mat)

        mat = dist_mat[~labeled_idxs, :][:, labeled_idxs]

        for i in tqdm(range(n), ncols=100):
            mat_min = mat.min(axis=1)
            q_idx_ = mat_min.argmax()
            q_idx = np.arange(self.dataset.n_pool)[~labeled_idxs][q_idx_]
            labeled_idxs[q_idx] = True
            mat = np.delete(mat, q_idx_, 0)
            mat = np.append(mat, dist_mat[~labeled_idxs, q_idx][:, None], axis=1)

        return np.arange(self.dataset.n_pool)[(self.dataset.labeled_idxs ^ labeled_idxs)]