import os, sys
import shutil
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import matplotlib


class Reshape(nn.Module):
    def __init__(self, *args):
        super(Reshape, self).__init__()
        self.shape = args

    def forward(self, x):
        return x.view(self.shape)


def get_rgba_from_cmap(cmap, val):
    cmap = matplotlib.cm.get_cmap(cmap)
    return np.asarray(cmap(val)).reshape(1, -1)


def get_device(gpu_id):
    if torch.cuda.is_available():
        device = torch.device(f'cuda:{gpu_id}')
    else:
        device = torch.device(f'cpu')
    return device


def get_coloset_elem_dist(row, arr):
    assert len(arr.shape) == 2
    row = np.asarray(row)
    dist = np.sum((arr - row) ** 2, axis=1, keepdims=True)
    idx_min = dist.argmin(axis=0)[0]
    return dist[idx_min], idx_min


def get_row_index_in_arr(row, arr):
    assert len(arr.shape) == 2
    row = np.asarray(row)
    min_dist, min_dist_idx = get_coloset_elem_dist(row, arr)
    return min_dist_idx if min_dist < 1e-6 else False


def make_path_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_path(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def remove_make_path(path):
    remove_path(path)
    os.makedirs(path)


def copy_move_file(source, target):
    shutil.copy(source, target)


def draw_confusion_matrix(y_pred, y_true):
    # https: // vitalflux.com / accuracy - precision - recall - f1 - score - python - example /
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

    conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')

    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    plt.savefig('confusion_matrix.png')
    print('Num. of Obj.: %.3d' % len(y_true))
    print('Num. Pos./ Num. Neg.: {}/{}'.format(y_true.count(1), y_true.count(0)))
    print('Precision: %.3f' % precision_score(y_true, y_pred))
    print('Recall: %.3f' % recall_score(y_true, y_pred))
    print('Accuracy: %.3f' % accuracy_score(y_true, y_pred))
    print('F1 Score: %.3f' % f1_score(y_true, y_pred))


def to_np(x, dtype=np.float32):
    return np.asarray(x, dtype=dtype)


def to_th(x, device, dtype=torch.float32):
    return torch.as_tensor(x, dtype=dtype, device=device)


def get_tianshou_envs(make_env, args):
    import tianshou as ts
    training_env = make_env(mode='training', args=args)
    test_env = make_env(mode='test', args=args)
    train_envs = ts.env.DummyVectorEnv(
        [lambda: make_env(mode='training', args=args) for _ in range(args.training_num)])
    train_envs2 = ts.env.DummyVectorEnv(
        [lambda: make_env(mode='train_for_test', args=args) for _ in range(args.training_num)])
    test_envs = ts.env.DummyVectorEnv(
        [lambda: make_env(mode='test', args=args) for _ in range(args.test_num)])
    return training_env, test_env, train_envs, train_envs2, test_envs


def get_tianshou_logger(log_dir):
    from tianshou.utils import TensorboardLogger
    from torch.utils.tensorboard import SummaryWriter
    return TensorboardLogger(SummaryWriter(log_dir))


def get_encoder_and_decoder(dim, hidden_dim, z_dim, hidden_sizes_for_enc=None):
    import numpy as np
    import torch
    import torch.nn as nn
    from tianshou.utils.net.common import MLP

    if isinstance(dim, tuple) and len(dim) == 3:  # img
        c, h, w = dim
        cnn = nn.Sequential(
            nn.Conv2d(c, 8, kernel_size=4, stride=2), nn.ReLU(inplace=True),
            nn.Conv2d(8, 16, kernel_size=2, stride=1), nn.ReLU(inplace=True),
        )
        with torch.no_grad():
            unflatten_dim = cnn(torch.zeros(1, c, h, w)).shape[1:]
            flatten_dim = int(np.prod(unflatten_dim))

        enc = nn.Sequential(
            cnn,
            nn.Flatten(),
            nn.Linear(flatten_dim, hidden_dim), nn.ReLU(inplace=True),
            # nn.LayerNorm(hidden_dim),
            nn.Linear(hidden_dim, 2 * z_dim)
        )

        dec = nn.Sequential(
            nn.Linear(z_dim, flatten_dim), nn.ReLU(inplace=True),
            Reshape(-1, *unflatten_dim),
            nn.ConvTranspose2d(16, 8, kernel_size=2, stride=1), nn.ReLU(inplace=True),
            nn.ConvTranspose2d(8, c, kernel_size=4, stride=2), nn.ReLU(inplace=True),
        )

    else:
        if len(dim) == 1:
            dim = dim[0]
        if hidden_sizes_for_enc is None:
            hidden_sizes_for_enc = [hidden_dim] * 3

        enc = MLP(input_dim=dim, output_dim=2 * z_dim, hidden_sizes=hidden_sizes_for_enc)
        dec = MLP(input_dim=z_dim, output_dim=dim, hidden_sizes=[hidden_dim])

    return enc, dec


def load_pickle(path):
    import pickle
    return pickle.load(open(path, 'rb'))


def load_config(config_path, config_name):
    import os
    import yaml
    with open(os.path.join(config_path, config_name)) as file:
        config = yaml.safe_load(file)
    return config
