from manim import *
from tools.basic_graph import BasicGraph
from tools.show_positional_values_2D import *

def grow_from_below(mobject):
    return mobject.shift(8*UP)

# def push_to_top(moject):
#     return moject.shift()

class KruskalsIntro(Scene):

    def construct(self):
        text = Tex("Kruskal's Algorithm also called "
                   "the greedy algorithm", font="futura"
                   )
        text2 = Tex("it is used to find the Minimum Spanning Tree.",
                    font="futura") \
            .next_to(text, DOWN)
        self.add(
            text,
            text2)


class Kruskals1(Scene):

    def construct(self):
        vertices = {"A": (-8, 2), "B": [-3, 5], "C": [0, 0],
                    "D": [-3, -2], "E": [1, -2], "F": [3, 2]}

        edges = (("A", "B"), ("A", "D"), ("B", "C"), ("B", "F"), ("C", "D"),
                 ("C", "F"), ("E", "F"), ("D", "E"))

        weights = {("A", "B"): [5, (-0.35, 0.6)], ("A", "D"): [6, (-0.5, -0.5)],
                   ("B", "C"): [6, (-0.35, -0.6)], ("B", "F"): [7, (0.5, 0.5)],
                   ("C", "D"): [3, (-0.5, 0.5)], ("C", "F"): [3, (-0.5, 0.5)],
                   ("E", "F"): [5, (0.5, 0)], ("D", "E"): [4, (0, -0.5)]}

        g1 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weights

        ).scale(0.5, about_point=ORIGIN).save_state()

        self.play(ShowCreation(g1))
        # self.add(g1)


class KruskalsMSTCreation(Scene):

    def construct(self):
        vertices = {"A": [-4, 0], "B": [0, -3], "C": [0, 0], "D": [3, 4],
                    "E": [7, 0], "F": (6, -3), "G": (10, 2), "H": [11, 0]}
        edges = [("A", "B"), ("A", "C"), ("A", "D"),
                 ("B", "C"), ("B", "F"),
                 ("C", "D"), ("C", "E"),
                 ("D", "E"),
                 ("E", "F"),
                 ("E", "G"),
                 ("E", "H"),
                 ("G", "H")]

        weight = {("A", "B"): [5, (-0.35, -0.35)], ("A", "C"): [4, (0.35, 0.5)],
                  ("A", "D"): [8, (-0.35, 0.35)], ("B", "C"): [3, (0.35, 0)],
                  ("B", "F"): [6, (0, 0.5)], ("C", "D"): [5, (0.35, -0.35)],
                  ("C", "E"): [7, (0, 0.5)], ("D", "E"): [6, (0.35, 0.35)],
                  ("E", "F"): [3, (0.35, 0)], ("E", "G"): [3, (0, 0.5)],
                  ("E", "H"): [4, (0, -0.5)], ("G", "H"): [1, (0.35, 0.25)]}

        g1 = BasicGraph(
            vertices=vertices.copy(),
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight
        ).save_state().scale(0.7, about_point=ORIGIN).shift(2.2 * LEFT)

        edges = [("A", "C"), ("B", "C"), ("C", "D"), ("B", "F"), ("E", "F"),
                 ("E", "G"), ("G", "H")]

        g2 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight

        ).save_state().scale(0.7, about_point=ORIGIN).shift(2.2 * LEFT)

        self.play(
            ShowCreation(g1)
        )
        BasicGraph.wait(self, 3)
        self.play(ShowCreation(g2))
        self.play(Uncreate(g1, run_time=7))


class KruskalsExample1(Scene):

    def construct(self):

        # grid = ImageMobject('tools/grid.png')
        # self.add(grid)

        # these are the defined vertices edges and weights of the graph
        vertices = {"A": (-8, 2), "B": [-3, 5], "C": [0, 0],
                    "D": [-3, -2], "E": [1, -2], "F": [3, 2]}

        edges = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "F"), ("C", "D"),
                 ("C", "F"), ("E", "F"), ("D", "E")]

        weight = {("A", "B"): [5, (-0.35, 0.6)], ("A", "D"): [6, (-0.5, -0.5)],
                  ("B", "C"): [6, (-0.35, -0.6)], ("B", "F"): [7, (0.5, 0.5)],
                  ("C", "D"): [3, (-0.5, 0.5)], ("C", "F"): [3, (-0.5, 0.5)],
                  ("E", "F"): [5, (0.5, 0)], ("D", "E"): [4, (0, -0.5)]}

        # Creates the first graph
        g = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight

        ).scale(0.5, about_point=ORIGIN).shift(RIGHT).save_state()

        # Displays first graph in the centre
        self.play(ShowCreation(g))
        BasicGraph.wait(self, 4)
        # Positions to left and down
        g.generate_target()
        g.target.shift(2.5 * LEFT + 1 * DOWN)
        BasicGraph.wait(self, 2)
        # Moves to the target locations
        self.play(MoveToTarget(g))
        BasicGraph.wait(self, 4)

        # This block is used to decompose the graph and make a list of mobjects
        # in order of:
        # [weight (number), edge, vertex1, label1, vertex2, label2, weight]
        # which is then used to display a column of edges and vertices
        # on the side of the graph or in any position on the screen.

        # uses the decompose to make a list of all the mobjectss
        g1_elements = BasicGraph.decompose_graph(g, edge_weight_scale=0.7)
        # Makes a list of all the mobjects of the edges in
        # ascending order based on the weight number
        ascending_list = sorted(g1_elements, key=lambda x: (x[0]))

        # deletes the first element to make it a list with only mobjects and no
        # integers to compute into a scene
        for y in g1_elements:
            del y[0]

        # This block makes a list of all the mobjects that are not ordered
        # making each next element eppear below the previous one
        list_of_scenes = []
        # iterating over the list of edges
        for test in range(len(edges)):
            # Creating a VGroup of all the elements on the g1_elements
            # list which contains the edge elements
            scenes = VGroup(*g1_elements[test])
            # Checks and positions the first edge to appear on screen
            if not list_of_scenes:
                final_scene = scenes.scale(0.45).move_to(np.array([4, -5, 0]))
            # Positions each succeeding edge one below each other
            else:
                final_scene = scenes.scale(0.45) \
                    .next_to(list_of_scenes[-1], 1.5 * DOWN)
            # Adds each of the edges with the right scaling
            # and positioning to a new list
            list_of_scenes.append(final_scene)

        # Makes a VGroup of all the elements in the list to render when called
        group_scenes = VGroup(*list_of_scenes)

        # Creates graph 2 which is the same as graph 1 but with dashed lines
        # for demonstration purposes
        g1 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine()

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        # Adds graph 2 and removes graph 1 whilst simultaneously adding
        # the list of edges on the right side
        self.add(g1)
        # self.play(Uncreate(g), Write(group_scenes))
        self.play(Uncreate(g), ApplyFunction(grow_from_below, group_scenes))
        BasicGraph.wait(self, 2)
        self.play(ApplyFunction(grow_from_below, group_scenes))
        # self.play(FadeOut(group_scenes))
        # BasicGraph.wait(self, 2)


        # Creates the same list of MObject as list_of_scenes but for
        # the sorted order of edges based on weight

        list_of_scenes2 = []
        for test in range(len(edges)):
            scenes = VGroup(*ascending_list[test])
            if not list_of_scenes2:
                final_scene = scenes.move_to(np.array([4, -5, 0]))
            else:
                final_scene = scenes \
                    .next_to(list_of_scenes2[-1], 1.5 * DOWN)

            list_of_scenes2.append(final_scene)
        # Like group_scenes makes a VGroup of all MObjects
        group_scenes2 = VGroup(*list_of_scenes2)

        # Transforms the unsorted list into the sorted list
        # in a clockwise manner
        # self.play(ClockwiseTransform(group_scenes, group_scenes2))

        self.play(ApplyFunction(grow_from_below, group_scenes2))
        # BasicGraph.wait(self, 5)

        g2 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            edge_config={("C", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10)
                         }

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        coloured_scene_g3 = list_of_scenes2[0][0].set_color(GREEN)
        coloured_scene1_g3 = list_of_scenes2[0][2].set_color(GREEN)
        coloured_scene2_g3 = list_of_scenes2[0][4].set_color(GREEN)

        self.play(Write(coloured_scene_g3), Write(coloured_scene1_g3),
                  Write(coloured_scene2_g3))

        # Adds the coloured list onto the scene after time x
        BasicGraph.wait(self, 2)
        self.play(FadeIn(g2))
        self.remove(g1)
        BasicGraph.wait(self, 2)

        g3 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            edge_config={("C", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("C", "F"): Line().set_color(GREEN) \
                .set_stroke(width=10)
                         }

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        coloured_scene_g4 = list_of_scenes2[1][0].set_color(GREEN)
        coloured_scene1_g4 = list_of_scenes2[1][2].set_color(GREEN)
        coloured_scene2_g4 = list_of_scenes2[1][4].set_color(GREEN)

        self.play(Write(coloured_scene_g4), Write(coloured_scene1_g4),
                  Write(coloured_scene2_g4))
        BasicGraph.wait(self, 2)
        self.play(FadeIn(g3))
        self.remove(g2)
        BasicGraph.wait(self, 2)

        g4 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            edge_config={("C", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("C", "F"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("D", "E"): Line().set_color(GREEN) \
                .set_stroke(width=10)}

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        coloured_scene_g5 = list_of_scenes2[2][0].set_color(GREEN)
        coloured_scene1_g5 = list_of_scenes2[2][2].set_color(GREEN)
        coloured_scene2_g5 = list_of_scenes2[2][4].set_color(GREEN)

        self.play(Write(coloured_scene_g5), Write(coloured_scene1_g5),
                  Write(coloured_scene2_g5))
        BasicGraph.wait(self, 2)
        self.play(FadeIn(g4))
        self.remove(g3)
        BasicGraph.wait(self, 2)

        g5 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            edge_config={("C", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("C", "F"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("D", "E"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("A", "B"): Line().set_color(GREEN) \
                .set_stroke(width=10)
                         }

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        coloured_scene_g6 = list_of_scenes2[3][0].set_color(GREEN)
        coloured_scene1_g6 = list_of_scenes2[3][2].set_color(GREEN)
        coloured_scene2_g6 = list_of_scenes2[3][4].set_color(GREEN)

        self.play(Write(coloured_scene_g6), Write(coloured_scene1_g6),
                  Write(coloured_scene2_g6))
        BasicGraph.wait(self, 2)
        self.play(FadeIn(g5))
        self.remove(g4)
        BasicGraph.wait(self, 2)

        g6 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            edge_config={("C", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("C", "F"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("D", "E"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("A", "B"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         }

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        coloured_scene_g7 = list_of_scenes2[4][0].set_color(RED)
        coloured_scene1_g7 = list_of_scenes2[4][2].set_color(RED)
        coloured_scene2_g7 = list_of_scenes2[4][4].set_color(RED)

        self.play(Write(coloured_scene_g7), Write(coloured_scene1_g7),
                  Write(coloured_scene2_g7))
        BasicGraph.wait(self, 2)
        self.play(FadeIn(g6))
        self.remove(g5)
        BasicGraph.wait(self, 2)

        g7 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            edge_config={("C", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("C", "F"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("D", "E"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("A", "B"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("A", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10)

                         }

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        coloured_scene_g8 = list_of_scenes2[5][0].set_color(GREEN)
        coloured_scene1_g8 = list_of_scenes2[5][2].set_color(GREEN)
        coloured_scene2_g8 = list_of_scenes2[5][4].set_color(GREEN)

        self.play(Write(coloured_scene_g8), Write(coloured_scene1_g8),
                  Write(coloured_scene2_g8))
        BasicGraph.wait(self, 2)
        self.play(FadeIn(g7))
        self.remove(g6)
        BasicGraph.wait(self, 2)

        coloured_scene_g9 = list_of_scenes2[6][0].set_color(RED)
        coloured_scene2_g9 = list_of_scenes2[6][2].set_color(RED)
        coloured_scene3_g9 = list_of_scenes2[6][4].set_color(RED)

        self.play(Write(coloured_scene_g9), Write(coloured_scene2_g9),
                  Write(coloured_scene3_g9))
        BasicGraph.wait(self, 2)

        coloured_scene4_g9 = list_of_scenes2[7][0].set_color(RED)
        coloured_scene5_g9 = list_of_scenes2[7][2].set_color(RED)
        coloured_scene6_g9 = list_of_scenes2[7][4].set_color(RED)

        self.play(Write(coloured_scene4_g9), Write(coloured_scene5_g9),
                  Write(coloured_scene6_g9))

        BasicGraph.wait(self, 2)
        # self.add(g2)

        weight1 = {("A", "B"): [5, (-0.35, 0.6)], ("A", "D"): [6, (-0.5, -0.5)],
                   ("C", "D"): [3, (-0.5, 0.5)], ("C", "F"): [3, (-0.5, 0.5)],
                   ("D", "E"): [4, (0, -0.5)]}

        # Makes a graph which only connects the nodes of the MST this
        g8 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight1,
            edge_default=Line(),
            edge_config={("C", "D"): Line().set_color(GREEN). \
                set_stroke(width=10),
                         ("C", "F"): Line().set_color(GREEN). \
                set_stroke(width=10),
                         ("D", "E"): Line().set_color(GREEN). \
                set_stroke(width=10),
                         ("A", "B"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("A", "D"): Line().set_color(GREEN) \
                .set_stroke(width=10),
                         ("B", "F"): Line().set_color(BLACK) \
                .set_stroke(width=10),
                         ("B", "C"): Line().set_color(BLACK) \
                .set_stroke(width=10),
                         ("E", "F"): Line().set_color(BLACK) \
                .set_stroke(width=10)
                         }

        ).scale(0.5, about_point=ORIGIN).shift(1.5 * LEFT + 1 * DOWN) \
            .save_state()

        self.play(Write(g8), run_time=0.5)
        self.play(FadeOut(g7), run_time=0.5)
        BasicGraph.wait(self, 2)

        g8.generate_target()
        g8.target.shift(2.5 * RIGHT + 0.5 * UP)
        # Moves to the target locations
        self.play(Uncreate(group_scenes2))
        BasicGraph.wait(self, 2)
        self.play(MoveToTarget(g8))
        BasicGraph.wait(self, 4)


class KruskalsExample2(Scene):
    def construct(self):
        vertices = {"A": [-4, 0], "B": [0, -3], "C": [0, 0], "D": [3, 4],
                    "E": [7, 0], "F": (6, -3), "G": (10, 2), "H": [11, 0]}
        edges = [("A", "B"), ("A", "C"), ("A", "D"),
                 ("B", "C"), ("B", "F"),
                 ("C", "D"), ("C", "E"),
                 ("D", "E"),
                 ("E", "F"),
                 ("E", "G"),
                 ("E", "H"),
                 ("G", "H")]

        weight = {("A", "B"): [5, (-0.35, -0.35)], ("A", "C"): [4, (0.35, 0.5)],
                  ("A", "D"): [8, (-0.35, 0.35)], ("B", "C"): [3, (0.35, 0)],
                  ("B", "F"): [6, (0, 0.5)], ("C", "D"): [5, (0.35, -0.35)],
                  ("C", "E"): [7, (0, 0.5)], ("D", "E"): [6, (0.35, 0.35)],
                  ("E", "F"): [3, (0.35, 0)], ("E", "G"): [3, (0, 0.5)],
                  ("E", "H"): [4, (0, -0.5)], ("G", "H"): [1, (0.35, 0.25)]}

        g = BasicGraph(
            vertices=vertices.copy(),
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight
        ).save_state().scale(0.7, about_point=ORIGIN).shift(2.2 * LEFT)

        self.play(ShowCreation(g))
        BasicGraph.wait(self, 4)
        g.generate_target()
        g.target.shift(3.8 * LEFT + 2 * DOWN).scale(0.75, about_point=ORIGIN)
        BasicGraph.wait(self, 2)
        self.play(MoveToTarget(g))

        g1_elements = BasicGraph.decompose_graph(g, 1.5)
        ascending_list = sorted(g1_elements, key=lambda x: (x[0]))
        # integers to compute into a scene
        for y in g1_elements:
            del y[0]
        list_of_scenes = []
        for test in range(len(edges)):
            scenes = VGroup(*g1_elements[test])
            if not list_of_scenes:
                final_scene = scenes.scale(0.35).move_to(np.array([4, -5, 0]))
            else:
                final_scene = scenes.scale(0.35) \
                    .next_to(list_of_scenes[-1], 0.75 *DOWN)

            list_of_scenes.append(final_scene)
        group_scenes = VGroup(*list_of_scenes)

        g1 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine()

        ).scale(0.5, about_point=ORIGIN).shift(3.8 * LEFT + 2 * DOWN) \
            .save_state()

        self.add(g1)
        self.play(Uncreate(g), ApplyFunction(grow_from_below, group_scenes))
        BasicGraph.wait(self, 2)
        self.play(ApplyFunction(grow_from_below, group_scenes))

        list_of_scenes2 = []
        for test in range(len(edges)):
            scenes = VGroup(*ascending_list[test])
            if not list_of_scenes2:
                final_scene = scenes.scale(1).move_to(np.array([4, -5, 0]))
            else:
                final_scene = scenes.scale(1) \
                    .next_to(list_of_scenes2[-1], 0.75 * DOWN)

            list_of_scenes2.append(final_scene)
        group_scenes2 = VGroup(*list_of_scenes2)

        self.play(ApplyFunction(grow_from_below, group_scenes2))

        g2 = BasicGraph(
            vertices=vertices,
            edges=edges,
            vertex_and_label_scale=1.3,
            weight=weight,
            edge_default=DashedLine(),
            # edge_config={}
        ).scale(0.5, about_point=ORIGIN).shift(3.8 * LEFT + 2 * DOWN) \
            .save_state()

        self.remove(g1)
        self.play(Write(g2))
