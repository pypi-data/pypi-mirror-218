
def ignore_warning():
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)


def set_plot_formats(formats='svg'):
    from matplotlib_inline import backend_inline
    backend_inline.set_matplotlib_formats(formats)


def try_use_device(cuda=True, tensor=True):
    import torch
    if cuda and torch.cuda.is_available():
        device = torch.device("cuda")
        type = torch.cuda.FloatTensor
    else:
        device = torch.device("cpu")
        type = torch.FloatTensor

    if tensor:
        torch.set_default_tensor_type(type)

    torch.set_default_device(device)
    return device


def load_model(model, filename):
    import torch
    model.load_state_dict(torch.load(filename))
    model.eval()
    return model


def save_model(model, filename):
    import os
    import torch

    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    torch.save(model.state_dict(), filename)


def save_module(model, filename):
    from .attrdict import attrdict
    import pickle
    import os
    attr = attrdict()
    attr.classname = type(model)
    attr.state_dict = model.state_dict()

    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, 'wb') as file:
        file.write(pickle.dumps(attr))


def load_module(filename):
    import pickle
    with open(filename, 'rb') as file:
        attr = pickle.loads(file.read())

    model = attr.classname()
    model.load_state_dict(attr.state_dict)
    model.eval()
    return model


def metrics(y_true, y_pred):
    from .attrdict import attrdict
    from sklearn import metrics as m
    import math

    scores = attrdict()
    scores.mape = m.mean_absolute_percentage_error(y_true, y_pred)
    scores.mse = m.mean_squared_error(y_true, y_pred)
    scores.rmse = math.sqrt(scores.mse)
    scores.mae = m.mean_absolute_error(y_true, y_pred)
    scores.vs = m.explained_variance_score(y_true, y_pred)
    scores.r2 = m.r2_score(y_true, y_pred)

    return scores
