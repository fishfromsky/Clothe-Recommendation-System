from flask import Flask, jsonify, Response, request
import base64
import numpy as np
import io
import random
import time
import os
import json
import sys
import torch
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


'''
================================================  模型代码  =============================================================
'''

sys.path.insert(0, "../mcn")
import torchvision.transforms as transforms
from model import CompatModel
from utils import prepare_dataloaders
from PIL import Image

train_dataset, _, _, _, test_dataset, _ = prepare_dataloaders(num_workers=1)
# Load pretrained weights
device = torch.device('cpu')
# print(len(.vocabulary)) # 2757
model = CompatModel(embed_size=1000, need_rep=True, vocabulary=2757).to(device)
model.load_state_dict(torch.load("../mcn/model_train_relation_vse_type_cond_scales.pth", map_location="cpu"))
model.eval()
for name, param in model.named_parameters():
    if 'fc' not in name:
        param.requires_grad = False


def defect_detect(img, model, normalize=True):
    # Register hook for comparison matrix
    relation = None

    def func_r(module, grad_in, grad_out):
        nonlocal relation
        relation = grad_in[1].detach()

    for name, module in model.named_modules():
        if name == 'predictor.0':
            module.register_backward_hook(func_r)
    # Forward
    out = model._compute_score(img)
    out = out[0]

    # Backward
    one_hot = torch.FloatTensor([[-1]]).to(device)
    model.zero_grad()
    out.backward(gradient=one_hot, retain_graph=True)

    if normalize:
        relation = relation / (relation.max() - relation.min())
    relation += 1e-3
    return relation, out.item()


def item_diagnosis(relation, select):
    """ Output the most incompatible item in the outfit

    Return:
        result (list): Diagnosis value of each item
        order (list): The indices of items ordered by its importance
    """
    mats = vec2mat(relation, select)
    for m in mats:
        mask = torch.eye(*m.shape).byte()
        m.masked_fill_(mask, 0)
    result = torch.cat(mats).sum(dim=0)
    order = [i for i, j in sorted(enumerate(result), key=lambda x: x[1], reverse=True)]
    return result, order


def vec2mat(relation, select):
    """ Convert relation vector to 4 matrix, which is corresponding to 4 layers
    in the backend CNN.

    Args:
        relation: (np.array | torch.tensor) of shpae (60,)
        select: List of select item indices, e.g. (0, 2, 3) means select 3 items
            in total 5 items in the outfit.

    Return:
        mats: List of matrix
    """
    mats = []
    for idx in range(4):
        mat = torch.zeros(5, 5)
        mat[np.triu_indices(5)] = relation[15 * idx:15 * (idx + 1)]
        mat += torch.triu(mat, 1).transpose(0, 1)
        mat = mat[select, :]
        mat = mat[:, select]
        mats.append(mat)
    return mats


root = "../data"
img_root = os.path.join(root, "images")
json_file = os.path.join(root, "test_no_dup_with_category_3more_name.json")

json_data = json.load(open(json_file))

top_options, bottom_options, shoe_options, bag_options, accessory_options = [], [], [], [], []
print("Load options...")
for cnt, (iid, outfit) in enumerate(json_data.items()):
    if cnt > 20:
        break
    if "upper" in outfit:
        label = os.path.join(iid, str(outfit['upper']['index']))
        value = os.path.join(img_root, label) + ".jpg"
        value = value.replace('\\', '/')
        top_options.append({'label': label, 'value': value})
    if "bottom" in outfit:
        label = os.path.join(iid, str(outfit['bottom']['index']))
        value = os.path.join(img_root, label) + ".jpg"
        value = value.replace('\\', '/')
        bottom_options.append({'label': label, 'value': value})
    if "shoe" in outfit:
        label = os.path.join(iid, str(outfit['shoe']['index']))
        value = os.path.join(img_root, label) + ".jpg"
        value = value.replace('\\', '/')
        shoe_options.append({'label': label, 'value': value})
    if "bag" in outfit:
        label = os.path.join(iid, str(outfit['bag']['index']))
        value = os.path.join(img_root, label) + ".jpg"
        value = value.replace('\\', '/')
        bag_options.append({'label': label, 'value': value})
    if "accessory" in outfit:
        label = os.path.join(iid, str(outfit['accessory']['index']))
        value = os.path.join(img_root, label) + ".jpg"
        value = value.replace('\\', '/')
        accessory_options.append({'label': label, 'value': value})


def item_diagnosis(relation, select):
    """ Output the most incompatible item in the outfit

    Return:
        result (list): Diagnosis value of each item
        order (list): The indices of items ordered by its importance
    """
    mats = vec2mat(relation, select)
    for m in mats:
        mask = torch.eye(*m.shape).byte()
        m.masked_fill_(mask, 0)
    result = torch.cat(mats).sum(dim=0)
    order = [i for i, j in sorted(enumerate(result), key=lambda x: x[1], reverse=True)]
    return result, order


def retrieve_sub(x, select, order):
    """ Retrieve the datset to substitute the worst item for the best choice.
    """
    all_names = {0: 'upper', 1: 'bottom', 2: 'shoe', 3: 'bag', 4: 'accessory'}
    try_most = 20

    best_score = -1
    best_img_path = dict()

    for o in order:
        if best_score > 0.9:
            break
        problem_part_idx = select[o]
        problem_part = all_names[problem_part_idx]
        for outfit in random.sample(test_dataset.data, try_most):
            if best_score > 0.9:
                break
            if problem_part in outfit[1]:
                img_path = os.path.join(test_dataset.root_dir, outfit[0],
                                        str(outfit[1][problem_part]['index'])) + '.jpg'
                img = Image.open(img_path).convert('RGB')
                img = test_dataset.transform(img).to(device)
                x[0][problem_part_idx] = img
                with torch.no_grad():
                    out = model._compute_score(x)
                    score = out[0]
                if score.item() > best_score:
                    best_score = score.item()
                    img_path = img_path.replace('\\', '/')
                    best_img_path[problem_part] = img_path
        x[0][problem_part_idx] = test_dataset.transform(Image.open(best_img_path[problem_part]).convert('RGB')).to(
            device)

        print('problem_part: {}'.format(problem_part))
        print('best substitution: {} {}'.format(problem_part, best_img_path[problem_part]))
        print('After substitution the score is {:.4f}'.format(best_score))
    return best_score, best_img_path


def base64_to_tensor(image_bytes_dict):
    my_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    outfit_tensor = []
    for k, v in image_bytes_dict.items():
        img = base64_to_image(v)
        tensor = my_transforms(img)
        outfit_tensor.append(tensor.squeeze())
    outfit_tensor = torch.stack(outfit_tensor)
    outfit_tensor = outfit_tensor.to(device)
    return outfit_tensor


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    return img


'''
===============================================  后端接口  ==============================================================
'''


def get_options(option):
    response = {'code': 20000, 'data': []}
    try:
        response['data'] = option
    except Exception as e:
        response['code'] = 50000
        response['data'] = [e]

    return response


@app.route('/')
def hello_word():
    return jsonify('hello world')


@app.route('/get_top', methods=['GET'])
def get_top():
    return jsonify(get_options(top_options))


@app.route('/get_bottom', methods=['GET'])
def get_bottom():
    return jsonify(get_options(bottom_options))


@app.route('/get_shoe', methods=['GET'])
def get_shoe():
    return jsonify(get_options(shoe_options))


@app.route('/get_accessory', methods=['GET'])
def get_accessory():
    return jsonify(get_options(accessory_options))


@app.route('/get_bag', methods=['GET'])
def get_bag():
    return jsonify(get_options(bag_options))


@app.route('/get_pic/<foldId>/<imgId>.jpg', methods=['GET'])
def get_pic(foldId, imgId):
    with open(os.path.dirname(__file__)[:-3]+'/data/images/{}/{}.jpg'.format(foldId, imgId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp


def path_transfer(fname):
    encoded_img = base64.b64encode(open(fname, "rb").read())
    return 'data:image/png;base64,{}'.format(
        encoded_img.decode())


@app.route('/evaluate', methods=['POST'])
def update_output():
    response = {'code': 20000, 'message': 'success'}
    data = request.json
    n_clicks = 1
    top = path_transfer(data.get('top'))
    bottom = path_transfer(data.get('bottom'))
    shoe = path_transfer(data.get('shoe'))
    bag = path_transfer(data.get('bag'))
    accessory = path_transfer(data.get('accessory'))

    if n_clicks > 0:
        img_dict = {
            "top": top.split(',')[1],
            "bottom": bottom.split(',')[1],
            "shoe": shoe.split(',')[1],
            "bag": bag.split(',')[1],
            "accessory": accessory.split(',')[1]
        }
        img_tensor = base64_to_tensor(img_dict)
        img_tensor.unsqueeze_(0)
        relation, score = defect_detect(img_tensor, model)
        relation = relation.squeeze()
        result, order = item_diagnosis(relation, select=[0, 1, 2, 3, 4])
        best_score, best_img_path = retrieve_sub(img_tensor, [0, 1, 2, 3, 4], order)

        response['best_img_path'] = best_img_path
        response['score'] = score
        response['best_score'] = best_score

        return jsonify(response)


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
