def get_utf8_tree(node):
    """Taken from
    https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python"""

    LINE = "─"
    DOWN_LEFT_F = "┌"
    DOWN_RIGHT_F = "┐"
    DOWN_LEFT = "│"
    DOWN_RIGHT = "│"

    if node.right is None and node.left is None:
        line = str(node.data)
        #line = hex(id(node))
        width = len(line)
        height = 1
        middle = width // 2
        return [line], width, height, middle

    if node.right is None:
        lines, n, p, x = get_utf8_tree(node.left)
        s = str(node.data)
        #s = hex(id(node))
        u = len(s)
        first_line = (x) * " " + DOWN_LEFT_F + (n - x - 1) * LINE + s
        second_line = x * "" + DOWN_LEFT + (n - x - 1 + u) * " "
        shifted_lines = [line + u * " " for line in lines]
        return [first_line, second_line] + shifted_lines, n+u, p+2, n+u//2

    if node.left is None:
        lines, n, p, x = get_utf8_tree(node.right)
        s = str(node.data)
        #s = hex(id(node))
        u = len(s)
        first_line = s+ (x+1) * LINE + DOWN_RIGHT_F + (n - x - 1) * " "
        second_line = (u+x+1) * " " + DOWN_RIGHT + (n - x - 1) * " "
        shifted_lines = [u * " " + line for line in lines]
        return [first_line, second_line] + shifted_lines, n+u, p+2, u//2

    left, n, p, x = get_utf8_tree(node.left)
    right, m, q, y = get_utf8_tree(node.right)
    s = str(node.data)
    #s = hex(id(node))
    u = len(s)
    first_line = (x + 1 - 1) * ' ' + DOWN_LEFT_F \
            + (n - x - 1) * LINE + s + y * LINE + DOWN_RIGHT_F \
            + (m - y - 1) * ' '
    second_line = x * ' ' + DOWN_LEFT + (n - x - 1 + u + y) * ' ' + \
            DOWN_RIGHT + (m - y - 1) * ' '
    if p < q:
        left += [n * ' '] * (q - p)
    elif q < p:
        right += [m * ' '] * (p - q)
    zipped_lines = zip(left, right)
    lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
    return lines, n + m + u, max(p, q) + 2, n + u // 2


def print_tree(node, space=0, char=""):
    pad = 1

    if node is not None:
        print_tree(node.right, space + pad, "/")
        print(space *" " + char + "{}".format(str(node.data)))
        print_tree(node.left, space + pad, "\\")


