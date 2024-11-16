import turtle
import math
from PIL import Image
import os
import random
import time

def compter_elements_identiques(tableau):
    nb=[]
    n=0
    for i in tableau:
        n+=1
        for j in range(n,len(tableau)):
            if i==tableau[j]:
                nb.append([n-1,j])
    print(nb)
def sauvegarder(titre):
    screen = turtle.Screen()
    image = screen.getcanvas()
    image.postscript(file=str(titre)+".ps", colormode='color')


    psimage = Image.open(str(titre)+".ps")
    psimage.save(str(titre)+".png")  



def dessinez(points,faces,titre):
    a=0
    turtle.speed(0)
    turtle.clear()
    turtle.hideturtle()
    turtle.pensize(1)
    for i in faces:
        
        turtle.penup()
        for j in range(len(i)): 
            if points[i[j]]!=False:
                turtle.goto(points[i[j]][0],points[i[j]][1])
                turtle.dot()
                turtle.pendown()
            else:
                turtle.up()
        if points[i[0]]!=False:   
            turtle.goto(points[i[0]][0],points[i[0]][1])
    sauvegarder(titre)
    

def faire_point(ligne):
    point=[]
    coordonées=""
    for i in range(2,len(ligne)):
        if ligne[i]==" ":
            
            point.append(float(coordonées))
            coordonées=""
        else:
            coordonées+=ligne[i]
    point.append(float(coordonées))
    points.append(point)

def faire_face(ligne):
    trios = ligne.split()
    premiers_entiers = []
    for trio in trios[1:]:
        premier_entier = int(trio.split('/')[0])
        premiers_entiers.append(premier_entier-1)
    faces.append(premiers_entiers)


def afficher_lignes_fichier(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                
                if ligne[0]=="v" and ligne[1]== " ":
                    faire_point(ligne)
                else:
                    if ligne[0]=="f":
                        faire_face(ligne)
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

def transformer_en_2d(points):
    nouveau_points=[]
    for i in points:
        if i[2]>0:
            nouveau_points.append([i[0]*distance_focale/i[2],i[1]*distance_focale/i[2]]) 
        else:
            nouveau_points.append(False)
    return nouveau_points

def regler_profondeur(points):
    for i in points:
        i[2]=camera-i[2]
    return points

def minimum(points):
    m=None
    mi=[]
    m=points[0][0]
    for i in points:
        if i[0]<m:
            m=i[0]
    mi.append(m)
    m=points[0][1]
    for i in points:
        if i[1]<m:
            m=i[1]
    mi.append(m)
    m=points[0][2]
    for i in points:
        if i[2]<m:
            m=i[2]
    mi.append(m)
    
    
    return mi


def maximum(points):
    m=None
    mi=[]
    m=points[0][0]
    for i in points:
        if i[0]>m:
            m=i[0]
    mi.append(m)
    m=points[0][1]
    for i in points:
        if i[1]>m:
            m=i[1]
    mi.append(m)
    m=points[0][2]
    for i in points:
        if i[2]>m:
            m=i[2]
    mi.append(m)
    
    
    return mi


def centre(points):
    mini=minimum(points)
    maxi=maximum(points)
    centre=[]
    for i in range(len(mini)):
        centre.append((mini[i]+maxi[i])//2)
    return centre
def rotation(points,centre,r,axe):
    
    
    y2=0
    x2=0
    r=r*(math.pi/180)
    axe1=0
    axe2=2
    if axe=="y":
        axe1=0
        axe2=2
        
    elif axe=="x":
        axe1=1
        axe2=2
    elif axe=="z":
        axe1=0
        axe2=1

    for i in points:
        x2=((i[axe1]-centre[axe1])*math.cos(r))-((i[axe2]-centre[axe2])*math.sin(r))+centre[axe1]
        y2=((i[axe1]-centre[axe1])*math.sin(r))+((i[axe2]-centre[axe2])*math.cos(r))+centre[axe2]

        i[axe1]=x2
        i[axe2]=y2
    return points

def avancer(points,pas):
    for i in points:
        i[2]-=pas
    return points
def monter(points,pas):
    for i in points:
        i[1]+=pas
    return points
def decaler(points,pas):
    for i in points:
        i[0]+=pas
    return points



def creer_gif(n):
    
   
    output_gif = "animation"+str(random.randint(0,99999999))+".gif"

    # Liste pour stocker les images
    images = []

    # Charger les images
    for i in range(n + 1):
        image_path = f"{i}.png"
        if os.path.exists(image_path):
            images.append(Image.open(image_path))

    # Créer un GIF
    if images:
        images[0].save(output_gif, save_all=True, append_images=images[1:], duration=83, loop=0)

    # Supprimer les images
    for i in range(n + 1):
        image_path = f"{i}.png"
        image_path2 = f"{i}.ps"
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(image_path2):
            os.remove(image_path2)

    print(f"GIF créé et enregistré sous le nom '{output_gif}'. Toutes les images sources ont été supprimées.")

if __name__=="__main__":
    points=[]
    faces=[]
    images = []
    distance_focale=1000
    camera=8
    nbimages=9
    afficher_lignes_fichier("cube.obj")
    points=regler_profondeur(points)
    point_centrale=centre(points)
    titre=""
    image=0
    s=time.time()
    """points_en_2d=transformer_en_2d(points)
    image+=1
    dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=rotation(points,point_centrale,10,"x")
        points_en_2d=transformer_en_2d(points)
        image+=1
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=rotation(points,point_centrale,10,"y")
        points_en_2d=transformer_en_2d(points)
        image+=1
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=rotation(points,point_centrale,10,"z")
        points_en_2d=transformer_en_2d(points)
        image+=1
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=avancer(points,1)
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=avancer(points,-1)
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=monter(points,1)
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=monter(points,-1)
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)      
    for i in range(nbimages):
        points=decaler(points,1)
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)
    for i in range(nbimages):
        points=decaler(points,-1)
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)    
    for i in range(nbimages):
        points=avancer(points,1)
        point_centrale=centre(points)
        points=rotation(points,point_centrale,10,"x")
        points=rotation(points,point_centrale,10,"y")
        points=rotation(points,point_centrale,10,"z")
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image) """      
    
    for i in range(nbimages):
       
        
        
        points=rotation(points,point_centrale,10,"y")
        
        
        image+=1
        points_en_2d=transformer_en_2d(points)
        dessinez(points_en_2d,faces,image)  
        print(time.time()-s)
    
    
    
    creer_gif(image+1)    
   


    
