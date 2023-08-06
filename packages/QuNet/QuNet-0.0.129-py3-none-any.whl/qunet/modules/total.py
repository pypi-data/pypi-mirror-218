from inspect import isfunction
import torch, torch.nn as nn
import torch.nn.functional as F
#===============================================================================

class LayerNormChannels(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.norm = nn.LayerNorm(channels)

    def forward(self, x):           # (B,C,H,W,...)
        x = x.transpose(1, -1)      # (B,W,H,...,C)
        x = self.norm(x)            # avg on index c, 2*C parameters
        x = x.transpose(-1, 1)      # (B,C,H,W,...)
        return x

#===============================================================================

class ShiftFeatures(nn.Module):
    def __init__(self, std=0.5):
        super().__init__()
        self.std = std

    def forward(self, x):           # (B,E) or (B,T,E) or (B,E,H,W) or (B,E,D,H,W)
        if self.std == 0.0:
            return x
        
        if x.dim() == 2:
            B,E = x.shape
            return x + self.std * torch.randn(B,E)
        if x.dim() == 3:
            B,_,E = x.shape
            return x + self.std * torch.randn(B,1,E)
        if x.dim() == 4:
            B,C,_,_ = x.shape
            return x + self.std * torch.randn(B,C,1,1)
        if x.dim() == 5:
            B,C,_,_,_ = x.shape
            return x + self.std * torch.randn(B,C,1,1,1)
                
        assert False, f"Wrong dim of tensor x: {x.shape}"

#===============================================================================
#
#===============================================================================

def get_activation(activation, inplace=True):
    """
    Create activation layer from string/function.

    Args
    ----------
    activation (function, or str, or nn.Module):
        Activation function or name of activation function.
    inplace (bool: True)

    Returns
    -------
    nn.Module
        Activation layer.
    """
    assert (activation is not None)
    if isfunction(activation):
        return activation()
    elif isinstance(activation, str):
        if activation     == "sigmoid":
            return  nn.Sigmoid()
        elif activation   == "tanh":
            return nn.Tanh()
        elif activation   == "gelu":
            return  nn.GELU()    
        elif activation   == "relu":
            return nn.ReLU(inplace=inplace)
        elif activation == "relu6":
            return nn.ReLU6(inplace=inplace)
        elif activation == "swish":
            return  lambda x: x * torch.sigmoid(x)                      # Swish()  https://arxiv.org/abs/1710.05941.
        elif activation == "hswish":
            return lambda x: x * F.relu6(x+3.0, inplace=inplace) / 6.0  # HSwish() https://arxiv.org/abs/1905.02244.
        elif activation == "hsigmoid":
            return lambda x: F.relu6(x+3.0, inplace=inplace) / 6.0      # HSigmoid() https://arxiv.org/abs/1905.02244.
        
        else:
            raise NotImplementedError()
    else:
        assert isinstance(activation, nn.Module)
        return activation

#===============================================================================


def get_norm(E,  norm, dim):
    if norm == 1:
        return nn.BatchNorm1d(E)    if dim==1 else nn.BatchNorm2d(E) 
    if norm == 2:
        return nn.LayerNorm (E)     if dim==1 else LayerNormChannels(E)
    if norm == 3:
        return nn.InstanceNorm1d(E) if dim==1 else nn.InstanceNorm2d(E)
    return nn.Identity()

#===============================================================================

def get_dropout(dim, p=0):
    if dim == 1:
        return nn.Dropout(p)
    if dim == 2:
        return nn.Dropout2d(p)        
    return nn.Identity()

#---------------------------------------------------------------------------

def set_dropout(model, p=0.):
    """
    Set dropout rates of DropoutXd to value p. It may be float or list of floats
    """
    layers = get_model_layers(model, kind=(nn.Dropout, nn.Dropout1d, nn.Dropout2d, nn.Dropout3d))

    if type(p) in (int, float):
        p = [p]

    for i,layer in enumerate(layers):
            layer.p = p[ min(i, len(p)-1) ]

#---------------------------------------------------------------------------

def set_shift(model, std=0.):
    """
    Set shift  std of ShiftFeatures to value std. It may be float or list of floats
    """
    layers = get_model_layers(model, kind=(ShiftFeatures))

    if type(std) in (int, float):
        std = [std]

    for i,layer in enumerate(layers):
            layer.std = std[ min(i, len(std)-1) ]

#===============================================================================

def get_model_layers(model, kind, layers=[]):        
    """Get a list of model layers of type kind

    Example:
    ----------
    layers = get_model_layers(model, (nn.Dropout1d, nn.Dropout2d) )
    """
    for mo in model.children():
        if isinstance(mo, kind):
            layers.append(mo)
        else:
            layers = get_model_layers(mo, kind, layers=layers)
    return layers
