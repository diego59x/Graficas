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
 
r = Renderer(2000,2000)
r.current_texture = Texture('./VertexBuffer/models/lamp.bmp')
r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
r.load('./VertexBuffer/models/lamp.obj',translate=[0.7, -0.5, 0], scale=[1, 1, 1], rotate=[1,0.3,5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./VertexBuffer/models/monitor.bmp')
r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
r.load('./VertexBuffer/models/monitor.obj',translate=[0.7, -0.5, 0], scale=[1/6, 1/6, 1/2], rotate=[90,90,-4.7])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.current_texture = Texture('./VertexBuffer/models/model.bmp')
r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
r.load('./VertexBuffer/models/model.obj',translate=[0, 0, 0], scale=[1/3, 1/3, 1/3], rotate=[90,-0.3,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')

r.display()


''' Monitor 
    r = Renderer(2000,2000)
    r.current_texture = Texture('./VertexBuffer/models/monitor.bmp')
    r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
    r.load('./VertexBuffer/models/monitor.obj',translate=[0.7, -0.5, 0], scale=[1/6, 1/6, 1/2], rotate=[90,90,-4.7])
    Cara 
    r.current_texture = Texture('./VertexBuffer/models/model.bmp')
    r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
    r.load('./VertexBuffer/models/model.obj',translate=[0, 0, 0], scale=[1/2, 1/2, 1], rotate=[90,90,-5])
    Lampara (es negra y no c ve)
    r.current_texture = Texture('./VertexBuffer/models/lamp.bmp')
    r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
    r.load('./VertexBuffer/models/lamp.obj',translate=[0.7, -0.5, 0], scale=[1, 1, 1], rotate=[0,0,0])

'''