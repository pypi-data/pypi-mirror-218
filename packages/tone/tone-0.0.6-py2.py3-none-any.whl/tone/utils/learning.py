
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
