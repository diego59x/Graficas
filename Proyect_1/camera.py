from gl import *

pi = 3.14

def gourad(render, **kwargs):
    w, v, u = kwargs['bar']
    tx, ty = kwargs['tex_coords']
    nA, nB, nC = kwargs['varyin_normals']

    tcolor = render.current_texture.get_color(tx,ty)

    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]

    intensity = w*iA + v*iB + u*iC
    
    return tcolor * intensity
 
r = Renderer(2500,2500)

r.current_texture = Texture('./Proyect_1/models/cama.bmp')
r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
r.load('./Proyect_1/models/cama.obj',translate=[0.5, -0.4, 0], scale=[1/2, 1/2, 1/2.8], rotate=[89.2,91.1,-4.7])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./Proyect_1/models/jarron.bmp')
r.load('./Proyect_1/models/jarron.obj', translate=[-0.5, 0.1, 0.48], scale=[1/2, 1/2, 1/2], rotate=[89.3,114.8,-4.6])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./Proyect_1/models/ukelele.bmp')
r.load('./Proyect_1/models/Ukulele.obj', translate=[-0.8, -0.12, 0.48], scale=[1, 1, 1], rotate=[90.7,114.8,-4.5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./Proyect_1/models/mesa.bmp')
r.load('./Proyect_1/models/mesa.obj', translate=[-0.7, -0.5, 0], scale=[1/2, 1/2, 1/2], rotate=[89.3,110,-4.7])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./Proyect_1/models/barril.bmp')
r.load('./Proyect_1/models/barril.obj',translate=[-0.4, -0.8, 0], scale=[1/2, 1/2, 1/2], rotate=[89.5,140,-4.7])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.load('./Proyect_1/models/barril.obj',translate=[-0.8, -0.8, 0.42], scale=[1/2, 1/2, 1/2], rotate=[89.5,140,-4.7])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./Proyect_1/models/lampara.bmp')
r.load('./Proyect_1/models/lampara.obj', translate=[0.4, 0.4, 0], scale=[1/2, 1/2, 1/2], rotate=[89.5,91.1,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.load('./Proyect_1/models/lampara.obj', translate=[0, 0.4, 0], scale=[1/2, 1/2, 1/2], rotate=[89.5,91.1,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.load('./Proyect_1/models/lampara.obj', translate=[-0.4, 0.4, 0], scale=[1/2, 1/2, 1/2], rotate=[89.5,91.1,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.load('./Proyect_1/models/lampara.obj', translate=[-0.8, 0.4, 0], scale=[1/2, 1/2, 1/2], rotate=[89.5,91.1,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.load('./Proyect_1/models/lampara.obj', translate=[0.8, 0.4, 0], scale=[1/2, 1/2, 1/2], rotate=[89.5,91.1,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.display()
