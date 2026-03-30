from manim import *
from sick_manim.utils import render_scene

class ACubeAppears(ThreeDScene):

    def construct(self):
        # Create a square
        square = Square(side_length=2)
        self.play(Create(square), run_time=1.25)
        self.wait(0.5)

        # Fill in the square, rotate, and move aside
        self.play(square.animate.set_fill(DARK_GRAY,opacity=0.2), run_time=0.5)
        self.play(square.animate.rotate(angle=PI/4), run_time=0.75)
        self.play(square.animate.to_edge(LEFT).shift(RIGHT), run_time = 0.5)

        # Add lidar
        lidar = Circle(radius=0.1,color=GRAY_A).move_to(RIGHT)
        self.play(Create(lidar), run_time=0.75)
        self.play(lidar.animate.set_fill(DARK_GRAY,opacity=0.2), run_time=0.5)
        self.play(lidar.animate.move_to(3*RIGHT))
        self.wait(0.5)



        # def face_camera(dot: Dot):
        #     center = dot.get_center()
        #     xv = dot.point_at_angle(0) - center
        #     xv = xv / np.linalg.norm(xv)
        #     yv = dot.point_at_angle(PI/2) - center
        #     yv = yv / np.linalg.norm(yv)
        #     zv = np.cross(xv,yv)
        #     camera_direction = self.camera.frame_center - center
        #     camera_direction = camera_direction/np.linalg.norm(camera_direction)

        #     delta_angle = np.acos(np.dot(zv,camera_direction))
        #     if not delta_angle < 0.1:
        #         delta_axis = np.cross(zv,camera_direction)
        #         dot.rotate(delta_angle,delta_axis, about_point=center)








        # Shoot a beam
        
        num_beams=20
        start_angle = 3*PI/4
        end_angle = 5*PI/4

        delta_angle = end_angle-start_angle
        beam_angles = [start_angle + delta_angle*k/num_beams for k in range(num_beams)]

        animlist = []
        dots = []
        beams = []
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
                dot = Dot(start_point, color=RED, fill_opacity=0.5)  
                dots.append(dot)              
            else:
                finish_point = start_point + 15*direction
                dot = Dot(start_point, radius=0)

            start_dot = Dot(start_point,radius=0)
            
            beam = always_redraw(lambda s = start_dot, e = dot: Line(s.get_center(), e.get_center(), color=RED, stroke_opacity=0.5))
            self.add(beam)
            beams.append(beam)

            animlist.append(Succession(
                Create(dot, run_time=0.01),
                AnimationGroup(dot.animate.move_to(finish_point), run_time=0.05),
                AnimationGroup(
                    start_dot.animate.move_to(finish_point),
                    ApplyMethod(dot.set_opacity,0.9, run_time=0.1),
                    lag_ratio=0.0,
                    run_time=0.1
                ),
            ))


        animate_beams = LaggedStart(*animlist,lag_ratio=0.25)
        self.play(animate_beams)
        for beam in beams:
            self.remove(beam)







        # Go to 3D
        # plane = NumberPlane(x_range=[-20,20,1],y_range=[-20,20,1]).shift(DOWN)

        cube = Cube(side_length=2).set_fill(DARK_GRAY,opacity=1).rotate(angle=PI/4).to_edge(LEFT).shift(RIGHT).set_stroke(WHITE,width=1)
        lidar2 = Cylinder(radius=0.1,height=0.1,resolution=(10,10)).set_fill(DARK_GRAY,opacity=1).move_to(3*RIGHT).set_stroke(WHITE,width=1)

        self.play(
            FadeOut(square),
            FadeOut(lidar),
        )
        self.play(
            FadeIn(cube),
            FadeIn(lidar2),
            # Create(plane),
        run_time=2)

        # self.play(
        #     Transform(square,cube),
        #     Transform(lidar,lidar2)
        # )
        # self.remove(lidar)
        # self.remove(square)

        # self.play(Uncreate(square))
        # self.play(Create(cube),run_time=2)
        # self.add(cube)
        # self.remove(square)

        # self.play(Uncreate(lidar))
        # self.play(Create(lidar2),run_time=2)
        # self.add(lidar2)
        # self.remove(lidar)

        self.move_camera(phi = 90*DEGREES,theta = -90*DEGREES)
        for dot in dots:
            dot.rotate(self.camera.get_phi(),RIGHT,about_point=dot.get_center())





        # Rotate the lidar
        arrow = Arrow(start=lidar2.get_center()+lidar2.height/2*OUT,end=lidar2.get_center()+2*OUT).rotate(PI/2,OUT)
        self.play(Create(arrow))

        lidar_plane_angle = PI/32
        lidar.rotate(lidar_plane_angle,UP)
        self.play(
            Rotate(lidar2,lidar_plane_angle,UP),
            Rotate(arrow,lidar_plane_angle,UP,about_point=lidar2.get_center())
        )

        self.play(Uncreate(arrow))


        # Move camera again
        self.move_camera(phi = 60*DEGREES,theta = -20*DEGREES)
        for dot in dots:
            dot.rotate(-30*DEGREES,RIGHT,about_point=dot.get_center()).rotate(self.camera.get_theta()+PI/2,OUT,about_point=dot.get_center())


        # And play the beams again
        cube_dist = np.linalg.norm(cube.get_center()-lidar.get_center())
        check_height = cube_dist*np.tan(lidar_plane_angle)
        check_square = Square(side_length=2).move_to(cube.get_center()).rotate(PI/4,OUT).rotate(lidar_plane_angle,UP).shift(OUT*check_height).set_stroke(RED)


        animlist = []
        dots2 = []
        beams2 = []
        for theta in beam_angles:

            start_point = lidar.point_at_angle(angle=theta)
            direction = start_point - lidar.get_center()
            direction = direction/np.linalg.norm(direction)

            width=0.05
            length=10
            ray = Rectangle(height=width,width=length).rotate(angle=theta,axis=OUT,about_point=lidar.get_center()).move_to(start_point+direction*length/2).rotate(angle=lidar_plane_angle,axis=UP)
            hits = Intersection(ray,check_square,color=GREEN).rotate(angle=lidar_plane_angle,axis=UP).shift(OUT*check_height)
            if not len(hits.get_all_points()) == 0:
                finish_point = hits.get_boundary_point(direction=lidar.get_center()-hits.get_center())
                dot = Dot(start_point, color=RED, fill_opacity=0.5).rotate(self.camera.get_phi(),RIGHT,about_point=dot.get_center()).rotate(self.camera.get_theta()+PI/2,OUT,about_point=dot.get_center())   
                dots2.append(dot)             
            else:
                finish_point = start_point + 15*direction
                dot = Dot(start_point, radius=0)




            start_dot = Dot(start_point,radius=0)
            
            beam = always_redraw(lambda s = start_dot, e = dot: Line(s.get_center(), e.get_center(), color=RED, stroke_opacity=0.5))
            self.add(beam)
            beams2.append(beam)

            animlist.append(Succession(
                Create(dot, run_time=0.01),
                AnimationGroup(dot.animate.move_to(finish_point), run_time=0.05),
                AnimationGroup(
                    start_dot.animate.move_to(finish_point),
                    ApplyMethod(dot.set_opacity,0.9, run_time=0.1),
                    lag_ratio=0.0,
                    run_time=0.1
                ),
            ))


        animate_beams = LaggedStart(*animlist,lag_ratio=0.25)
        self.play(animate_beams)
        for beam in beams2:
            self.remove(beam)




        # Fade out object
        self.play(
            FadeOut(cube),
        run_time = 2)


        # Add in image
        img_point = 0.5*RIGHT
        img_values = np.uint8([
                [100, 100, 30, 200, 200],
                [255, 150, 170, 33, 120],
                [150, 20, 50, 170, 100]]
            )
        image = ImageMobject(img_values).rotate(PI/2,OUT).rotate(PI/2,UP).move_to(img_point).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image.height = 1
        image.width = 1.7

        self.add(image)


        def point_at_x(p1, p2, x_target):
            if abs(p2[0] - p1[0]) < 1e-8:
                raise ValueError("Line is vertical in x; x is constant")

            t = (x_target - p1[0]) / (p2[0] - p1[0])
            return p1 + t * (p2 - p1)
        

        all_dots = [*dots, *dots2]
        animlist = []
        animlist2 = []
        for idx,dot in enumerate(all_dots):
            value = img_values.flatten()[idx]
            color = ManimColor.from_rgb((value,value,value))
            img_intersection = point_at_x(lidar.get_center(),dot.get_center(),img_point[0])
            beam1 = Line(lidar.get_center(),img_intersection,color=BLUE)
            beam2 = Line(img_intersection,dot.get_center(),color=color).set_z_index(-100)
            
            anim = Succession(
                Create(beam1,run_time=0.5),
                Create(beam2,run_time=0.5),
                AnimationGroup(dot.animate.set_fill(color),run_time=0.2),
            )
            animlist.append(anim)

            anim2 = AnimationGroup(
                FadeOut(beam1,run_time=0.5),
                FadeOut(beam2,run_time=0.5),
            )
            animlist2.append(anim2)

        self.play(AnimationGroup(*animlist,lag_ratio=0.0))
        self.play(AnimationGroup(*animlist2,lag_ratio=0.0))






        # Sit
        self.wait(1)


if __name__ == "__main__":
    render_scene(ACubeAppears)