from panda3d.core import Point2, Point3, Texture


app = None

def set_app(l_app):
    global app
    app = l_app

def load_object(tex = None, pos = Point2(0,0), depth = 0, transparency = True, scaleX = 1, scaleY = 1, scale = None):
    global app
    obj = app.loader.loadModel("models/plane")
    obj.reparentTo(app.render)

    obj.setPos(Point3(pos.getX(), pos.getY(), depth))

    if (scale == None):
        obj.setScale(scaleX, 1, scaleY)
    else:
        obj.setScale(scale)

    obj.setBin("unsorted", 0) # ignore draw order (z-fighting fix)       
    obj.setDepthTest(True)   # Don't disable depth write like the tut says
    obj.setHpr(0, -90, 0)

    if transparency:
        obj.setTransparency(1) #All of our objects are transparent
    else:
        obj.setTransparency(0) #All of our objects are transparent
    if tex:
        tex = app.loader.loadTexture("textures/"+tex+".png") #Load the texture
        tex.setWrapU(Texture.WMClamp)                    # default is repeat, which will give
        tex.setWrapV(Texture.WMClamp)                    # artifacts at the edges
        obj.setTexture(tex, 1)                           #Set the texture

    return obj

