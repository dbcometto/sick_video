from manim import *
from sick_manim.utils import render_scene

class ASquareAppears(Scene):

    def construct(self):
        # Create a square
        square = Square(side_length=2)
        self.play(Create(square), run_time=1.25)
        self.wait(0.5)

        # Fill in the square, rotate, and move aside
        self.play(square.animate.set_fill(GRAY,opacity=0.2), run_time=0.5)
        self.play(square.animate.rotate(angle=PI/4), run_time=0.75)
        self.play(square.animate.to_edge(LEFT).shift(RIGHT), run_time = 0.5)

        # Add lidar
        lidar = Circle(radius=0.1,color=GRAY_A).move_to(RIGHT)
        self.play(Create(lidar), run_time=0.75)
        self.play(lidar.animate.set_fill(GRAY,opacity=0.2), run_time=0.5)
        self.wait(0.5)

        # Shoot a beam
        
        animlist = []
        for k in range(3):
            theta = PI-1/10+k/10

            start_point = lidar.point_at_angle(angle=theta)
            direction = start_point - lidar.get_center()
            direction = direction/np.linalg.norm(direction)

            width=0.05
            length=10
            ray = Rectangle(height=width,width=length).rotate(angle=theta,about_point=lidar.get_center()).move_to(start_point+direction*length/2)

            hits = Intersection(ray,square,color=GREEN)


            # self.add(ray)
            # self.add(hits)
            # self.wait(1)
            # hitpt = hits.get_all_points()

            finish_point = hits.get_boundary_point(direction=lidar.get_center()-hits.get_center())

            start_dot = Dot(start_point,radius=0)

            dot = Dot(start_point, color=RED, fill_opacity=0.5)
            
            beam = always_redraw(lambda s = start_dot, e = dot: Line(s.get_center(), e.get_center(), color=RED, stroke_opacity=0.5))
            self.add(beam)

        
            

            animlist.append(AnimationGroup(
                Create(dot),
                dot.animate.move_to(finish_point),
                # dot.animate.set_opacity(0.9),
                start_dot.animate.move_to(finish_point),
                # AnimationGroup(
                #     dot.animate.set_opacity(0.9),
                #     start_dot.animate.move_to(finish_point),
                #     lag_ratio=0
                # ),
            ))
            animlist.append(dot.animate.set_opacity(0.9))

            # self.play(Create(dot), run_time=0.25)
            # self.add(beam)
            # self.play(dot.animate.move_to(finish_point), run_time = 0.25)
            # self.play(
            #     AnimationGroup(
            #         dot.animate.set_opacity(0.9),
            #         start_dot.animate.move_to(finish_point),
            #         lag_ratio=0
            #     ),
            #     run_time=0.1
            # )

        animate_beams = AnimationGroup(*animlist,lag_ratio=0.1)
        self.play(animate_beams,run_time=1)

        # Sit
        self.wait(1)


if __name__ == "__main__":
    render_scene(ASquareAppears)