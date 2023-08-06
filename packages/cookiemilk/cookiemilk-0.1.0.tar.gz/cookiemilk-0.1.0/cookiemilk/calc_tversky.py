#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calc_tversky(
        graph1,
        graph2,
        comparison,
        alpha=0.5
):
    # Error messages
    if comparison not in ['conceptual', 'propositional', 'semantic']:
        raise ValueError('The value of "comparison" is unrecognized. It must be one of "conceptual", "propositional", '
                         'or "semantic"!')

    # Calculation
    if comparison == 'conceptual':
        s = conceptual(graph1, graph2, alpha)

    elif comparison == 'propositional':
        s = propositional(graph1, graph2, alpha)

    elif comparison == 'semantic':
        s_c = conceptual(graph1, graph2, alpha)
        s_p = propositional(graph1, graph2, alpha)
        s = s_p / s_c

    return float('%.4f' % s)


def conceptual(
        graph1,
        graph2,
        alpha
):
    set1 = set(graph1.nodes)
    set2 = set(graph2.nodes)

    beta = 1 - alpha
    s = len(set1 & set2) / (len(set1 & set2) + alpha * len(set1 - set2) + beta * len(set2 - set1))

    return s


def propositional(
        graph1,
        graph2,
        alpha
):
    beta = 1 - alpha

    edges1 = set(graph1.edges())
    edges2 = set(graph2.edges())

    intersection = edges1.intersection(edges2)
    dif_graph1 = edges1 - edges2
    dif_graph2 = edges2 - edges1

    s = len(intersection) / (len(intersection) + alpha * len(dif_graph1) + beta * len(dif_graph2))

    return s
