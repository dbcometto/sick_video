from manim import *
from sick_manim.utils import render_scene

class ASquareAppears(ThreeDScene):

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
        self.play(lidar.animate.move_to(3*RIGHT))
        self.wait(0.5)

        # Shoot a beam
        
        num_beams=20
        start_angle = 3*PI/4
        end_angle = 5*PI/4

        delta_angle = end_angle-start_angle
        beam_angles = [start_angle + delta_angle*k/num_beams for k in range(num_beams)]

        animlist = []
        for theta in beam_angles:

            start_point = lidar.point_at_angle(angle=theta)
            direction = start_point - lidar.get_center()
            direction = direction/np.linalg.norm(direction)

            width=0.05
            length=10
            ray = Rectangle(height=width,width=length).rotate(angle=theta,about_point=lidar.get_center()).move_to(start_point+direction*length/2)
            hits = Intersection(ray,square,color=GREEN)
            if not len(hits.get_all_points()) == 0:
                finish_point = hits.get_boundary_point(direction=lidar.get_center()-hits.get_center())
            else:
                finish_point = start_point + 15*direction

            # self.add(ray)
            # self.add(hits)
            # self.wait(1)
            # hitpt = hits.get_all_points()


            start_dot = Dot(start_point,radius=0)
            dot = Dot(start_point, color=RED, fill_opacity=0.5)
            
            beam = always_redraw(lambda s = start_dot, e = dot: Line(s.get_center(), e.get_center(), color=RED, stroke_opacity=0.5))
            self.add(beam)

        
            # print(id(dot))
            # dot.generate_target()
            # dot.target.move_to(finish_point)
            # dot.target.set_opacity(0.9)

            animlist.append(Succession(
                Create(dot, run_time=0.01),
                # MoveToTarget(dot, run_time=0.2),
                AnimationGroup(dot.animate.move_to(finish_point), run_time=0.05),
                # dot.animate.move_to(finish_point).set_opacity(0.9),
                # dot.animate.set_opacity(0.9),
                # start_dot.animate.move_to(finish_point),
                AnimationGroup(
                    start_dot.animate.move_to(finish_point),
                    ApplyMethod(dot.set_opacity,0.9, run_time=0.1),
                    lag_ratio=0.0,
                    run_time=0.1
                ),
            ))
            # animlist.append(dot.animate.set_opacity(0.9))

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

        animate_beams = LaggedStart(*animlist,lag_ratio=0.25)
        self.play(animate_beams)






        # Fade out scene
        self.play(
            FadeOut(square), 
            FadeOut(lidar),
        run_time = 2)






        # Sit
        self.wait(1)


if __name__ == "__main__":
    render_scene(ASquareAppears)