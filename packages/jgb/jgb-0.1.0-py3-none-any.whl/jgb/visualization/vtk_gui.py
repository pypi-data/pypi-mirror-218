#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import vtk


class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.middleButtonReleaseEvent)

    def middleButtonPressEvent(self, obj, event):
        print("Middle Button pressed")
        self.OnMiddleButtonDown()
        return

    def middleButtonReleaseEvent(self, obj, event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
        return


def create_window():
    ren = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(ren)
    render_window.SetSize((800, 800))

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(MyInteractorStyle())
    interactor.SetRenderWindow(render_window)

    return ren, interactor, render_window


def window_start(interactor, render_window):
    interactor.Initialize()
    render_window.Render()
    interactor.Start()


def close_window(ren):
    render_window = ren.GetRenderWindow()
    render_window.Finalize()
    ren.TerminateApp()


def actor_from_polydata(poly_data, lw=None, color=None, opacity=None):
    mapper = vtk.vtkPolyDataMapper()

    if isinstance(poly_data, vtk.vtkAlgorithm):
        mapper.SetInputConnection(poly_data.GetOutputPort())
    else:
        mapper.SetInputData(poly_data)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    if color is not None:
        actor.GetProperty().SetColor(color[0], color[1], color[2])
    if lw is not None:
        actor.GetProperty().SetLineWidth(lw)
    if opacity is not None:
        actor.GetProperty().SetOpacity(opacity)
    return actor


def actor_sphere(center, radius, color=(1.0, 0.0, 0.0)):
    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetCenter(*center)
    sphere_source.SetRadius(radius)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere_source.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    return actor


def actor_rgb_axes(axes_length=0.2):
    # Red, Green, Blue分别对应X,Y,Z三条轴：
    axes = vtk.vtkAxesActor()
    axes.SetPosition(0, 0, 0)
    axes.SetTotalLength(axes_length, axes_length, axes_length)
    axes.SetShaftType(0)
    axes.SetAxisLabels(0)
    axes.SetCylinderRadius(0.02)
    return axes


def add_xyz_pts(render: vtk.vtkRenderer, pts, color=None):
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(pts)
    else:
        mapper.SetInputData(pts)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(1)

    if color is not None:
        actor.GetProperty().SetColor(color[0], color[1], color[2])
    render.AddActor(actor)


def add_actor_cube_axes(render: vtk.vtkRenderer, poly_data):
    cube_axes = vtk.vtkCubeAxesActor2D()
    # cube_axes.SetInputConnection(input_conn)
    if isinstance(poly_data, vtk.vtkAlgorithm):
        cube_axes.SetInputConnection(poly_data.GetOutputPort())
    else:
        cube_axes.SetInputData(poly_data)

    cube_axes.SetCamera(render.GetActiveCamera())
    cube_axes.SetLabelFormat("%1.1g")

    render.AddViewProp(cube_axes)


def camera_to_actor(camera):
    colors = vtk.vtkNamedColors()

    planes_array = [0] * 24
    camera.GetFrustumPlanes(1.0, planes_array)

    planes = vtk.vtkPlanes()
    planes.SetFrustumPlanes(planes_array)

    frustum_source = vtk.vtkFrustumSource()
    frustum_source.ShowLinesOff()
    frustum_source.SetPlanes(planes)

    shrink = vtk.vtkShrinkPolyData()
    shrink.SetInputConnection(frustum_source.GetOutputPort())
    shrink.SetShrinkFactor(0.8)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(shrink.GetOutputPort())

    back = vtk.vtkProperty()
    back.SetColor(colors.GetColor3d("Tomato"))

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetColor(colors.GetColor3d("Banana"))
    actor.SetBackfaceProperty(back)
    actor.GetProperty().SetOpacity(0.99)
    return actor


def vtk_show(poly_data):
    ren, interactor, render_window = create_window()
    ren.AddActor(actor_from_polydata(poly_data))
    ren.AddActor(actor_rgb_axes())
    window_start(interactor, render_window)


def zky_plane():
    plane = vtk.vtkPlaneSource()
    plane.SetNormal(0, 1, 0)
    plane.SetPoint1(400, 0, 400)
    plane.SetPoint2(-400, 0, 400)
    plane.SetXResolution(50)
    plane.SetYResolution(50)
    plane.SetCenter(0, 0, 0)
    return plane
