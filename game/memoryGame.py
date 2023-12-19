# Importation des bibliothèques nécessaires
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image as PilImage
from PIL import ImageTk
import random
import time

# Définition de la classe principale du jeu de mémoire
class MemoryGame:

    def __init__(self, master):
        self.master = master
        self.master.title("Jeu de Mémoire - Technologies Informatiques")
        self.master.configure(bg="lightblue")
        self.master.geometry("800x600")
        self.show_welcome_screen()  # Appelle la fonction pour afficher l'écran de bienvenue

        # Variables de configuration du jeu
        self.difficulty_var = tk.StringVar(value="Débutant")
        self.mode_var = tk.StringVar(value="Solo")
        self.mode_var.trace_add("write", self.update_mode_display)  # Suivi des changements de mode

        # Variables du jeu
        self.player_turn = 1
        self.player_scores = {1: 0, 2: 0}
        self.player_pairs = {1: 0, 2: 0}
        self.player_names = {1: "Joueur 1", 2: "Joueur 2"}
        self.score_labels = {}
        self.start_time = None
        self.elapsed_time = None

        # Variables spécifiques au mode solo
        self.correct_attempts_solo = 0
        self.incorrect_attempts_solo = 0

        # Variables spécifiques au mode multijoueur
        self.correct_attempts = {1: 0, 2: 0}
        self.incorrect_attempts = {1: 0, 2: 0}

        # Liste des entrées pour les noms des joueurs
        self.name_entries = [tk.Entry(self.master) for _ in range(4)]  # Crée 4 entrées, mais ne les affiche pas encore
        self.update_mode_display()

        # Liste des images avec leurs catégories
        self.images_with_categories = [
            ('image1-1.png', 1), ('image1-2.png', 1),
            ('image2-1.png', 2), ('image2-2.png', 2),
            ('image3-1.png', 3), ('image3-2.png', 3),
            ('image4-1.png', 4), ('image4-2.png', 4),
            ('image5-1.png', 5), ('image5-2.png', 5),
            ('image6-1.png', 6), ('image6-2.png', 6),
            ('image7-1.png', 7), ('image7-2.png', 7),
            ('image8-1.png', 8), ('image8-2.png', 8),
            ('image9-1.png', 9), ('image9-2.png', 9),
            ('image10-1.png', 10), ('image10-2.png', 10)
        ]

    # Fonction pour afficher l'écran de bienvenue
    def show_welcome_screen(self):
        # Afficher une image explicative du jeu
        welcome_img = PilImage.open('welcome_image.png')  # Assurez-vous que cette image existe
        welcome_img = welcome_img.resize((500, 400))
        self.welcome_image = ImageTk.PhotoImage(welcome_img)

        welcome_image_label = tk.Label(self.master, image=self.welcome_image)
        welcome_image_label.pack(pady=10)

        # Afficher un texte de bienvenue
        welcome_text = tk.Label(self.master, text="Bienvenue dans le Jeu de Mémoire!\nCliquez ci-dessous pour commencer.", bg="lightblue")
        welcome_text.pack(pady=10)

        # Bouton pour passer aux options du jeu
        start_button = tk.Button(self.master, text="Commencer", command=self.create_game_options)
        start_button.pack(pady=20)

    # Fonction pour créer les options de jeu
    def create_game_options(self):
        # Supprimer tous les widgets de la page de bienvenue
        for widget in self.master.winfo_children():
            widget.destroy()

        # Initialisation des variables
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Débutant")
        self.mode_var = tk.StringVar()
        self.mode_var.set("Solo")
        self.mode_var.trace('w', self.update_mode)
        self.player_turn = 1
        self.player_scores = {1: 0, 2: 0}
        self.player_pairs = {1: 0, 2: 0}
        self.player_names = {1: "Joueur 1", 2: "Joueur 2"}
        self.score_labels = {}
        self.start_time = None

        # Choix de la difficulté
        difficulty_label = tk.Label(self.master, text="Choisissez un niveau de difficulté:", bg="lightblue")
        difficulty_label.pack(pady=10, padx=10)

        difficulty_options = ["Débutant", "Avancé", "Expert"]
        difficulty_menu = tk.OptionMenu(self.master, self.difficulty_var, *difficulty_options)
        difficulty_menu.pack(pady=5)

        # Choix du mode de jeu
        mode_label = tk.Label(self.master, text="Choisissez un mode de jeu:", bg="lightblue")
        mode_label.pack(pady=10, padx=10)

        mode_menu = tk.OptionMenu(self.master, self.mode_var, *["Solo", "Multijoueur"], command=self.update_mode)
        mode_menu.pack(pady=5)
       
        # Entrée des noms des joueurs
        self.name_entry_1 = tk.Entry(self.master, bg="lightgray", font=("Arial", 12))
        self.name_entry_1.insert(0, "Nom du Joueur 1")
        self.name_entry_1.bind("<FocusIn>", lambda _: self.clear_entry(self.name_entry_1, 1))
   

        self.name_entry_2 = tk.Entry(self.master, bg="lightgray", font=("Arial", 12))
        self.name_entry_2.insert(0, "Nom du Joueur 2")
        self.name_entry_2.bind("<FocusIn>", lambda _: self.clear_entry(self.name_entry_2, 2))
        

        # Bouton pour commencer le jeu
        start_game_button = tk.Button(self.master, text="Commencer le jeu", font=("Arial", 14), command=self.start_game)
        start_game_button.pack(pady=20)

    # Fonction pour mettre à jour le mode de jeu
    def update_mode(self, *args):
        mode = self.mode_var.get()
        if mode == "Multijoueur":
            self.name_entry_1.pack(pady=5)
            self.name_entry_2.pack(pady=5)
        else:
            self.name_entry_1.pack_forget()
            self.name_entry_2.pack_forget()

    # Fonction pour afficher les entrées des noms des joueurs
    def show_player_entries(self):
        # Supprimer tous les widgets précédemment affichés pour les noms des joueurs
        for entry in getattr(self, 'name_entries', []):
            entry.pack_forget()

        # Réinitialiser la liste des entrées et ajouter les deux premiers joueurs par défaut
        self.name_entries = [self.name_entry_1, self.name_entry_2]
        for entry in self.name_entries:
            entry.pack(pady=5)

        # Afficher le bouton pour ajouter des joueurs
        self.add_player_button.pack(pady=5)

    # Fonction pour ajouter une entrée de joueur supplémentaire
    def add_player_entry(self):
        # Limiter le nombre de joueurs à un maximum, par exemple 4
        if len(self.name_entries) < 4:
            player_number = len(self.name_entries) + 1
            entry = tk.Entry(self.master, bg="lightgray", font=("Arial", 12))
            entry.insert(0, f"Nom du Joueur {player_number}")
            entry.bind("<FocusIn>", lambda e, num=player_number: self.clear_entry(e, num))
            entry.pack(pady=5)
            self.name_entries.append(entry)

    # Fonction pour effacer le texte d'une entrée de nom de joueur lorsque le focus est dessus
    def clear_entry(self, event, player_number):
        if event.get() == f"Nom du Joueur {player_number}":
            event.delete(0, 'end')

    # Fonction pour masquer les entrées des noms des joueurs
    def hide_player_entries(self):
        if hasattr(self, 'name_entries'):
            for entry in self.name_entries:
                entry.pack_forget()
        self.add_player_button.pack_forget()


    # Fonction pour démarrer le jeu
    def start_game(self):
        # Charger l'image cachée
        hidden_img = PilImage.open('hidden.png')
        hidden_img = hidden_img.resize((50, 50))
        self.hidden_image = ImageTk.PhotoImage(hidden_img)

        difficulty = self.difficulty_var.get()

        # Définir le nombre de catégories en fonction de la difficulté
        if difficulty == "Débutant":
            num_categories = 4
        elif difficulty == "Avancé":
            num_categories = 6
        else:  # Expert
            num_categories = 10

        # Sélectionnez les images en fonction du nombre de catégories
        selected_categories = set()
        while len(selected_categories) < num_categories:
            _, category = random.choice(self.images_with_categories)
            selected_categories.add(category)

        selected_images = [img for img, cat in self.images_with_categories if cat in selected_categories]

        # Mélanger les images sélectionnées
        random.shuffle(selected_images)

        # Créer la liste des cartes pour le jeu
        self.cards = selected_images
        random.shuffle(self.cards)

        # Chargez les images pour les cartes sélectionnées
        self.images = {}
        for img_path in selected_images:
            img = PilImage.open(img_path)
            img = img.resize((50, 50))
            self.images[img_path] = ImageTk.PhotoImage(img)

        # Configuration de la fenêtre de jeu
        self.game_window = tk.Toplevel(self.master)
        self.game_window.title("Jeu de Mémoire - En cours")

        # Configuration des noms des joueurs en mode multijoueur
        if self.mode_var.get() == "Multijoueur":
            self.player_names[1] = self.name_entry_1.get() if self.name_entry_1.get() else "Joueur 1"
            self.player_names[2] = self.name_entry_2.get() if self.name_entry_2.get() else "Joueur 2"
            self.score_labels[1] = tk.Label(self.game_window, text=f"{self.player_names[1]}: 0")
            self.score_labels[1].grid(row=0, column=num_categories * 2 + 1)
            self.score_labels[2] = tk.Label(self.game_window, text=f"{self.player_names[2]}: 0")
            self.score_labels[2].grid(row=1, column=num_categories * 2 + 1)

        # Création des boutons pour le tableau de jeu
        self.board_buttons = []
        for i in range(num_categories * 2):
            row = i // 4
            col = i % 4
            button = tk.Button(self.game_window, image=self.hidden_image, width=100, height=100, command=lambda i=i: self.flip_card(i))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.board_buttons.append(button)

        # Initialisation des variables de jeu
        self.matched_pairs = []
        self.selected_cards = []

        # Mise à jour du tableau de jeu
        self.update_board()
        self.start_time = time.time()


    # Fonction pour retourner une carte lorsque le joueur clique dessus
    def flip_card(self, index):
        if len(self.selected_cards) < 2 and index not in [i for i, _ in self.selected_cards]:
            card_img_path = self.cards[index]
            self.selected_cards.append((index, card_img_path))
            self.update_board()

            if len(self.selected_cards) == 2:
                self.master.after(1000, self.check_match)


    # Fonction pour vérifier si les cartes sélectionnées correspondent
    def check_match(self):
        card1_index, card1_img_path = self.selected_cards[0]
        card2_index, card2_img_path = self.selected_cards[1]

        # Trouver les catégories des cartes sélectionnées
        card1_category = [category for img, category in self.images_with_categories if img == card1_img_path][0]
        card2_category = [category for img, category in self.images_with_categories if img == card2_img_path][0]

        if card1_category == card2_category:
            # Pour le mode solo
            if self.mode_var.get() == "Solo":
                self.correct_attempts_solo += 1
            else:
                # Pour le mode multijoueur
                self.correct_attempts[self.player_turn] += 1

            # Mise à jour des paires et du score pour le joueur actuel
            self.matched_pairs.extend([card1_index, card2_index])
            self.player_pairs[self.player_turn] += 1
            if self.mode_var.get() == "Multijoueur":
                self.player_scores[self.player_turn] += 1
                self.score_labels[self.player_turn].config(text=f"{self.player_names[self.player_turn]}: {self.player_pairs[self.player_turn]}")

            # Vérifiez si toutes les paires ont été trouvées
            if len(self.matched_pairs) == len(self.board_buttons):
                self.end_game()
            self.selected_cards = []  # Réinitialiser la sélection
            self.update_board()  # Mise à jour immédiate de l'affichage

        else:
            if self.mode_var.get() == "Solo":
                self.incorrect_attempts_solo += 1
            else:
                self.incorrect_attempts[self.player_turn] += 1
                self.player_turn = 1 if self.player_turn == 2 else 2

            # Réinitialisez les cartes sélectionnées et mettez à jour le tableau
            self.selected_cards = []
            self.update_board()


    # Fonction pour afficher le podium et les résultats
    def show_podium(self):
        # Créer une nouvelle fenêtre pour le podium
        podium_window = tk.Toplevel(self.master)
        podium_window.title("Résultats du Jeu")
        podium_window.configure(bg="lightblue")

        # Message de félicitations
        congrats_label = tk.Label(podium_window, text="Félicitations ! Voici les résultats :", bg="lightblue", font=("Arial", 14))
        congrats_label.pack(pady=10)

        # Afficher les résultats spécifiques du mode solo
        if self.mode_var.get() == "Solo":
            results_label = tk.Label(podium_window, text=f"Tentatives justes : {self.correct_attempts_solo}\nTentatives fausses : {self.incorrect_attempts_solo}\nTemps écoulé : {self.elapsed_time:.2f} secondes", bg="lightblue", font=("Arial", 12))
            results_label.pack()
        else:
            # Pour le mode multijoueur, trouver et afficher le gagnant
            winner = max(self.player_scores, key=self.player_scores.get)
            winner_label = tk.Label(podium_window, text=f"Le gagnant est {self.player_names[winner]} avec {self.player_scores[winner]} paires trouvées!", bg="gold", font=("Arial", 14, "bold"))
            winner_label.pack(pady=(10, 20))

            # Afficher les scores de tous les joueurs
            for player, score in self.player_scores.items():
                player_label = tk.Label(podium_window, text=f"{self.player_names[player]}: {score} paires trouvées\nTentatives justes : {self.correct_attempts[player]}\nTentatives fausses : {self.incorrect_attempts[player]}", bg="lightblue", font=("Arial", 12))
                player_label.pack()

        # Bouton pour fermer le podium
        close_button = tk.Button(podium_window, text="Fermer", command=podium_window.destroy)
        close_button.pack(pady=10)


    # Fonction pour gérer la fin du jeu
    def end_game(self):
        self.elapsed_time = time.time() - self.start_time

        # Afficher le podium
        self.show_podium()
        self.game_window.destroy()


    # Fonction pour mettre à jour l'affichage du tableau de jeu
    def update_board(self):
        if self.game_window.winfo_exists():
            for i, button in enumerate(self.board_buttons):
                card_img_path = self.cards[i]
                if (i, card_img_path) in self.selected_cards or i in self.matched_pairs:
                    button.config(image=self.images[card_img_path])
                else:
                    button.config(image=self.hidden_image)

    # Fonction pour mettre à jour l'affichage en fonction du mode de jeu
    def update_mode_display(self, *args):
        mode = self.mode_var.get()
        if mode == "Solo":
            for entry in self.name_entries:
                entry.pack_forget()
        elif mode == "Multijoueur":
            for entry in self.name_entries:
                entry.pack()  # Affiche toutes les entrées si le mode est Multijoueur


if __name__ == "__main__":
    # Crée une instance de la classe MemoryGame et l'attache à la fenêtre principale
    root = tk.Tk()
    app = MemoryGame(root)

    # Démarre la boucle principale de l'interface graphique
    root.mainloop()
