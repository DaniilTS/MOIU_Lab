from copy import copy


def deikstra(net, s, t):
    if s == t or s not in net or t not in net:
        return None

    labels, order = {}, {}

    for i in net.keys():
        if i == s:
            labels[i] = 0
        else:
            labels[i] = float("inf")

    drop1 = copy(labels)  # used for looping
    while len(drop1) > 0:
        minNode = min(drop1, key=drop1.get)
        minNode_net = net[minNode]
        for i in minNode_net:
            minNode_label = labels[minNode]
            i_minNode_net = minNode_net[i]
            if labels[i] > (minNode_label + i_minNode_net):
                labels[i] = minNode_label + i_minNode_net
                drop1[i] = minNode_label + i_minNode_net
                order[i] = minNode
        del drop1[minNode]

    temp, rpath, path = copy(t), [], []
    while 1:
        rpath.append(temp)
        if temp in order:
            temp = order[temp]
        else:
            return None  # no path
        if temp == s:
            rpath.append(temp)
            break

    for j in range(len(rpath) - 1, -1, -1):
        path.append(rpath[j])

    return {
        'path': path,
        'weight': labels[t]
    }


net = {
    '1': {
        '2': 3,
        '3': 6
    },
    '2': {
        '3': 1
    },
    '3': {
        '2': 2,
        '4': 1
    },
    '4': {

    },
}

print(deikstra(net, s='1', t='4'))
