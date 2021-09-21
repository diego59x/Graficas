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
 
r = Renderer(800,800)
r.current_texture = Texture('./VertexBuffer/models/model.bmp')
r.lookAt(V3(0,1,3), V3(0,0,0), V3(0,1,0))
r.load('./VertexBuffer/models/model.obj',translate=[0, 0, 0], scale=[1/2, 1/2, 1], rotate=[90,90,-5])
r.active_shader = gourad
r.draw_arrays('TRIANGLES')
r.display()