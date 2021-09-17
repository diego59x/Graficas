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
#print("salio textura")
r.lookAt(V3(0,0,5), V3(0,0,0), V3(0,1,0))
#print("salio lookAt")
r.load('./VertexBuffer/models/model.obj',translate=[0, 0, 0], scale=[1, 1, 1], rotate=[0,0,0])
#print("salio load")
r.active_shader = gourad
#print("salio gorad")
r.draw_arrays('TRIANGLES')
print("salio draw")
r.display()