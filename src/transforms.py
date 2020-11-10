import torch
import torchvision.transforms.functional
from typing import Dict, Tuple


class random_v_flip:
    def __init__(self, rate: float = 0.5) -> None:
        self.rate = rate
        self.fun = torch.jit.script(torchvision.transforms.functional.vflip)

    def __call__(self, data_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Randomly flips the mask vertically.

        :param data_dict Dict[str, torch.Tensor]: data_dictionary from a dataloader. Has keys:
            key : val
            'image' : torch.Tensor of size [C, X, Y] where C is the number of colors, X,Y are the mask height and width
            'masks' : torch.Tensor of size [I, X, Y] where I is the number of identifiable objects in the mask
            'boxes' : torch.Tensor of size [I, 4] where each box is [x1, y1, x2, y2]
            'labels' : torch.Tensor of size [I] class label for each instance

        :return: Dict[str, torch.Tensor]
        """

        if torch.randn(1) < self.rate:
            data_dict['image'] = self.fun(data_dict['image'])
            data_dict['masks'] = self.fun(data_dict['masks'])

        return data_dict


class random_h_flip:
    def __init__(self, rate: float = 0.5) -> None:
        self.rate = rate
        self.fun = torch.jit.script(torchvision.transforms.functional.hflip)

    def __call__(self, data_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Randomly flips the mask vertically.

        :param data_dict Dict[str, torch.Tensor]: data_dictionary from a dataloader. Has keys:
            key : val
            'mask' : torch.Tensor of size [C, X, Y] where C is the number of colors, X,Y are the mask height and width
            'masks' : torch.Tensor of size [I, X, Y] where I is the number of identifiable objects in the mask
            'boxes' : torch.Tensor of size [I, 4] where each box is [x1, y1, x2, y2]
            'labels' : torch.Tensor of size [I] class label for each instance

        :return: Dict[str, torch.Tensor]
        """

        if torch.randn(1) < self.rate:
            data_dict['image'] = self.fun(data_dict['image'])
            data_dict['masks'] = self.fun(data_dict['masks'])

        return data_dict


class gaussian_blur:
    def __init__(self, kernel_targets: torch.Tensor = torch.tensor([3, 5, 7]), rate: float = 0.5) -> None:
        self.kernel_targets = kernel_targets
        self.rate = rate

    def __call__(self, data_dict):
        """
        Randomly applies a gaussian blur

        :param data_dict Dict[str, torch.Tensor]: data_dictionary from a dataloader. Has keys:
            key : val
            'mask' : torch.Tensor of size [C, X, Y] where C is the number of colors, X,Y are the mask height and width
            'masks' : torch.Tensor of size [I, X, Y] where I is the number of identifiable objects in the mask
            'boxes' : torch.Tensor of size [I, 4] where each box is [x1, y1, x2, y2]
            'labels' : torch.Tensor of size [I] class label for each instance

        :return: Dict[str, torch.Tensor]
        """
        if torch.randn(1) < self.rate:
            kern = self.kernel_targets[int(torch.randint(0, len(self.kernel_targets), (1, 1)).item())].item()
            data_dict['image'] = torchvision.transforms.functional.gaussian_blur(data_dict['image'], kern)
        return data_dict


class random_resize:
    def __init__(self, rate: float = 0.5, scale: tuple = (300, 1440)) -> None:
        self.rate = rate
        self.scale = scale

    def __call__(self, data_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Randomly resizes an mask

        :param data_dict Dict[str, torch.Tensor]: data_dictionary from a dataloader. Has keys:
            key : val
            'mask' : torch.Tensor of size [C, X, Y] where C is the number of colors, X,Y are the mask height and width
            'masks' : torch.Tensor of size [I, X, Y] where I is the number of identifiable objects in the mask
            'boxes' : torch.Tensor of size [I, 4] where each box is [x1, y1, x2, y2]
            'labels' : torch.Tensor of size [I] class label for each instance

        :return: Dict[str, torch.Tensor]
        """
        if torch.randn(1) < self.rate:
            size = torch.randint(self.scale[0], self.scale[1], (1, 1)).item()
            data_dict['image'] = torchvision.transforms.functional.resize(data_dict['image'], size)
            data_dict['masks'] = torchvision.transforms.functional.resize(data_dict['masks'], size)

        return data_dict


class adjust_brightness:
    def __init__(self, rate=.5, range_brightness=(.3, 1.7)):
        self.rate = rate
        self.range = range_brightness
        self.fun = torch.jit.script(torchvision.transforms.functional.adjust_brightness)

    def __call__(self, data_dict):

        val = torch.FloatTensor(1).uniform_(self.range[0], self.range[1])
        if torch.randn(1) < self.rate:
            data_dict['image'] = self.fun(data_dict['image'], val)

        return data_dict


# needs docstring
class adjust_contrast:
    def __init__(self, rate: float = 0.5, range_contrast: tuple = (.3, 1.7)) -> None:
        self.rate = rate
        self.range = range_contrast
        self.fun = torch.jit.script(torchvision.transforms.functional.adjust_brightness)

    def __call__(self, data_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:

        if torch.randn(1) < self.rate:
            val = torch.FloatTensor(1).uniform_(self.range[0], self.range[1])  # .to(image.device)
            data_dict['image'] = torchvision.transforms.functional.adjust_contrast(data_dict['image'], val)

        return data_dict


# needs docstring
class random_affine:
    def __init__(self, rate: float = 0.5, angle: Tuple[int, int] = (-180, 180),
                 shear: Tuple[int, int] = (-45, 45), scale: Tuple[float, float] = (0.9, 1.5)) -> None:
        self.rate = rate
        self.angle = angle
        self.shear = shear
        self.scale = scale

    def __call__(self, data_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        if torch.randn(1) < self.rate:
            angle = torch.FloatTensor(1).uniform_(self.angle[0], self.angle[1]).to(self.device)
            shear = torch.FloatTensor(1).uniform_(self.shear[0], self.shear[1]).to(self.device)
            scale = torch.FloatTensor(1).uniform_(self.scale[0], self.scale[1]).to(self.device)
            translate = torch.tensor([0, 0])

            data_dict['image'] = _affine(data_dict['image'], angle, translate, scale, shear)
            data_dict['masks'] = _affine(data_dict['masks'], angle, translate, scale, shear)

        return data_dict


# Needs Docstring
class to_cuda:
    def __init__(self):
        pass

    def __call__(self, data_dict: Dict[str, torch.Tensor] = None) -> Dict[str, torch.Tensor]:
        for key in data_dict:
            data_dict[key] = data_dict[key].cuda()
        return data_dict


# Needs Docstring
class to_tensor:
    def __init__(self):
        pass

    def __call__(self, data_dict):
        data_dict['image'] = torchvision.transforms.functional.to_tensor(data_dict['image'])

        return data_dict


class correct_boxes:
    def __init__(self):
        pass

    def __call__(self, data_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Other geometric transforms may have removed some of the visible stereocillia. We use this transform to infer new
        bounding boxes from the old masks and remove instances (I) where  there was no segmentation mask.

        :param data_dict Dict[str, torch.Tensor]: data_dictionary from a dataloader. Has keys:
            key : val
            'image' : torch.Tensor of size [C, X, Y] where C is the number of colors, X,Y are the mask height and width
            'masks' : torch.Tensor of size [I, X, Y] where I is the number of identifiable objects in the mask
            'boxes' : torch.Tensor of size [I, 4] where each box is [x1, y1, x2, y2]
            'labels' : torch.Tensor of size [I] class label for each instance

        :return: Dict[str, torch.Tensor]
        """

        return _correct_box(image=data_dict['image'], masks=data_dict['masks'], labels=data_dict['labels'])


class stack_image:
    def __init__(self):
        pass

    def __call__(self, data_dict):
        data_dict['image'] = torch.cat((data_dict['image'], data_dict['image'], data_dict['image']), dim=0)
        return data_dict

@torch.jit.script
def get_box_from_mask(mask: torch.Tensor) -> torch.Tensor:
    """
    Returns the bounding box for a particular segmentation mask
    :param: mask torch.Tensor[X,Y] some mask where 0 is background and !0 is a segmentation mask
    :return: torch.Tensor[4] coordinates of the box surrounding the segmentation mask [x1, y1, x2, y2]
    """
    ind = torch.nonzero(mask)

    if ind.shape[0] == 0:
        box = torch.tensor([0, 0, 0, 0])

    else:
        box = torch.empty(4).to(mask.device)
        x = ind[:, 1]
        y = ind[:, 0]
        torch.stack((torch.min(x), torch.min(y), torch.max(x), torch.max(y)), out=box)

    return box


@torch.jit.script
def _correct_box(image: torch.Tensor,  masks: torch.Tensor, labels: torch.Tensor) -> Dict[str, torch.Tensor]:

    boxes = torch.cat([get_box_from_mask(m).unsqueeze(0) for m in masks], dim=0)
    ind = torch.tensor([m.max().item() > 0 for m in masks], dtype=torch.bool)

    return {'image': image, 'masks': masks[ind, :, :], 'boxes': boxes[ind, :], 'labels': labels[ind]}


@torch.jit.script
def _affine(img: torch.Tensor, angle: torch.Tensor, translate: torch.Tensor, scale: torch.Tensor, shear: torch.Tensor) -> torch.Tensor:
    angle = float(angle.item())
    scale = float(scale.item())
    shear = [float(shear.item())]
    translate_list = [int(translate[0].item()), int(translate[1].item())]
    return torchvision.transforms.functional.affine(img, angle, translate_list, scale, shear)
