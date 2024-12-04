import random

class InvalidMoveError(Exception):
    """Exception raised for invalid moves in the game."""
    def __init__(self, message, piece=None, player=None, game=None):
        super().__init__(message)
        self.piece = piece
        self.player = player
        self.game = game
    
    def __str__(self):
        return f"{super().__str__()}"
    
    def restore_piece(self):
        if all([self.piece, self.player, self.game]):
            if self.player == 'player1':
                self.game.p1_sidelines.insert(0, self.piece)
            else:
                self.game.p2_sidelines.insert(0, self.piece)

class InvalidPlayerError(Exception):
    """Exception raised for invalid players in the game."""
    pass

def roll_dice():
    sides = [1, 1, 0, 0]
    num_rolls = 3
    result = 0
    for roll in range(num_rolls):
        throw = random.choice(sides)
        result+= throw
    return result

class GameOfUr:
    def __init__(self):
        # Initialize empty board
        # 0 = empty, 'a'-'g' = player 1, 'A'-'G' = player 2, 'R' = rosette, 3 = blank space
        # self.board = { 
        #     'p1_sidelines': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        #     'p1_finished' : [],
        #     'p1_path': ['R', 0, 0, 0, 3, 3, 'R', 0],  # Player 1's starting path
        #     'shared': [0, 0, 0, 'R', 0, 0, 0, 0],  # Shared middle path
        #     'p2_path': ['R', 0, 0, 0, 3, 3, 'R', 0],  # Player 2's starting path
        #     'p2_sidelines': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        #     'p2_finished' : []        
        # } 
        self.p1_sidelines = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.p1_finished = []
        self.p1_path = ['R', 0, 0, 0, 3, 3, 'R', 0]  # Player 1's starting path
        self.shared = [0, 0, 0, 'R', 0, 0, 0, 0]  # Shared middle path
        self.p2_path = ['R', 0, 0, 0, 3, 3, 'R', 0]  # Player 2's starting path
        self.p2_sidelines = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.p2_finished = []        
        
        self.p1_pieces = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.p2_pieces = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        
        #When TRUE it's player one's turn, when FALSE, it's player two's turn
        self.playerFlag = True

        #When TRUE, player get's an extra turn, when FALSE they do not
        self.rollAgain = False

        #Flag to end gameplay loop
        self.playing = True


        # startIndex = 3
        # end_index = 6
        # first_turn_index = 0
        # second_turn_index = 7
        # rosette_indeces = [0, 3, 6]

    # def board_values(self):
    #      # Get the different sections
    #     p1_sidelines = self.board['p1_sidelines']
    #     p1_finished = self.board['p1_finished']
    #     p1_path = self.board['p1_path']
    #     shared = self.board['shared']
    #     p2_path = self.board['p2_path']
    #     p2_sidelines = self.board['p2_sidelines']
    #     p2_finished = self.board['p2_finished']
        
    #     return p1_sidelines, p1_path, shared, p2_path, p2_sidelines, p1_finished, p2_finished
    
    def display_board(self):
        # Get the different sections
        # self.p1_sidelines, self.p1_path, self.shared, self.p2_path, self.p2_sidelines, self.p1_finished, self.p2_finished = self.board_values()
        
        # Convert board values to display characters
        def convert_to_display(value):
            if value == 0:
                return '□'  # Empty square
            # elif value == 1:
            #     return '①'  # Player 1 piece
            # elif value == 2:
            #     return '②'  # Player 2 piece
            elif value == 3:
                return ' '
            elif value == 'R':
                return '★'  # Rosette
            else:
                return f"{value}"
        
        # Convert sections to display format
        p1_sidelines_display = [convert_to_display(x) for x in self.p1_sidelines]
        p1_path_display = [convert_to_display(x) for x in self.p1_path]
        shared_display = [convert_to_display(x) for x in self.shared]
        p2_path_display = [convert_to_display(x) for x in self.p2_path]
        p2_sidelines_display = [convert_to_display(x) for x in self.p2_sidelines]
        p1_finished_display = [convert_to_display(x) for x in self.p1_finished]
        p2_finished_display = [convert_to_display(x) for x in self.p2_finished]

        
        # Display the board
        print("\n=== The Royal Game of Ur ===\n")
        
        # Print Board
        print("Finished Pieces:", ''.join(p1_finished_display))
        print("        ", ''.join(p1_sidelines_display))
        print("P1 Path:", ' '.join(p1_path_display))
        print("Shared: ", ' '.join(shared_display))
        print("P2 Path:", ' '.join(p2_path_display))
        print("        ", ''.join(p2_sidelines_display))
        print("Finished Pieces:", ''.join(p2_finished_display))

    def return_index_to_default(self, list, index):
        default_p1_path = ['R', 0, 0, 0, 3, 3, 'R', 0]  # Player 1's starting path
        default_shared = [0, 0, 0, 'R', 0, 0, 0, 0]  # Shared middle path
        default_p2_path = ['R', 0, 0, 0, 3, 3, 'R', 0]  # Player 2's starting path
        
        if list == 'p1_path':
            self.p1_path[index] = default_p1_path[index]
        if list == 'p2_path':
            self.p2_path[index] = default_p2_path[index]
        if list == 'shared':
            self.shared[index] = default_shared[index]

            
    
    def move_new_piece_on_to_board(self, playerID, moves):
        if not moves or moves <= 0:
            raise InvalidMoveError("Moves must be greater than 0")
        try:
            if playerID == 'player1':
                if not self.p1_sidelines:
                    raise InvalidMoveError("No pieces available to move onto board")
                new_piece = self.p1_sidelines.pop(0)
                if self.test_if_square_free(playerID, self.p1_path, 4-moves): 
                    self.p1_path[4-moves] = new_piece
                    self.display_board()
                
                #TODO: remove nested new move call 
                if self.p1_path.index(new_piece) == 0:
                    self.rollAgain = True
                    return True
                else:
                    return True
                            
            elif playerID == 'player2':
                if not self.p1_sidelines:
                    raise InvalidMoveError("No pieces available to move onto board")
                new_piece = self.p2_sidelines.pop(0)
                if self.test_if_square_free(playerID, self.p2_path, 4-moves): 
                    self.p2_path[4-moves] = new_piece
                    self.display_board()
                #TODO: remove nested new move call 
                if self.p2_path.index(new_piece) == 0:
                    self.rollAgain = True
                    return True
                else:
                    return True     
            else:
                raise InvalidMoveError("Not a valid player")
        except InvalidMoveError as e:
            print(f"Invalid move: {str(e)}")
            raise InvalidMoveError(str(e), new_piece, playerID, self) from e
        
    
    def move_piece(self, playerID, piece, moves):
        position = 0
        try:
            if playerID == 'player1':
                if piece in self.p1_path:
                    position = self.p1_path.index(piece)
                    new_position = position - moves
                    
                    if new_position < 0:
                        index = abs(new_position+1)
                        if self.test_if_square_free(playerID, self.shared, index):
                            # MOVE ONTO SHARED
                            self.shared[index] = piece
                            self.return_index_to_default('p1_path', position)
                            self.display_board()

                    elif position == 6 and moves >= 1:
                        # MOVE OFF BOARD
                        self.p1_finished.append(piece)
                        self.return_index_to_default('p1_path', position)
                        self.display_board()  

                    elif new_position in [3, 4, 5]:
                        # MOVE OFF BOARD
                        self.p1_finished.append(piece)
                        self.return_index_to_default('p1_path', position)
                        self.display_board()
                    
                    else:
                        if self.test_if_square_free(playerID, self.p1_path, new_position):
                            self.p1_path[new_position] = piece
                            self.return_index_to_default('p1_path', position)
                            self.display_board()
                    
                    if piece in self.p1_path and self.p1_path.index(piece) in [0, 6]:
                        self.rollAgain = True 
                        return True
                    else:
                        return True
                
                elif piece in self.shared:
                    position = self.shared.index(piece)
                    new_position = position + moves
                    
                    if new_position > 7:
                        p1_path_moves = new_position - 7
                        p1_position = len(self.p1_path) - p1_path_moves

                        if p1_position < 0:
                            raise InvalidMoveError("Move would place piece beyond the board")
                        
                        if p1_position == 7:
                            if self.test_if_square_free(playerID, self.shared, p1_position):
                                self.p1_path[p1_position] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                
                        elif p1_position == 6:
                            if self.test_if_square_free(playerID, self.shared, p1_position):
                                self.p1_path[p1_position] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                                self.rollAgain = True 
            
                        elif p1_position < 6:
                            self.p1_finished.append(piece)
                            self.return_index_to_default('shared', position)
                            self.display_board()
                    
                    else:
                        if self.test_if_square_free(playerID, self.shared, new_position):
                            self.shared[new_position] = piece
                            self.return_index_to_default('shared', position)
                            self.display_board()
                       
                    if self.shared.index(piece) == 3:
                        self.rollAgain = True
                        return True 
                    else:
                        return True

            if playerID == 'player2':
                if piece in self.p2_path:
                    position = self.p2_path.index(piece)
                    new_position = position - moves
                    
                    if new_position < 0:
                        index = abs(new_position+1)
                        if self.test_if_square_free(playerID, self.shared, index):
                            # MOVE ONTO SHARED
                            self.shared[index] = piece
                            self.return_index_to_default('p2_path', position)
                            self.display_board()
                    elif position == 6 and moves >= 1:
                        # MOVE OFF BOARD
                        self.p2_finished.append(piece)
                        self.return_index_to_default('p2_path', position)
                        self.display_board()  
                    elif new_position in [3, 4, 5]:
                        # MOVE OFF BOARD
                        self.p2_finished.append(piece)
                        self.return_index_to_default('p2_path', position)
                        self.display_board()
                    
                    else:
                        if self.test_if_square_free(playerID, self.p2_path, new_position):
                            self.p2_path[new_position] = piece
                            self.return_index_to_default('p2_path', position)
                            self.display_board()
                            
                    
                    if piece in self.p2_path and self.p2_path.index(piece) in [0, 6]:
                        self.rollAgain = True
                        return True 
                    else:
                        return True
                
                elif piece in self.shared:
                    position = self.shared.index(piece)
                    new_position = position + moves
                    
                    if new_position > 7:
                        p2_path_moves = new_position - 7
                        p2_position = len(self.p2_path) - p2_path_moves

                        if p2_position < 0:
                            raise InvalidMoveError("Move would place piece beyond the board")
                        
                        if p2_position == 7:
                            if self.test_if_square_free(playerID, self.shared, p2_position):
                                self.p2_path[p2_position] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                
                        elif p2_position == 6:
                            if self.test_if_square_free(playerID, self.shared, p2_position):
                                self.p2_path[p2_position] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                                self.rollAgain = True 
            
                        elif p2_position < 6:
                            self.p2_finished.append(piece)
                            self.return_index_to_default('shared', position)
                            self.display_board()
                    
                    else:
                        if self.test_if_square_free(playerID, self.shared, new_position):
                            self.shared[new_position] = piece
                            self.return_index_to_default('shared', position)
                            self.display_board()
                       
                        if self.shared.index(piece) == 3:
                            self.rollAgain = True
                            return True
                        else:
                            return True 
        
        except InvalidMoveError as e:
            raise InvalidMoveError(str(e), piece=piece, player=playerID, game=self) from e
                


    def test_if_square_free(self, playerID, list, index):
        if index < 0 or index >= len(list):
            return InvalidMoveError(f"Move position is outside of valid range")

        if playerID == 'player1':
            if list[index] in self.p1_pieces:
                raise InvalidMoveError(f"Invalid move: {list[index]} at target square.")
            elif list[index] in self.p2_pieces:
                print(f"Captured opponent's piece {list[index]}")
                self.p2_sidelines.append(list[index])
                return True
            elif list == self.shared and index == 3:
                if self.shared[3] in self.p2_pieces:
                    raise InvalidMoveError("You cannot capture an opponent's piece when it is on a Rosette")
                elif self.shared[3] in self.p1_pieces:
                    raise InvalidMoveError(f"Invalid move: {list[index]} at target square.")
                else:
                    return True
            else:
                return True
        if playerID == 'player2':
            if list[index] in self.p2_pieces:
                raise InvalidMoveError(f"Invalid move: {list[index]} at target square.")
            elif list[index] in self.p1_pieces:
                print(f"Captured opponent's piece {list[index]}")
                self.p1_sidelines.append(list[index])
                return True
            elif list == self.shared and index == 3:
                if self.shared[3] in self.p1_pieces:
                    raise InvalidMoveError("You cannot capture an opponent's piece when it is on a Rosette")
                elif self.shared[3] in self.p2_pieces:
                    raise InvalidMoveError(f"Invalid move: {list[index]} at target square.")
                else:
                    return True
            else:
                return True


    def get_player_input(self, prompt="Enter your choice: "):
        """Get player input and check for quit command"""
        response = input(prompt).strip()
        if response == 'q':
            raise SystemExit
        return response

    def new_move(self, playerID):

        dice_roll = roll_dice()
        remaining_moves = dice_roll
        print(f"{playerID} rolled: {dice_roll}")
        if remaining_moves == 0:
            self.playerFlag = not self.playerFlag
        else:    
            while remaining_moves > 0:
                try:
                    piece = self.get_player_input(f"{playerID} has {remaining_moves} moves remaining. Enter q to quit game.\nWhich piece do you want to move? \n(enter letter to choose piece from board or 1 to add a new piece to the board): ")
                    if piece != '1':
                        if playerID == 'player1' and piece not in self.p1_pieces:
                            print("Piece must belong to Player 1")
                            continue
                        if playerID == 'player2' and piece not in self.p2_pieces:
                            print("Piece must belong to Player 2")
                            continue  
                        if piece in self.p1_finished or piece in self.p2_finished:
                            print("Piece has finished game, please choose a piece still in play")             
                    # TODO: Add handling for if the piece they enter is invalid to catch this before entering the for loop below
                    moves = int(self.get_player_input(f"How many spaces do you want to move {piece}?\nEnter q to quit game: "))
                    if moves <= 0:  
                        print("Moves must be greater than 0")
                        continue
                        # while moves <= 0:
                        #     moves = int(input("Moves cannot be 0 or negative. Please try again with a larger value:"))
                    if moves > remaining_moves:
                        print(f"{moves} is greater than {remaining_moves} remaining moves")
                        continue
                    
                    if piece == '1':
                        try:
                            success = self.move_new_piece_on_to_board(playerID, moves)
                        except InvalidMoveError as e:
                            print(f"Invalid move: {str(e)}")
                            e.restore_piece()
                            continue
                    else:
                        try:
                            success = self.move_piece(playerID, piece, moves)
                        except InvalidMoveError as e:
                            print(f"Invalid move: {str(e)}")
                            continue
                    
                    if success:
                        remaining_moves = remaining_moves - moves
                    
                    if self.rollAgain:
                        self.rollAgain = False
                        self.new_move(playerID)

                    else:
                        self.playerFlag = not self.playerFlag

            # except ValueError as e:
            #     print(f"Value error:{e} ")
                except KeyboardInterrupt:
                    print("\nGame interrupted by user (Ctrl+C)")
                except Exception as e:
                    print(f"\nUnexpected error: {e}")
            

def abstracted_moves(self, playerID, piece, moves, playerPath, playerPathString, playerFinished):
    try:
        if piece in playerPath:
            position = playerPath.index(piece)
            new_position = position - moves
            
            if new_position < 0:
                index = abs(new_position+1)
                if self.test_if_square_free(playerID, self.shared, index):
                    # MOVE ONTO SHARED
                    self.shared[index] = piece
                    self.return_index_to_default(playerPathString, position)
                    self.display_board()
            elif position == 6 and moves >= 1:
                # MOVE OFF BOARD
                self.playerFinished.append(piece)
                self.return_index_to_default(playerPathString, position)
                self.display_board()  
            elif new_position in [3, 4, 5]:
                # MOVE OFF BOARD
                self.playerFinished.append(piece)
                self.return_index_to_default(playerPathString, position)
                self.display_board()
            
            else:
                if self.test_if_square_free(playerID, playerPath, new_position):
                    self.playerPath[new_position] = piece
                    self.return_index_to_default(playerPathString, position)
                    self.display_board()
            
            if self.p1_path.index(piece) in [0, 6]:
                self.rollAgain = True
        
        elif piece in self.shared:
            position = self.shared.index(piece)
            new_position = position + moves
            
            if new_position > 7:
                p1_path_moves = new_position - 7
                p1_position = len(playerPath) - p1_path_moves

                if p1_position < 0:
                    raise InvalidMoveError("Move would place piece beyond the board")
                
                if p1_position == 7:
                    if self.test_if_square_free(playerID, self.shared, p1_position):
                        playerPath[p1_position] = piece
                        self.return_index_to_default('shared', position)
                        self.display_board()
        
                elif p1_position == 6:
                    if self.test_if_square_free(playerID, self.shared, p1_position):
                        playerPath[p1_position] = piece
                        self.return_index_to_default('shared', position)
                        self.display_board()
                        self.rollAgain = True
    
                elif p1_position < 6:
                    self.playerFinished.append(piece)
                    self.return_index_to_default('shared', position)
                    self.display_board()
            
            else:
                if self.test_if_square_free(playerID, self.shared, new_position):
                    self.shared[new_position] = piece
                    self.return_index_to_default('shared', position)
                    self.display_board()
            
                    if self.shared.index(piece) == 3:
                        self.rollAgain = True
    except InvalidMoveError as e:
        raise InvalidMoveError(str(e), piece=piece, player=playerID, game=self) from e
        

def main():
    # game.playing = True
    game = GameOfUr()
    game.display_board()

    while True:
        try:
            if game.playerFlag == True:
                game.new_move("player1") 
            else:
                game.new_move("player2")
            if len(game.p1_finished) == 6:
                print("Congratulations! Player 1 has won the game")
                return False
            if len(game.p2_finished) == 6:
                print("Congratulations! Player 2 has won the game")
                return False
        except ValueError:
            print("Please enter a valid input or q to quit")

            

if __name__ == "__main__":
    main()