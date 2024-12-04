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

        self.rules = "\n=== The Royal Game of Ur ===\n\nRULES\n1. You cannot split your moves between pieces\n2. You remove an opponent's piece by landing on it\n3. You cannot land on your own piece\n4. If you land on a rosette you must roll again\n5. The first person to get all their pieces off the board wins\n6. You can only exit on an exact throw\n\n=== ENTER q TO QUIT ===\n=== ENTER s TO SKIP TURN ===\n "
        
        # Initialize empty board
        # 0 = empty square, 'a'-'g' = player 1, 'A'-'G' = player 2, 'R' = rosette, 3 = blank space
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
    
    def display_board(self):
        # Convert board values to display characters
        def convert_to_display(value):
            if value == 0:
                return '□'  # Empty square
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

                    elif position == 6 and moves == 1:
                        # MOVE OFF BOARD
                        #TODO: RULE NEEDED: player can only remove piece from board if they have the exact number of moves required to do so
                        self.p1_finished.append(piece)
                        self.return_index_to_default('p1_path', position)
                        self.display_board()  

                    elif new_position == 5:
                        # MOVE OFF BOARD
                        #TODO: RULE NEEDED: player can only remove piece from board if they have the exact number of moves required to do so
                        self.p1_finished.append(piece)
                        self.return_index_to_default('p1_path', position)
                        self.display_board()

                    elif new_position in [3, 4]:
                        raise InvalidMoveError("You must move past the exact number of remaining squares to leave the board")
                    
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
                        
                        if p1_position == 7:
                            if self.test_if_square_free(playerID, self.p1_path, p1_position):
                                self.p1_path[p1_position] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                
                        elif p1_position == 6:
                            if self.test_if_square_free(playerID, self.p1_path, p1_position):
                                self.p1_path[p1_position] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                                self.rollAgain = True 
                        
                        elif p1_position == 5:
                            self.p1_finished.append(piece)
                            self.return_index_to_default('shared', position)
                            self.display_board()
                        
                        elif p1_position in [3, 4]:
                            raise InvalidMoveError("You must move past the exact number of remaining squares to leave the board")
                    
                    else:
                        if self.test_if_square_free(playerID, self.shared, new_position):
                            self.shared[new_position] = piece
                            self.return_index_to_default('shared', position)
                            if new_position == 3:
                                self.rollAgain = True
                            self.display_board()


            elif playerID == 'player2':
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
                    
                    elif position == 6 and moves == 1:
                        # MOVE OFF BOARD
                        self.p2_finished.append(piece)
                        self.return_index_to_default('p2_path', position)
                        self.display_board()  
                    
                    elif new_position == 5:
                        # MOVE OFF BOARD
                        self.p2_finished.append(piece)
                        self.return_index_to_default('p2_path', position)
                        self.display_board()
                    
                    elif new_position in [3, 4]:
                        raise InvalidMoveError("You must move past the exact number of remaining squares to leave the board")
                    
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
                            if self.test_if_square_free(playerID, self.p2_path, p2_position):
                                self.p2_path[7] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                
                        elif p2_position == 6:
                            if self.test_if_square_free(playerID, self.p2_path, p2_position):
                                self.p2_path[6] = piece
                                self.return_index_to_default('shared', position)
                                self.display_board()
                                self.rollAgain = True 
            
                        elif p2_position == 5:
                            self.p2_finished.append(piece)
                            self.return_index_to_default('shared', position)
                            self.display_board()

                        elif p2_position in [3, 4]:
                            raise InvalidMoveError("You must move past the exact number of remaining squares to leave the board")
                    
                    else:
                        if self.test_if_square_free(playerID, self.shared, new_position):
                            self.shared[new_position] = piece
                            self.return_index_to_default('shared', position)
                            if new_position == 3:
                                self.rollAgain = True
                            self.display_board()
            return True
        
        except InvalidMoveError as e:
            raise InvalidMoveError(str(e), piece=piece, player=playerID, game=self) from e
                

    def test_if_square_free(self, playerID, list, index):
        if index < 0 or index >= len(list):
            return InvalidMoveError(f"Move position is outside of valid range")

        if playerID == 'player1':
            if list[index] in self.p1_pieces:
                raise InvalidMoveError(f"Invalid move: {list[index]} at target square.")
            elif list == self.shared and index == 3:
                if self.shared[3] in self.p2_pieces:
                    raise InvalidMoveError("You cannot capture an opponent's piece when it is on a Rosette")
                else:
                    return True
            elif list[index] in self.p2_pieces:
                print(f"Captured opponent's piece {list[index]}")
                self.p2_sidelines.append(list[index])
                return True
            else:
                return True
        if playerID == 'player2':
            if list[index] in self.p2_pieces:
                raise InvalidMoveError(f"Invalid move: {list[index]} at target square.")
            elif list == self.shared and index == 3:
                if self.shared[3] in self.p1_pieces:
                    raise InvalidMoveError("You cannot capture an opponent's piece when it is on a Rosette")
                else:
                    return True
            elif list[index] in self.p1_pieces:
                print(f"Captured opponent's piece {list[index]}")
                self.p1_sidelines.append(list[index])
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
        moves = dice_roll
        print(f"{playerID} rolled: {dice_roll}")
        if moves == 0:
            print(f"Skipping {playerID}'s turn")
            self.playerFlag = not self.playerFlag
        else:    
            while moves > 0:
                try:
                    # piece = self.get_player_input(f"{playerID} has {remaining_moves} moves remaining.\nEnter letter to choose piece from board or 1 to add a new piece to the board: ")
                    piece = self.get_player_input(f"{playerID} - Enter letter to choose piece from board OR 1 to add a new piece to the board: ")

                    if piece == 's':
                        break
                    
                    if piece != '1':
                        if playerID == 'player1' and piece not in self.p1_pieces:
                            print("Piece must belong to Player 1")
                            continue
                        if playerID == 'player2' and piece not in self.p2_pieces:
                            print("Piece must belong to Player 2")
                            continue  
                        if piece in self.p1_finished or piece in self.p2_finished:
                            print("Piece has finished game, please choose a piece still in play")             
                    
                    # if piece == '1':
                    #     moves = int(self.get_player_input(f"How many spaces do you want to move the new piece?:"))
                    
                    # else:
                    #     moves = int(self.get_player_input(f"How many spaces do you want to move {piece}?: "))
                    
                    if piece == 's':
                        break

                    # if moves <= 0:  
                    #     print("Moves must be greater than 0")
                    #     continue

                    # if moves > remaining_moves:
                    #     print(f"{moves} is greater than {remaining_moves} remaining moves")
                    #     continue
                    
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
                        moves = moves - moves
               
                except ValueError as e:
                    print(f"Value error:{e} ")
                except KeyboardInterrupt:
                    print("\nGame interrupted by user (Ctrl+C)")
                except Exception as e:
                    print(f"\nUnexpected error: {e}")
                 
            if self.rollAgain:
                    self.rollAgain = False
                    self.new_move(playerID)

            else:
                self.playerFlag = not self.playerFlag
            

def main():
    # game.playing = True
    game = GameOfUr()
    print(game.rules)
    game.display_board()

    while True:
        try:
            if game.playerFlag == True:
                game.new_move("player1") 
            else:
                game.new_move("player2")
            if len(game.p1_finished) == 7:
                print("Congratulations! Player 1 has won the game")
                return False
            if len(game.p2_finished) == 7:
                print("Congratulations! Player 2 has won the game")
                return False
        except ValueError:
            print("Please enter a valid input or q to quit")
        

if __name__ == "__main__":
    main()