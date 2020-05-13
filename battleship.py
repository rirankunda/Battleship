from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from random import randint
from kivy.uix.popup import Popup
import json



class Game(App):
    def build(self):
        self.soundboom = SoundLoader.load('boum.mp3') #son en cas de cible touchée
        self.soundplouf= SoundLoader.load('plouf.mp3') #son en cas de cible manquée
        self.iclique=0 #nombre de cliques total
        self.iC=0 #compteur des croiseurs touchés
        self.iT=0 #compteur des torpilleurs touchés
        self.iS=0 #compteur des sous-marins touchés
        self.iP=0 #compteur des portes-avions touchés
        self.iTot=0 #compteur des cibles touchés
        Letters=['A','B','C','D','E','F','G','H','I','J'] #Liste des noms des lignes
        self.title = 'Battleship' #Titre du jeu
        box1=BoxLayout(orientation='vertical') #Création d'une box globale dans laquelle les éléments vont s'ajouter
                                               #du haut vers le bas

        #Highscore=Label(text=str(self.top),size_hint=(1,0.1)) #création de la ligne contenant le plus haut score
        

        line1=GridLayout(rows=1,cols=11, size_hint=(1, 0.1)) #Création de la ligne des noms des colonnes
        line1.add_widget(Label(text=''))
        for i in range(2,12):
            line1.add_widget(Label(text=str(i-1)))
        
        box2=BoxLayout(orientation='horizontal') #Création d'une deuxième box dans laquelle on va mettre la colonnes des noms des
                                                 #lignes et la grille clicable. C'est une box dans lequel les éléments vont 
                                                 #s'ajouter de la gauche vers la droite

        row1=GridLayout(rows=10,cols=1, size_hint=(0.1,1)) #Création de la colonnes des noms des lignes
        for i in range(len(Letters)):
            row1.add_widget(Label(text=Letters[i]))

        grid=GridLayout(rows=10,cols=10) #Création de la grille clicable
        #Dans cette boucle for on va associer le plan donné à notre grille cliquable
        for k in range (1,101):
            file = open(str(randint(0,3))+'plan.txt') 
            content=file.read()
            file.close()
            a=content.splitlines()
            emplacement=''#on crée un autre "tableau" car le fichier donné n'est pas sous le bon format donc on doit le convertir pour qu'il soit dans le bon format et sauver ce format dans notre tableau ensemble
            for i in range (1,11):
                for j in range (1,11):
                    if a[i][j]=='c' or a[i][j]=='t' or a[i][j]=='p' or a[i][j]=='s':
                        emplacement=emplacement+a[i][j]
                    else:
                        emplacement=emplacement+' '
            buttons=emplacement
        for s in range (len(buttons)):
            self.button = Button(text=buttons[s])
            self.button.background_color=(1,1,1,1)
            self.button.color=(0,0,0,0) #Change la couleur de la lettre
            self.button.bind(on_press=self.fire) #Ajout d'une fonction qui se lance lorsqu'on clique sur une case
            grid.add_widget(self.button)
            
        box2.add_widget(row1) #Ajout de la colonne des noms de lignes dans la deuxième box
        box2.add_widget(grid) #Ajout de la grille dans la deuxième box

        self.output = Label() #Création d'une zone de texte
        self.output.size_hint=(1,0.1)
        
        #box1.add_widget(Highscore) #ajout de la ligne du meilleur score
        box1.add_widget(line1) #Ajout de la ligne des noms de colonnes dans la première box
        box1.add_widget(box2) #Ajout de la deuxièmebox dans la première
        box1.add_widget(self.output) #Ajout de la zone de texte dans la première box
        
        return box1

    def fire(self,src): #Idée de départ de la fonction qui renvoi des messages lorsqu'on clique sur une case
        self.iclique=self.iclique+1
        src.disabled=True
        if self.iTot==17:
            
            self.score=str(100*17/(self.iclique-1)) #variable score accessible plus loin 

            content = BoxLayout(orientation='vertical')    #création d'une box 
            content.add_widget(Label(text='score: '+ self.score +'%', font_size=25)) #création d'un label donnant le score de la partie
            Line = BoxLayout(orientation='horizontal',size_hint=(1, 0.1)) #création d'une autre box
            Line.add_widget(Label(text='Entrez votre pseudo')) #création d'un label 
            self.Pseudo=TextInput() #création d'un text input auquel on pourra accéder plus loin
            Line.add_widget(self.Pseudo) 
            Enter=Button(text='Entrer') #création d'un bouton
            Line.add_widget(Enter)
            content.add_widget(Line)

            #fait apparaitre un popup qui annonce la fin
            popup = Popup(title='Félicitations vous avez coulé tous les bateaux!',content=content, size_hint=(0.7,0.7))
            Enter.bind(on_press=popup.dismiss)
            Enter.bind(on_press=self.save)
            popup.open()


        elif src.text=='c':
            self.soundboom.play()
            src.background_color=(100,1,1,1)
            src.color=(100,0,0,0)
            self.iC=self.iC+1 
            self.iTot=self.iTot+1
            if self.iC<4:
                self.output.text='croiseur touché'
            else:
                self.output.text='croiseur coulé'
        elif src.text == 't' :
            self.soundboom.play()
            src.background_color=(100,1,1,1)
            src.color=(100,0,0,0)
            self.iT=self.iT+1
            self.iTot=self.iTot+1
            if self.iT<2:
                self.output.text='torpilleur touché'
            else:
                self.output.text='torpilleur coulé'
        elif src.text == 's' :
            self.soundboom.play()
            src.background_color=(100,1,1,1)
            src.color=(100,0,0,0)
            self.iS=self.iS+1            
            self.iTot=self.iTot+1
            if self.iS<6:
                self.output.text='sous-marin touché,attention il y a deux sous-marins distincts'
            else:
                self.output.text='les sous-marins sont coulés'
        elif src.text == 'p' :
            self.soundboom.play()
            src.background_color=(100,1,1,1)
            src.color=(100,0,0,0)            
            self.iP=self.iP+1
            self.iTot=self.iTot+1
            if self.iP<5:
                self.output.text='porte-avion touché'
            else:
                self.output.text='porte-avion coulé'
        else :
            self.soundplouf.play()
            src.background_color=(1,1,100,1)
            self.output.text='raté'

    def save(self,src): #fonction qui met à jour le fichier json
        name = self.Pseudo.text
        with open("score.json","r") as file: #ouverture du fichier en lecture
            ChaineJson=file.read() 
            dictionary=json.loads(ChaineJson)

            if name not in dictionary :  #si le pseudo entré n'existe pas encore on l'ajoute au fichier json
                dictionary[name]=[self.score]
            else :                                  #si le pseudo existe on regarde si le score actuel est meilleur que le premier score de la liste
                if dictionary[name][0]<self.score : #si oui on le met en premier
                    inf=dictionary[name][0]
                    dictionary[name][0]=self.score
                    dictionary[name].append(inf)
                else :                              #si non on met le score à la suite des autres
                    dictionary[name].append(self.score)
                        
                
        with open("score.json","w") as file:        #on ouvre le fichier en écriture et on y met le dictionnaire créé
            ChaineJson=json.dumps(dictionary, indent= '\t')
            file.write(ChaineJson)

    def top(self,src):               #idée de fonction permettant d'afficher le meilleur score
        best=0
        with open("score.json","r") as file:
            ChaineJson=file.read()
            dictionary=json.loads(ChaineJson)

            for name in dictionary :
                if dictionary[name][0]>self.best :
                    best=dictionary[name][0]


        

Game().run()
