import bpy
import os
from os.path import join
from random import uniform, triangular, choice
from math import radians


class MoveRender():
    
    def __init__(self, object = "ID_card", camera = "Camera", plastic = "Glossy_Plastic", 
    nb = 0, anim_lgth = 10, precision = 2,
    height_ob = 0.296, height_cam_min = 0.4, height_cam_max = 0.44,
    north_desk = 1.200, south_desk = 1.482, west_desk = 0.163, east_desk = 0.915, 
    cam_rot_y_min = -7, cam_rot_y_max = 7, cam_rot_x_min = -2, cam_rot_x_max = 2,
    cam_rot_z_min = 0, cam_rot_z_max = 360, id_rotz_min = 0, id_rotz_max = 360, translation_degree =0.09):
                
        self.ob = bpy.data.objects[object] #we select the ID card
        self.cam = bpy.data.objects[camera] #we select the camera we will use to render the card 
        self.plastic = bpy.data.objects[plastic] #we select the plastic part of the id card

        self.number = nb #number of pictures we have (at the start, it's 0)
        self.animation_length = anim_lgth #number of pictures we want

        self.z_ob = height_ob #ID fixed height
        self.z_cam_min = height_cam_min #camera min height
        self.z_cam_max = height_cam_max #camera max height

        self.precision = precision #precision of the position
        self.north = north_desk #coordinate x maximum
        self.south = south_desk #coordinate x minimum
        self.west = west_desk #coordinate y minimum
        self.east = east_desk #coordinate y maximum
        
        self.cam_roty_min = radians(cam_rot_y_min) #camera rotation min on the y axe 
        self.cam_roty_max = radians(cam_rot_y_max) #camera rotation max on the y axe 
        self.cam_rotx_min = radians(cam_rot_x_min) #camera rotation min on the x axe 
        self.cam_rotx_max = radians(cam_rot_x_max) #camera rotation max on the x axe 
        self.cam_rotz_min = radians(cam_rot_z_min) #camera rotation min on the z axe 
        self.cam_rotz_max = radians(cam_rot_z_max) #camera rotation max on the z axe
        
        self.id_rotz_min = radians(id_rotz_min) # ID rotation min on the x axe
        self.id_rotz_max = radians(id_rotz_max) # ID rotation max on the x axe
        
        self.tra_degree = translation_degree # translate the id card using a certain percentage of the actual position of the card
        
        self.desk_textures_dir = "C:/Users/anais/Documents/Esilv/S7/Parcours Recherche/Blender/Texture_Tables/" #file where the texture for the desk are taken
        self.desk = bpy.data.objects["Desk"] #
        self.desk_mat = bpy.data.materials["Desk"]
        
        
    def move_all(self): #we move the object (here an ID card and the camera randomly on the desk)
            
        x = round(uniform(self.north,self.south),self.precision)
        y = round(uniform(self.west,self.east),self.precision)
        z_cam = round(uniform(self.z_cam_min, self.z_cam_max), self.precision)

        self.ob.location = (x,y,self.z_ob)
        self.cam.location = (x,y,z_cam)
        #self.plastic.location = (x,y,self.z_plastic)
        
        
       
    def rotation(self):
        
        x_rot = round(uniform(self.cam_rotx_min,self.cam_rotx_max),self.precision)
        y_rot = round(uniform(self.cam_roty_min,self.cam_roty_max), self.precision)
        z_rot = round(uniform(self.cam_rotz_min, self.cam_rotz_max), self.precision)
        
        self.cam.rotation_euler = (x_rot, y_rot, z_rot)
        
        id_z_rot = round(uniform(self.id_rotz_min, self.id_rotz_max), self.precision)
        self.ob.rotation_euler = (0,0,id_z_rot)
        #self.plastic.rotation_euler =  (0,0,id_z_rot)
        
        
    def translation(self):
        
        x_tempo = self.cam.location.x
        x_tra = round(uniform(x_tempo-(x_tempo*self.tra_degree), x_tempo+(x_tempo*self.tra_degree)), self.precision)
        y_tempo = self.cam.location.y
        y_tra = round(uniform(y_tempo-(y_tempo*self.tra_degree), y_tempo+(y_tempo*self.tra_degree)), self.precision)
  
        self.cam.location = (x_tra,y_tra,self.cam.location.z)
        
        
        
    def render_and_save(self,filepath): #we render the camera view and save the picture in our folder
        
        scene.render.filepath = filepath.format(self.number)
        bpy.ops.render.render(write_still=True, use_viewport=True)
        
    
    def lighting(self, FLASH_BRIGHTNESS):
        
        scene = bpy.data.scenes[0]
        flash = bpy.data.objects["flash"]
        world_mat = bpy.data.worlds["World"]
        # is our camera flash on?
        flash.data.node_tree.nodes["Emission"].inputs[1].default_value =\
        round(uniform(0, 1),self.precision) * FLASH_BRIGHTNESS
        
        #adjust the ambient brightness of our HDRI world
        world_mat.node_tree.nodes["Background"].inputs[1].default_value = uniform(0, 1)
        
        # bigger aperature = blurrier outside of focal distance
        self.cam.data.cycles.aperture_size = uniform(0, 0.05)
        
        scene.cycles.film_exposure = triangular(0.2, 2, 0)
        
        
    def textures_and_mat(self, path):    
        """ load a random desk texture"""
        self.desk_mat.node_tree.nodes["Image Texture"].image = self.load_random_table(path)
    

    def load_random_table(self,path):
        """ pick a random desk texture and load it"""
        name = choice(os.listdir(bpy.path.abspath(self.desk_textures_dir)))
        print(name)
        path = join(self.desk_textures_dir, name)
        print(path)
        im = bpy.data.images.load(filepath = path)
        return im

        

if __name__ == "__main__":
    moveRender = MoveRender()
    scene = bpy.context.scene #shortcut
    scene.render.image_settings.file_format = 'PNG' #format de l'image obtenue
    filepath = "C:/Users/anais/Documents/Esilv/S7/Parcours Recherche/Blender/Images_carteID_Test/{}.png" #folder where the pictures will be sent
    texturespath = moveRender.desk_textures_dir
    FLASH_BRIGHTNESS = 5
    
    while moveRender.number < moveRender.animation_length:
        moveRender.move_all()
        moveRender.rotation()
        moveRender.translation()
        moveRender.lighting(FLASH_BRIGHTNESS)
        moveRender.textures_and_mat(texturespath)
        moveRender.render_and_save(filepath)
        moveRender.number+=1

