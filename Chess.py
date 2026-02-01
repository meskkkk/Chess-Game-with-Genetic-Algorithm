import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk
import chess
import random

class GeneticAlgorithm:

    def evaluate_fitness(self):
        """Evaluate the fitness of all possible moves for the black player."""
        fitness_scores = {}
        for move in self.board.legal_moves:
            # Apply the move and evaluate the board after it
            self.board.push(move)
            score = self.calculate_score()  # Calculate score for the move
            fitness_scores[move] = score
            self.board.pop()  # Undo the move to check other moves
        return fitness_scores

    def calculate_score(self):
        """Calculate the score based on material, piece safety, and other criteria."""
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                # Material value
                if piece.piece_type == chess.PAWN:
                    score += 1
                elif piece.piece_type == chess.KNIGHT:
                    score += 3
                elif piece.piece_type == chess.BISHOP:
                    score += 3
                elif piece.piece_type == chess.ROOK:
                    score += 5
                elif piece.piece_type == chess.QUEEN:
                    score += 9
                elif piece.piece_type == chess.KING:
                    score += 100  # King is invaluable

                # Piece safety: Check if the piece is under attack
                if not self.is_piece_safe(piece, square):
                    score -= 2

                # Control of the center (squares: d4, e4, d5, e5)
                if square in [chess.D4, chess.E4, chess.D5, chess.E5]:
                    score += 1

        return score

    def is_piece_safe(self, piece, square):
        """Determine if a piece is in a safe position (not under immediate threat)."""
        for move in self.board.legal_moves:
            if move.to_square == square:
                return False  # The piece is under attack
        return True

    def genetic_algorithm(self, board, generations=20, population_size=10, mutation_rate=0.2, sequence_length=3):
     """
    Use an improved genetic algorithm to find the best move sequence for the black player.
    :param generations: Number of generations for the algorithm.
    :param population_size: Number of sequences in each generation's population.
    :param mutation_rate: Probability of mutation for each sequence.
    :param sequence_length: Number of moves in each sequence (depth of search).
    :return: The best move (first move in the best sequence).
    """
    # Step 1: Generate initial population (random move sequences)
     self.board = board
     population = [
        [random.choice(list(self.board.legal_moves)) for _ in range(sequence_length)]
        for _ in range(population_size)
     ]

     for generation in range(generations):
        # Step 2: Evaluate fitness of each sequence in the population
        fitness_scores = {tuple(sequence): self.evaluate_sequence(sequence) for sequence in population}

        # Step 3: Select the top sequences based on fitness (elitism)
        sorted_population = sorted(population, key=lambda seq: fitness_scores[tuple(seq)], reverse=True)
        top_sequences = sorted_population[:population_size // 2]  # Keep the top 50% of sequences

        # Step 4: Crossover - Create new sequences by combining top sequences
        children = self.crossover_sequences(top_sequences, population_size - len(top_sequences))

        # Step 5: Mutation - Randomly mutate some sequences
        for i in range(len(children)):
            if random.random() < mutation_rate:
                children[i] = self.mutate_sequence(children[i])

        # Combine the top sequences and the children to form the new population
        population = top_sequences + children

    # Final Step: Return the best move (first move in the best sequence)
     best_sequence = max(population, key=lambda seq: self.evaluate_sequence(seq))
     return best_sequence[0]  # Return the first move in the best sequence

    def evaluate_sequence(self, sequence):
     """
    Evaluate the fitness of a given move sequence.
    :param sequence: A list of chess moves to evaluate.
    :return: The fitness score of the sequence.
    """
     score = 0
     pushed_moves = 0  # Track how many moves were successfully pushed

     try:
         for move in sequence:
            if move not in self.board.legal_moves:
                break  # Stop if the move is illegal
            self.board.push(move)  # Apply the move
            pushed_moves += 1
            score += self.calculate_score()  # Evaluate the board state
     finally:
        # Undo only the moves that were successfully pushed
        for _ in range(pushed_moves):
            self.board.pop()

     return score

    def crossover_sequences(self, top_sequences, num_children):
     """
    Perform crossover to create new sequences by combining top sequences.
    :param top_sequences: A list of the top move sequences based on fitness.
    :param num_children: Number of new sequences to generate.
    :return: A list of new sequences (children).
    """
     children = []
     for _ in range(num_children):
        # Randomly select two parent sequences
        parent1 = random.choice(top_sequences)
        parent2 = random.choice(top_sequences)

        # Combine parents to create a child sequence
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        children.append(child)
     return children

    def mutate_sequence(self, sequence):
     """
    Mutate a given move sequence by altering one move.
    :param sequence: The chess move sequence to mutate.
    :return: A new mutated sequence.
    """
     mutation_index = random.randint(0, len(sequence) - 1)
     mutated_sequence = sequence[:]
     mutated_sequence[mutation_index] = random.choice(list(self.board.legal_moves))
     return mutated_sequence

class ChessGUI:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("Chess GUI")
        self.root.geometry("640x640")

        self.board = chess.Board()  # Initialize the chess board using python-chess
        self.squares = [[] for _ in range(8)]
        self.selected_square = None
        self.turn = chess.WHITE
        self.king_in_check_square = None  # Track the square of the king in check
        self.genetic_algorithm = GeneticAlgorithm()  # Initialize the genetic algorithm
        # Load chess piece images into a dictionary
        self.piece_images = {
            piece: ctk.CTkImage(light_image=Image.open(f"{piece}.png"), size=(70, 70))
            for piece in [
                "white_knight", "white_pawn", "black_king", "black_pawn", "black_knight",
                "white_king", "default", "white_rook", "black_rook", "white_bishop",
                "black_bishop", "white_queen", "black_queen"
            ]
        }

        self.root.resizable(False, False)
        self.menu()  # Initialize the chessboard GUI
        self.root.mainloop()

    def menu(self):
        """Create a visually appealing main menu."""
        self.root.geometry("300x350")
        self.root.title("Chess Game")

        # Create the main menu frame and background
        menu_frame = ctk.CTkFrame(self.root, width=300, height=350, fg_color="black")
        menu_frame.pack(fill="both", expand=True)

        canvas = Canvas(menu_frame, width=300, height=350, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.bg_photo = ImageTk.PhotoImage(Image.open("Chess Wallpaper.jpeg"))
        canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Overlay transparent image
        self.overlay_photo = ImageTk.PhotoImage(Image.open("chess.png"))
        canvas.create_image(150, 100, image=self.overlay_photo, anchor="center")

        # Common button styling
        button_style = {
            "width": 100, "height": 50, "font": ("PMingLiU-ExtB", 30),
            "text_color": "white", "fg_color": "#141414", "bg_color": "#141414", "hover_color": "#292927"
        }

        # Add buttons
        ctk.CTkButton(menu_frame, text="Play", command=lambda: [self.board_gui(), menu_frame.destroy()], **button_style) \
            .place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkButton(menu_frame, text="Quit", command=self.root.destroy, **button_style) \
            .place(relx=0.5, rely=0.7, anchor="center")

    def board_gui(self):
        """Create the chessboard and set up pieces."""
        self.root.geometry("640x640")
        board_frame = ctk.CTkFrame(self.root, width=640, height=640)

        # Create the chessboard grid
        for i in range(8):
            for j in range(8):
                fg_color = "white" if (i + j) % 2 == 0 else "gray"

                # Create and configure a square button
                b = ctk.CTkButton(
                    board_frame, text="", width=80, height=80, fg_color=fg_color,
                    border_color="black", border_width=1, corner_radius=0,
                    image=self.piece_images.get(
                        self.get_piece(i, j)),
                    command=lambda row=i, column=j: self.move_piece(row, column),
                )
                b.grid(row=i, column=j)
                self.squares[i].append(b)

        board_frame.pack(fill="both", expand=True)

    def get_piece(self, row, col):
        """Get the piece at the given board position using python-chess."""
        piece = self.board.piece_at(chess.square(col, 7 - row))  # python-chess uses a different coordinate system
        if piece is None:
            return "default"
        piece_map = {
            chess.PAWN: "white_pawn" if piece.color == chess.WHITE else "black_pawn",
            chess.KNIGHT: "white_knight" if piece.color == chess.WHITE else "black_knight",
            chess.BISHOP: "white_bishop" if piece.color == chess.WHITE else "black_bishop",
            chess.ROOK: "white_rook" if piece.color == chess.WHITE else "black_rook",
            chess.QUEEN: "white_queen" if piece.color == chess.WHITE else "black_queen",
            chess.KING: "white_king" if piece.color == chess.WHITE else "black_king",
        }
        return piece_map.get(piece.piece_type, "default")

    def move_piece(self, row, col):
        """Handle a piece movement."""
        if self.selected_square:
            # A square is already selected; move the piece if the move is valid
            selected_row, selected_col = self.selected_square
            from_square = chess.square(selected_col, 7 - selected_row)
            to_square = chess.square(col, 7 - row)
            move = chess.Move(from_square, to_square)
            if move in self.board.legal_moves:  # Check if the move is legal
                self.board.push(move)  # Make the move on the chess board
                self.update_board()  # Update the board GUI
                self.check_king_in_check()  # Highlight the king if it's in check

                # Check for checkmate or stalemate
                if self.board.is_checkmate():
                    self.display_game_over("Checkmate!")
                elif self.board.is_stalemate():
                    self.display_game_over("Stalemate!")
                else:
                    self.switch_turn()  # Switch turns
                    self.make_black_move()  # Make a move for the black player
            self.selected_square = None  # Deselect the square
            self.reset_colors()  # Reset colors but keep the check highlight
        else:
            # Select the clicked square
            self.selected_square = (row, col)
            self.highlight_moves(row, col)  # Highlight possible moves

    def display_game_over(self, message):
        """Display a game-over message and disable the board."""
        # Disable all buttons
        for row in self.squares:
            for button in row:
                button.configure(state="disabled")

        # Create a popup for the game-over message
        popup = ctk.CTkToplevel(self.root)
        popup.title("Game Over")
        popup.geometry("300x150")

        label = ctk.CTkLabel(popup, text=message, font=("Garamond", 16))
        label.pack(pady=20)

        button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        button.pack(pady=10)

    def switch_turn(self):
        """Switch the turn between white and black."""
        self.turn = chess.BLACK if self.turn == chess.WHITE else chess.WHITE

    def check_king_in_check(self):
        """Highlight the king's square if it's in check."""
        if self.board.is_check():
            # Find the king's square based on the current turn
            if self.turn == chess.WHITE:
                turn=chess.BLACK
            else:
                turn=chess.WHITE
            king_square = self.board.king(turn)
            king_row, king_col = divmod(king_square, 8)
            self.king_in_check_square = (7 - king_row, king_col)  # Convert to GUI coordinates
            self.squares[7 - king_row][king_col].configure(fg_color="red")
        else:
            # Clear the check highlight if no longer in check
            self.king_in_check_square = None

    def highlight_moves(self, row, col):
        """Highlight valid moves for the selected piece."""
        self.reset_colors()  # Reset all square colors but retain the check highlight
        selected_piece = self.get_piece(row, col)

        # Only highlight moves for non-empty squares
        if selected_piece == "default":
            return

        piece_square = chess.square(col, 7 - row)
        for move in self.board.legal_moves:
            if move.from_square == piece_square:
                to_square = move.to_square
                to_row, to_col = divmod(to_square, 8)
                destination_piece = self.board.piece_at(to_square)

                # Highlight attackable squares as pink, otherwise green
                if destination_piece and destination_piece.color != self.board.piece_at(piece_square).color:
                    self.squares[7 - to_row][to_col].configure(fg_color="pink")
                else:
                    self.squares[7 - to_row][to_col].configure(fg_color="light green")

    def reset_colors(self):
        """Reset the colors of all squares but retain the check highlight."""
        for i in range(8):
            for j in range(8):
                if self.king_in_check_square == (i, j):
                    # Skip resetting the king's square if it's in check
                    continue
                fg_color = "white" if (i + j) % 2 == 0 else "gray"
                self.squares[i][j].configure(fg_color=fg_color)

    def update_board(self):
        """Update the board GUI with the current pieces."""
        for i in range(8):
            for j in range(8):
                self.squares[i][j].configure(
                    image=self.piece_images.get(self.get_piece(i, j), self.piece_images["default"])
                )
    def make_black_move(self):
        """Use genetic algorithm to make a move for the black player."""
        if self.turn == chess.BLACK:
            best_move = self.genetic_algorithm.genetic_algorithm(self.board)  # Get the best move using GA
            self.board.push(best_move)  # Apply the move
            self.update_board()  # Update the board GUI
            self.check_king_in_check()  # Check if the king is in check
            self.switch_turn()  # Switch to the white player's turn
    GeneticAlgorithm()

ChessGUI()