#coding:utf-8
from PIL import Image, ImageDraw


def getwidth(tree):
    if tree.tb == None and tree.fb == None:
        return 1
    return getwidth(tree.tb) + getwidth(tree.fb)


def getdepth(tree):
    if tree.tb == None and tree.fb == None:
        return 0
    return max(getdepth(tree.tb), getdepth(tree.fb)) + 1


def draw_tree(tree, jpeg='tree.jpg'):
    w = getwidth(tree) * 100
    h = getdepth(tree) * 100 + 120

    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw_node(draw, tree, w/2, 20)
    img.save(jpeg, 'JPEG')


def draw_node(draw, tree, x, y):
    if tree.results == None:
        w1 = getwidth(tree.fb) * 100
        w2 = getwidth(tree.tb) * 100

        left = x -(w1 + w2) / 2
        right = x + (w1 + w2) / 2

        draw.text((x - 20, y - 10),
                str(tree.col) + ":" + str(tree.value), (0, 0, 0))

        draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
        draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))

        draw_node(draw, tree.fb, left + w1 / 2, y + 100)
        draw_node(draw, tree.tb, right - w2 / 2, y + 100)
    else:
        text = " \n".join(['%s:%d' % v for v in tree.results.items()])
        draw.text((x - 20, y), text, (0, 0, 0))


if __name__ == "__main__":
    from data import my_data
    from decision_tree import *
    tree = build_tree(my_data)
    draw_tree(tree, jpeg='treeview.jpg')
