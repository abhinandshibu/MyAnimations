from manim import *
from tools.font_centering_pos import FUTURA_CENTERING_POS


class BasicGraph(VMobject):
    """An undirected graph. Which focuses on aesthetics for teaching purposes.

    Parameters
    ----------

    vertices
        A dictionary containing the vertices names and positions (2 element
        list or tuple).
    edges
        A list of edges, specified as tuples ``(u, v)`` where both ``u``
        and ``v`` are the vertices names.
    label_type
        Specifies whether or not the vertices are labeled; if ``None`` vertices
        are unlabeled. If not, it specifies the mobject class of the label
        (default is ``Text``).
    label_default
        A dictionary specifying the default attributes of ``label_type``.
    label_config
        A dictionary containing the vertices names and corresponding attributes
        to that label. It builds on top of the attributes contained in
        label_default.
    vertex_default
        Specifies a mobject instance which will display the vertices.
    vertex_config
        A dictionary containing the vertices names and corresponding mobject
        instance which will display that vertex.
    vertex_and_label_scale
        Scales the size of the vertices and labels together.
    edge_default
        Specifies a mobject instance which will display the edges.
    edge_config
        A dictionary containing the edges and corresponding mobject instance
        which will display that edge.
    weight
        A dictionary containing the edges as keys and a list of 2 elements
        containing the corresponding weight as an ``Integer`` and a pair
        describing how the weight should be placed relative to the middle
        of the line eg. (-0.25, 0.2).

    .. note::

        If label ``font=futura`` then it will automatically center the text
        for aesthetics. Individual capital letters were centered with reference
        to a circle of ``radius=0.5``.

    .. note ::

        Preferred methods of rendering are ``ShowCreation`` and ``Uncreate``.
        FadeIn and FadeOut do not work very well.

    Examples
    --------

    First, we create an unlabeled graph.

    .. manim:: UnlabeledGraph

        class UnlabeledGraph(Scene):
            def construct(self):
                graph = BasicGraph(
                    vertices={"A": [0, 0], "B": [1, 0], "C": [1, 1],
                              "D": [0, 1], "E": [-1, 1]},
                    edges=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
                            ("A", "E"), ("D", "E")],
                    label_type=None,
                    vertex_default=Dot()
                )

                self.add(graph)

    We can similarly create labeled graphs.

    .. manim:: LabeledGraph

        class LabeledGraph(Scene):
            def construct(self):
                graph = BasicGraph(
                    vertices={"A": [0, 0], "B": [2, 0], "C": [2, 2],
                              "D": [0, 2], "E": [-1, 1]},
                    edges=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
                           ("A", "E"), ("E", "D")],
                    vertex_and_label_scale=0.75
                )

                self.add(graph)

    We can change certain vertices and edges.

    .. manim:: ChangeConfigs

        class ChangeConfigs(Scene):
            def construct(self):
                graph = BasicGraph(
                    vertices={"A": [0, 0], "B": [2, 0], "C": [2, 2],
                              "D": [0, 2], "E": [-1, 1]},
                    edges=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
                            ("A", "E"), ("E", "D")],
                    vertex_and_label_scale=0.75,
                    edge_config={("A", "B"): DashedLine(),
                                 ("B", "C"): Line(color=BLUE)},
                    vertex_config={"E": Dot(radius=0.3),
                                   "D": Square(side_length=0.7, fill_opacity=1,
                                               fill_color=BLACK)},
                    label_config={"E": {"color": BLACK}},
                )
                self.add(graph)

    We can add nodes and edges to the graph.

    .. manim:: AddingToGraph

        class AddingToGraph(Scene):
            def construct(self):
                vertices = {"A": [0, 0], "B": [2, 0], "C": [0, 2], "D": [2, 2]}
                edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]

                g1 = BasicGraph(
                    vertices=vertices,
                    edges=edges,
                    vertex_and_label_scale=0.8,
                )

                self.play(Write(g1))
                self.wait()

                vertices["E"] = [-1, 1]
                vertices["F"] = [1, -2]
                edges.append(("E", "A"))
                edges.append(("E", "C"))
                edges.append(("F", "A"))
                edges.append(("F", "B"))

                g2 = BasicGraph(
                    vertices=vertices,
                    edges=edges,
                    vertex_and_label_scale=0.8,
                )

                BasicGraph.basic_transform_expand(self, g1, g2)
    """

    def __init__(self,
                 vertices={},
                 edges=[],
                 label_type=Text,
                 label_default={"font": "futura"},
                 label_config={},
                 vertex_default=Circle(color=BLUE, radius=0.5, fill_opacity=1,
                                       fill_color=BLACK),
                 vertex_config={},
                 vertex_and_label_scale=1,
                 edge_default=Line().set_stroke(width=6),
                 edge_config={},
                 weight={},
                 **kwargs
                 ):

        # turns the vertex positions (can be 2 element list or tuple)
        # into an np array
        self.vertices = {
            vertex: np.array(list(pos) + [0]) for vertex, pos in
            vertices.items()
        }

        self.edges = edges
        self.label_type = label_type
        self.label_default = label_default
        self.label_config = label_config
        self.vertex_default = vertex_default
        self.vertex_config = vertex_config
        self.vertex_and_label_scale = vertex_and_label_scale
        self.edge_default = edge_default
        self.edge_config = edge_config
        self.weight = weight
        VMobject.__init__(self, **kwargs)

        self.add(VGroup(*self.add_vertices()).set_z_index(4))
        if self.label_type is not None:
            self.add(VGroup(*self.add_labels()).set_z_index(5))
        self.add(VGroup(*self.add_edges_weights()).set_z_index(3))

    def add_vertices(self):
        out_vertices = []

        # adds vertices
        for v in self.vertices:
            if v in self.vertex_config:
                vertex_image = self.vertex_config[v]
            else:
                vertex_image = self.vertex_default.copy()

            vertex_image.scale(self.vertex_and_label_scale) \
                .shift(self.vertices[v])
            out_vertices.append(vertex_image)

        return out_vertices

    def add_labels(self):
        out_labels = []

        # adds labels
        for v in self.vertices:
            if v in self.label_config:
                label_attr = self.label_default.copy()
                label_attr.update(self.label_config[v])
                label_image = self.label_type(text=v, **label_attr)
            else:
                label_image = self.label_type(text=v, **self.label_default)

            label_image.move_to(FUTURA_CENTERING_POS[v]) \
                .scale(self.vertex_and_label_scale, about_point=ORIGIN) \
                .shift(self.vertices[v])
            out_labels.append(label_image)

        return out_labels

    def add_edges_weights(self):
        out_edges_weights = []

        # adds edges and weights
        for (v1, v2) in self.edges:
            # add edge
            if (v1, v2) in self.edge_config:
                edge_image = self.edge_config[(v1, v2)]
            else:
                edge_image = self.edge_default.copy()
            edge_image.put_start_and_end_on(self.vertices[v1],
                                            self.vertices[v2])
            out_edges_weights.append(edge_image)

            # add weight
            if (v1, v2) in self.weight:
                weight_image = Text(
                    str(self.weight[(v1, v2)][0]),
                    font=self.label_default["font"]
                )
                weight_image.move_to(edge_image) \
                    .shift(
                    self.weight[(v1, v2)][1][0] * RIGHT +
                    self.weight[(v1, v2)][1][1] * UP
                )
                out_edges_weights.append(weight_image)

        return out_edges_weights

    # since normal wait breaks the graphs displays, tacky solution for now
    @staticmethod
    def wait(self_scene, t=1):
        self_scene.play(FadeIn(Dot(fill_opacity=0), run_time=t))

    # returns a 2D list of mobjects (except for weight), each sublist consists
    # of all the mobjects associated to an edge, ordered as
    # [weight (number), edge, vertex1, label1, vertex2, label2, weight]
    # with the sublist as a mobject being centered at the ``ORIGIN``.
    # the length of the edges in manim are computed via
    # ``edge_weight_scale * weight`` instead of the distance between the two
    # vertices as seen in the graph.
    # pre-condition: has to be weighted on all edges

    @staticmethod
    def decompose_graph(g, edge_weight_scale=0.5):
        out = []

        # adds vertices, labels, edges and weights
        for (v1, v2) in g.edges:
            # building the sublist consisting of all mobjects associated with
            # an edge
            edge_weight = g.weight[(v1, v2)][0]
            out_edge = [edge_weight]

            # add edge
            if (v1, v2) in g.edge_config:
                edge_image = g.edge_config[(v1, v2)]
            else:
                edge_image = g.edge_default.copy()
            edge_image.put_start_and_end_on(
                0.5 * edge_weight_scale * edge_weight * LEFT,
                0.5 * edge_weight_scale * edge_weight * RIGHT
            )
            out_edge.append(edge_image)

            # add vertices and labels
            for v, direction in [(v1, LEFT), (v2, RIGHT)]:

                # add vertex
                if v in g.vertex_config:
                    vertex_image = g.vertex_config[v]
                else:
                    vertex_image = g.vertex_default.copy()
                vertex_image.shift(
                    0.5 * direction * edge_weight_scale * edge_weight
                )

                # add label
                if v in g.label_config:
                    label_attr = g.label_default.copy()
                    label_attr.update(g.label_config[v])
                    label_image = g.label_type(text=v, **label_attr)
                else:
                    label_image = g.label_type(text=v, **g.label_default)

                label_image.move_to(FUTURA_CENTERING_POS[v]) \
                    .scale(g.vertex_and_label_scale, about_point=ORIGIN) \
                    .shift(0.5 * direction * edge_weight_scale * edge_weight)

                out_edge.append(vertex_image)
                out_edge.append(label_image)

            # add weight
            weight_image = Text(
                str(edge_weight),
                font=g.label_default["font"]
            )
            weight_image.move_to(edge_image).shift(0.4 * UP)
            out_edge.append(weight_image)

            out.append(out_edge)

        return out

