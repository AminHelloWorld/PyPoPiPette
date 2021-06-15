# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pygame
from pygame.locals import *



class segment:
    def __init__(self):
        '''
        Cree l'objet segment avec des parametres definissant sa couleur le nombre de carrés auquel il appartient et son objet rectangle de pygame
        '''
        self.couleur=None
        self.carrees=[] 
        self.rect=None
    
    def estTracee(self):
        '''
        Retourne True si le segment est tracé
        '''
        return not self.couleur is None
    
    def getCoul(self):
        '''
        Retourne la couleur du segment
        '''
        return self.couleur
    
    def tracer(self,joueur):
        '''
        Change la couleur du segment a la couleur du joueur seulement si le segment n'a pas deja de couleur'
        '''
        if self.couleur is None:
            self.couleur=joueur
            return True
    
    def __repr__(self):
        '''
        Change le contenu du print lorsque l'on print l'objet segment
        '''
        couleurs=['Bleu','Rouge']
        if self.estTracee():
            return f'{couleurs[self.getCoul()]}'
        return f'{self.getCoul()}'


class carree:
    def __init__(self,segment1,segment2,segment3,segment4):
        '''
        Cree un objet carrée prennant comme parametre les 4 objets segment qui le composent
        Cree aussi le parametre representant la couleur du carré
        '''
        self.segment1=segment1
        self.segment2=segment2
        self.segment3=segment3
        self.segment4=segment4
        self.couleur=None
        
        for i in self.getSegments(): #Ajoute cet objet carré a la liste de carrés de chaque segment
            i.carrees.append(self)
        
    def estRempli(self):
        '''
        Retourne True si le carré est rempli avec une couleur
        '''
        return not self.couleur is None
    
    def getSegments(self):
        '''
        Retourne les 4 objets segment qui composent ce carré.
        '''
        return self.segment1,self.segment2,self.segment3,self.segment4
        
    def getCoul(self):
        '''
        Retourne la couleur du carré
        '''
        return self.couleur
    
    def verifiercoul(self,dernierjou):
        '''
        Verifie si les 4 segments qui composent le carré sont coloriés.
        Dans ce cas remplit ce carré de la couleur de la couleur du dernier joueur
        '''
        if self.segment1.estTracee() and self.segment2.estTracee() and self.segment3.estTracee() and self.segment4.estTracee() and not self.estRempli(): 
            self.couleur=dernierjou
            return True
    
    def __repr__(self):
        '''
        Change le contenu du print lorsque l'on print l'objet carré
        '''
        couleurs=['Bleu','Rouge']
        couleur=f'{self.getCoul()}'
        if self.estRempli():
            couleur=f'{couleurs[self.getCoul()]}'
        return f'Segments :{self.segment1,self.segment2,self.segment3,self.segment4} \nCouleur: {couleur}'        


class grille:
    def __init__(self, nbcarreau):
        '''
        Cree l'objet grille qui prend comme parametre le nombre de carreaux que aura la grille
        
        self.grill est un double tableau qui contient les objets segment
        self.carreaux est un tableau qui contient les objets carré
        '''
        
        self.nbcarreau=nbcarreau
        self.grill=self.defGrille()
        self.carreaux=self.defCarreaux()
        
    def defGrille(self):
        '''
        Fonction qui cree le double tableau self.grill
        '''
        grill=[[],[]]
        coord=[]
        for i in range(2):
            coord=[]
            for y in range(self.nbcarreau):
                ligne=[]
                for z in range(self.nbcarreau+1):
                    ligne.append(segment())
                coord.append(ligne)
            # print(grill,coord,i)
            grill[i]=coord
        return grill
    
    def defCarreaux(self):
        '''
        Fonction qui cree le tableau self.carreaux
        '''
        carreaux=[]
        for i in range(self.nbcarreau**2):
            
            carreaux.append(carree(self.grill[0][i%self.nbcarreau][i//self.nbcarreau],self.grill[0][i%self.nbcarreau][(i//self.nbcarreau)+1],
                                   self.grill[1][i//self.nbcarreau][i%self.nbcarreau],self.grill[1][i//self.nbcarreau][(i%self.nbcarreau)+1]))
            
        return carreaux
    
    def __repr__(self):
        '''
        Change le contenu du print lorsque l'on print l'objet grille
        '''
        return "\n".join([str(c) for c in self.carreaux])
    


    
    
class jeu:
    def __init__(self, nbcarreau):
        '''
        initialise le jeu pipopipette creant ainsi la grille necessaire pour celui ci
        self.larg et self.haut sont respectivement les hauteurs et largeurs d'un segment des carrés de la grille
        self.marge est la marge utilisée pour centrer le programme
        '''
        self.nbcarreau=nbcarreau
        self.grille=grille(nbcarreau)
        self.tour=0
        self.marge=pygame.display.Info().current_w/6
        self.larg=round((pygame.display.Info().current_w-self.marge)/self.nbcarreau)
        self.haut=round((pygame.display.Info().current_h-self.marge)/self.nbcarreau)
    
    
    def jouer(self,segment):
        '''
        execute la fonction tracer de l'objet segment passé en parametre
        et verifie si un carré a été rempli
        si l'on a pu tracer le segment et aucun carré a été rempli on fait passer le tour
        '''
        if segment.tracer(self.tour%2) and not self.verifierCarr(segment):
            self.tour+=1
    
    def getSegment(self,pos):
        '''
        Renvoyé le segment correspondant aux coordonées données en parametre grace aux collisions des rectangles de pygame.
        '''
        for coord in self.grille.grill :
            for ligne in coord :
                for segment in ligne :
                    if segment.rect.collidepoint(pos):
                        return segment
    
    def verifierCarr(self,segment):
        '''
        Verifie si le coloriage de ce segment rempli un carré
        Renvoye True dans ce cas et False dans le cas contraire
        '''
        x=False
        for i in segment.carrees:
            if i.verifiercoul(self.tour%2):
                x=True
        return x
    
    def verifierGagnant(self):
        '''
        Verifie lequel des deux joueurs a gagne et retourne 1 ou 0 dependant de quel a gagné
        Retourne aussi le nombre de points du gagnant
        '''
        joueurs=[0,0]
        for carreau in self.grille.carreaux:
            if carreau.getCoul() is None:
                return None
            joueurs[carreau.getCoul()]+=1
        if joueurs[1]>joueurs[0]:
            return 1,joueurs[1]
        return 0,joueurs[0]
        
    def winScreen(self,gagnant):
        '''
        Affiche un ecran de victoire annonçant le gagnant
        prend comme parametre le retour de self.verifierGagnant
        '''
        surf.fill((0,0,0))
        i=['Joueur Bleu','Joueur Rouge']
        myfont = pygame.font.SysFont("Arial", 80)
        letter = myfont.render(i[gagnant[0]]+' gagne',0,(255,255,255))
        letter2= myfont.render('Avec '+str(gagnant[1])+' points',0,(255,255,255))
        surf.blit(letter,(100,100))
        surf.blit(letter2,(100,300))
    
    def afficherGrille(self):
        '''
        Affiche la grille sur la surface pygame

        '''
        colors={1:(255,0,0),0:(0,0,255),None:(255,255,255)}
        for carre in range(len(self.grille.carreaux)):
            if self.grille.carreaux[carre].estRempli():
                pygame.draw.rect(surf, 
                                 colors[self.grille.carreaux[carre].getCoul()],
                                 Rect(
          int(self.marge*2/3)+self.larg*(carre%self.nbcarreau),
          int(self.marge*2/3)+self.larg*(carre//self.nbcarreau),
          self.larg-int(self.marge*1/3),
          self.larg-int(self.marge*1/3)))
                
        # print (f'{self.grille}')
        for coord in range(len(self.grille.grill)):
            for ligne in range(len(self.grille.grill[coord])):
                for segment in range (len(self.grille.grill[coord][ligne])):
                    if coord==0:
                        self.grille.grill[coord][ligne][segment].rect = pygame.draw.line(surf,(colors[self.grille.grill[coord][ligne][segment].getCoul()]),
                                         (int(self.marge/2)+self.larg*ligne,
                                          int(self.marge/2)+self.haut*segment),
                                         (int(self.marge/2)+self.larg*(ligne+1),
                                          int(self.marge/2)+self.larg*segment),
                                         int(self.larg/10))
                    else:
                        self.grille.grill[coord][ligne][segment].rect = pygame.draw.line(surf,(colors[self.grille.grill[coord][ligne][segment].getCoul()]),
                                         (int(self.marge/2)+self.larg*segment,
                                          int(self.marge/2)+self.haut*ligne),
                                         (int(self.marge/2)+self.larg*segment,
                                          int(self.marge/2)+self.larg*(ligne+1)),
                                        int(self.larg/10))
        
        for i in range ((self.nbcarreau+1)**2):
            pygame.draw.circle(surf,(255,255,255),
                                (int(self.marge/2)+self.larg*(i//(self.nbcarreau+1)),
                                int(self.marge/2)+self.larg*(i%(self.nbcarreau+1))),
                                int(self.larg/10),
                                0)
      
    def jouerTour(self,segment):
        self.afficherGrille()
        self.jouer(segment)
        

#Initialisation du script
surf=pygame.display.set_mode((800,800))
wincon=True
game=jeu(3)
run=True

pygame.font.init()

while run:
    #Boucle principale du script
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()==(1,0,0):
                pos=pygame.mouse.get_pos()
                
                segment=game.getSegment(pos)
                if segment:
                    game.jouerTour(segment)
                gagnant=game.verifierGagnant()
                if gagnant is not None :
                    wincon=False
    if wincon:
        game.afficherGrille()
    else:
        game.winScreen(gagnant)
    pygame.display.flip()
pygame.quit()