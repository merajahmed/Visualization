import cherrypy
import json
import h5py as h5
import numpy as np
from yt.units.dimensions import velocity
class Haloes(object):
    @cherrypy.expose
    def index(self):        
        return file('index.html')
    @cherrypy.expose
    def fetchparticles(self,**args):   
        HaloId = 'Halo00000000'
        halo_particles = h5.File('basename.h5','r')
        xcoords =  halo_particles[HaloId]['particle_position_x']
        ycoords = halo_particles[HaloId]['particle_position_y']
        zcoords = halo_particles[HaloId]['particle_position_z']
        xvelocity = halo_particles[HaloId]['particle_velocity_x']
        yvelocity = halo_particles[HaloId]['particle_velocity_y']
        zvelocity = halo_particles[HaloId]['particle_velocity_z']
        velocity = np.sqrt(np.square(xvelocity)+np.square(yvelocity)+np.square(zvelocity))
        X = np.array(xcoords,dtype=np.float64)
        Y = np.array(ycoords,dtype=np.float64)
        Z = np.array(zcoords,dtype=np.float64)
        xlist = X.tolist()
        ylist = Y.tolist()
        zlist = Z.tolist()
        vlist = velocity.tolist()
    @cherrypy.expose
    def fetchparticlescsv(self,**args):  
        haloId = args['haloId[0]']
        print haloId
        raise cherrypy.HTTPRedirect('static/haloview.html')
        
        
if __name__ == '__main__':
    conf = {
         '/': {
             'tools.sessions.on': True,
         },
         '/generator': {
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         },
         '/static': {
             'tools.staticdir.on': True,
         'tools.staticdir.root':"/media/meraj/Seagate Backup Plus Drive/backupworkspace/darksky/",
             'tools.staticdir.dir':'static'
         }
    }
webapp = Haloes()
cherrypy.config.update({'server.socket_host':'0.0.0.0'})
cherrypy.quickstart(webapp, '/', conf)
