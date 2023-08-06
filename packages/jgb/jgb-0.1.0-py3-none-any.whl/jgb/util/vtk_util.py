#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import os

import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util.numpy_support import numpy_to_vtk


class TransformBuilder:
    def __init__(self):
        self._trans = vtk.vtkTransform()

    def translate(self, x, y, z):
        self._trans.Translate((x, y, z))
        return self

    def rotate_x(self, degree):
        self._trans.RotateX(degree)
        return self

    def rotate_y(self, degree):
        self._trans.RotateY(degree)
        return self

    def rotate_z(self, degree):
        self._trans.RotateZ(degree)
        return self

    def scale(self, x, y, z):
        self._trans.Scale(x, y, z)
        return self

    def build(self):
        return self._trans


def io_read_poly_data(file_name):
    path, extension = os.path.splitext(file_name)
    extension = extension.lower()
    if extension == ".ply":
        reader = vtk.vtkPLYReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".vtp":
        reader = vtk.vtkXMLpoly_dataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".obj":
        reader = vtk.vtkOBJReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".stl":
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".vtk":
        reader = vtk.vtkpoly_dataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".g":
        reader = vtk.vtkBYUReader()
        reader.SetGeometryFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    else:
        # Return a None if the extension is unknown.
        poly_data = None
    return poly_data


def op_transform(poly_data, trans):
    trans_filter = vtk.vtkTransformPolyDataFilter()
    trans_filter.SetInputData(poly_data)
    trans_filter.SetTransform(trans)
    trans_filter.Update()
    result = trans_filter.GetOutput()
    return result


def io_write_stl(poly_data, file_path):
    stl_writer = vtk.vtkSTLWriter()
    stl_writer.SetFileTypeToBinary()
    stl_writer.SetFileName(file_path)
    stl_writer.SetFileTypeToASCII()
    stl_writer.SetInputData(poly_data)
    stl_writer.Write()


def io_write_ply(poly_data, file_path):
    ply_writer = vtk.vtkPLYWriter()
    ply_writer.SetFileTypeToBinary()
    ply_writer.SetFileName(file_path)
    ply_writer.SetInputData(poly_data)
    ply_writer.Write()


def op_smooth_polydata(poly_data, iterations=30, relaxation_factor=0.1):
    smooth = vtk.vtkSmoothPolyDataFilter()

    # smooth.SetInputConnection(delaunay.GetOutputPort())
    smooth.SetInputData(poly_data)

    smooth.SetNumberOfIterations(iterations)
    smooth.SetRelaxationFactor(relaxation_factor)
    smooth.FeatureEdgeSmoothingOff()
    smooth.BoundarySmoothingOff()
    smooth.Update()

    return smooth.GetOutput()


def op_dsa_points(vtk_obj):
    """
    返回 points

    没有考虑点集构建的结构比如 ``op_cutter`` 返回的 strip 中多个 polyline
    """
    return dsa.WrapDataObject(vtk_obj).Points


def op_cutter(point, normal, polydata):
    plane = vtk.vtkPlane()
    plane.SetOrigin(*point)
    plane.SetNormal(normal[0], normal[1], normal[2])

    cutter = vtk.vtkCutter()
    cutter.SetInputData(polydata)
    cutter.SetCutFunction(plane)

    strip = vtk.vtkStripper()
    strip.SetInputConnection(cutter.GetOutputPort())
    strip.Update()

    return cutter, strip.GetOutput()


def op_mass_properties(poly_data):
    mass_properties = vtk.vtkMassProperties()
    mass_properties.SetInputData(poly_data)
    mass_properties.Update()
    return mass_properties


def xyz_point_polydata(pts):
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()

    for i in range(len(pts)):
        p = pts[i, :]
        idx = points.InsertNextPoint(p)
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(idx)

    point = vtk.vtkPolyData()
    point.SetPoints(points)
    point.SetVerts(vertices)
    return point


def xyz_point_spheres(centers, radius, res=8):
    src = vtk.vtkSphereSource()
    src.SetRadius(radius)
    res_t, res_phi = 2 * res, res

    src.SetThetaResolution(res_t)
    src.SetPhiResolution(res_phi)
    src.Update()

    psrc = vtk.vtkPointSource()
    psrc.SetNumberOfPoints(len(centers))
    psrc.Update()
    pd = psrc.GetOutput()
    vpts = pd.GetPoints()

    glyph = vtk.vtkGlyph3D()
    glyph.SetSourceConnection(src.GetOutputPort())

    vpts.SetData(numpy_to_vtk(np.ascontiguousarray(centers), deep=True))

    glyph.SetInputData(pd)
    glyph.Update()
    return glyph.GetOutput()


def cvt_matrix4x4_to_numpy(matrix):
    m = np.ones((4, 4))
    for i in range(4):
        for j in range(4):
            m[i, j] = matrix.GetElement(i, j)
    return m


def cvt_numpy_to_matrix4x4(mat):
    matrix = vtk.vtkMatrix4x4()
    for i in range(4):
        for j in range(4):
            matrix.SetElement(i, j, mat[i, j])
    return matrix


def zky_stl_to_pcd_trans(stl_poly_data):
    transform = vtk.vtkTransform()
    transform.Scale(1000, 1000, 1000)
    # transform.RotateY(45)
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputData(stl_poly_data)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    return transform_filter.GetOutput()
