from sklearn.cluster import KMeans # Used for detecting likely columns
import numpy as np # Used for creating array for sklearn

"""
Team 19
Artifact: board.py
Purpose: For using the board and performing operations on it
Created: 3/17/25
Revised: 4/16/25
Preconditions: Ro-board is set up to have taken a picture from the board and a string has been made that represents the board
Postconditions: Ro-board knows if a win has occurred
Errors: None
Side Effects: None
Invariants: None
Faults: None
"""
NEW_ROW_BOUND = 12 # Jumps to rows are indicated by a difference of 10 or more in the y-value
NEXT_COL_BOUND = 40 # Jumps to columns are indicated by a difference of 100 or more in the x-value
RED = '1'
YELLOW = '2'

class Board:
    
    """
    Board based on indices of "board" :
    0  1  2  3  4  5  6
    7  8  9  10 11 12 13
    14 15 16 17 18 19 20
    21 22 23 24 25 26 27
    28 29 30 31 32 33 34
    35 36 37 38 39 40 41

    board is a string of 42 characters, representing the 6x7 board
    The spaces go from left to right, top to bottom (first 7 characters are the top row, next 7 are the second to top row, etc.)
    A 0 is an empty space, a 1 is a red space, and a 2 is a yellow space

    The strategy used to efficiently search the board is this:
      If there are four consecutive pieces in a column (vertical), they must always occupy the middle 2 rows. So, we need only check adjacent pieces of the piece that occupies the 2nd row (using 0-based indexing) to find a potential win
      Next, if there are four consecutive pieces in a row (horizontal) or on a diagonal, they must always occupy the middle column. So, we need only check adjacent pieces of the pieces that occupy the 3rd column (0-based) to find a potential win
      (By adjacent, I am referencing the 8 potential spaces around a space)
    """

    # Initialize board class
    def __init__(self, pieces):
        self.board = self.build(pieces) # Construct board with pieces

    def build(self, pieces):
        # Remove unneeded information
        updated_pieces = [] # Keep track of new pieces
        for piece in pieces:
            # Find middle of the bounding box for more accurate representation
            upd_piece = dict() # Empty piece
            upd_piece['x'] = piece['x'] + (piece['width'] / 2) # Find x-coord of middle
            upd_piece['y'] = piece['y'] + (piece['height'] / 2) # Find y-coord of middle
            upd_piece['class'] = piece['class'] # Keep class
            updated_pieces.append(upd_piece) # Add updated piece to update pieces

        # Construct board from the pieces from the model with updated values
        sorted_pieces = sorted(updated_pieces, key=lambda p: p['y'], reverse=False) #sort pieces by y value
        # print(f"sorted pieces {sorted_pieces}")
        grouped_data = [] # Stores all pieces sorted by row
        prev_y = 0 # Keeps track of the previous y value
        curr_row = [] # Keeps track of current row
        for piece in sorted_pieces: # Loop through all the pieces
            if len(curr_row) < 7 and (prev_y == 0 or (abs(prev_y - piece['y']) < NEW_ROW_BOUND)): # Add to the row if difference of y is small
                curr_row.append(piece) # Add piece to current row
            else:
                grouped_data.append(curr_row) # Add row to grouped
                curr_row = [] # Clear row
                curr_row.append(piece)
            prev_y = piece['y'] # Update previous y

        grouped_data.append(curr_row) # Add last row to board
        # print(f"grouped data: {grouped_data}")

        fully_sorted = [] #init sorted array
        for group in grouped_data: #now put groups in sorted array
            sorted_group = sorted(group, key=lambda d: d['x'], reverse=False) #sort individual group
            fully_sorted.append(sorted_group) #add to array

        # Remove duplicates from each row
        no_duplicates = self._remove_duplicates(fully_sorted) 

        board = "" #init board
        for row in no_duplicates: #now go through sorted array and change into enums
            for column in row: #go through each column and change into enums
                piece = column['class'] #get current piece
                if piece == 'red': #if is in red class
                    board += RED #add enum RED to board
                elif piece == 'yellow': #if in yellow class
                    board += YELLOW #add enum YELLOW to board
                else: # piece == 'empty':
                    board += '0' #add enum empty to board

        # Add pieces that are not detected
        print(board)
        print(len(board))
        full_board = self._fill_pieces(no_duplicates, board)

        return full_board

    # Takes the board object and "fixes" it
    # Fixing it means removing extra length (> 42 pieces in the board)
    # and filling in gaps (< 42 pieces in the board)
    def _fill_pieces(self, pieces, board):
        xs = [] # Group for all x values
        num_reds = 0 # Count the number of yellows in the board
        num_yellows = 0 # Count the number of reds in the board
        for row in pieces: # Loop through every row
            for piece in row: # Loop through every piece
                xs.append(piece['x']) # Add x to xs
                if piece['class'] == 'red': # If piece of red
                    num_reds += 1 # Add one to number of reds
                elif piece['class'] == 'yellow': # If piece is yellow
                    num_yellows += 1 # Add one to number of yellows 

        xs_arr = np.array(xs).reshape(-1, 1) # Convert to 2D array
        col_means = KMeans(n_clusters=7, random_state=0).fit(xs_arr) # Find means of column x values
        col_sorted = sorted(col_means.cluster_centers_.flatten())
        # print("Column centers: ", col_sorted)

        # Find missing pieces and add 0's in their place
        missing_pieces = [] # Keeps track of the pieces that are missing (their index in board)
        for i, row in enumerate(pieces):
            print(f"{i}: {len(row)}")
            if len(row) < 7: # Only look at rows well fewer than 7 pieces
                assignments = [None] * 7  # 7 columns
                for piece in row: # Loop through row of xs
                    # Find closest column center
                    x = piece['x']
                    dists = [abs(x - c) for c in col_sorted] # Find distances to all columns
                    col = dists.index(min(dists)) # Get column that this x value is closest to

                    if assignments[col] is not None: # If piece already assigned to column
                        unassigned = -1 # Try to find a column to the left that is unassigned
                        for col_check in range(col, -1, -1): # Loop backwards through columns
                            if assignments[col_check] is None: # Check if unassigned
                                unassigned = col_check # Reassign unassigned
                                break # End search
                        if unassigned == -1: # Found no None
                            for col_check in range(col, 8): # Search forward
                                if assignments[col_check] is None: # Check if unassigned
                                    assignments[col_check] = x # Assign col
                                    break # End search
                        else: # Found a None
                            for col_swap in range(unassigned, col): # Shift assigned down 1
                                assignments[col_swap] = assignments[col_swap + 1] # Shift col over

                            assignments[col] = x # Update column of row with the value

                    else: # Nothing assigned
                        assignments[col] = x # Update column of row with the value

                for j in range(len(assignments)):
                    if assignments[j] == None:
                        missing_pieces.append((7*i)+j)  
        
        missing_pieces = sorted(missing_pieces, reverse=True) # Reverse the missing pieces 
        print(missing_pieces)
        board_list = list(board)
        for piece in missing_pieces: # Loop through missing pieces
            if num_yellows <= num_reds: # Equal number of each color or less yellows 
                if piece <= 34 and board_list[piece + 7] != '0': # If piece below is not empty
                    board_list.insert(piece, YELLOW) # Yellow is missing and might go here
                    num_yellows += 1 # Add 1 to num of yellow
            elif num_yellows > num_reds + 1: # Too many yellows compared to reds
                if piece <= 34 and board_list[piece + 7] != '0': # If piece below is not empty
                    board_list.insert(piece, RED) # Red is missing and might go here
                    num_reds += 1 # Add 1 to num of reds
            else:
                board_list.insert(piece, '0') # Piece is most likely empty
    
        board_list = "".join(board_list)
        return board_list 

    # Remove all duplicates from a row
    def _remove_duplicates(self, pieces):
        new_board = [] # Keep track of the new board
        for row in pieces: # Loop through every row
            new_row = [] # Keep track of the new row 
            for i in range(len(row)): # Loop through row
                if i < len(row) - 1 and abs(row[i + 1]['x'] - row[i]['x']) < NEXT_COL_BOUND: # Check next piece
                    continue # Dont add to updated row 
                new_row.append(row[i]) # Add piece to updated row
            new_board.append(new_row)
        return new_board # Return new board
    
    # Print the board to stdout
    def print(self):
        print(f"Board: {self.board}")
        print(f"Length: {len(self.board)}")

    """ 
    Finds consecutive pieces in the column
    @param piece: The piece that we are looking for
    @param ind: The initial index of the piece
    @ret: The number of consecutive pieces
    """
    def look_vertical(self, piece, ind) -> int:
        connected = 0
        
        # Look up to find pieces
        curr = ind
        while curr >= 7 and self.board[curr - 7] == piece: # Prevent out of bounds error and then check the space above
            connected += 1 # Increase count of connected when a piece is found
            curr -= 7 # Move one space up

        # Look down to find pieces
        curr = ind
        while curr <= 34 and self.board[curr + 7] == piece: # Prevent out of bounds error and then check the space below
            connected += 1 # Increase count of connected when a piece is found
            curr += 7 # Move one space down

        return connected # Return amount of consecutive pieces from looking up and down

    """ 
    Finds consecutive pieces in the row
    @param piece: The piece that we are looking for
    @param ind: The initial index of the piece
    @ret: The number of consecutive pieces
    """
    def look_horizontal(self, piece, ind) -> int:
        connected = 0
        
        # Look left to find pieces
        curr = ind #
        while curr % 7 >= 1 and self.board[curr - 1] == piece: # Prevent out of bounds error and then check the space to the left
            connected += 1 # Increase count of connected when a piece is found
            curr -= 1 # Move one space left

        # Look right
        curr = ind
        while curr % 7 <= 5 and self.board[curr + 1] == piece: # Prevent out of bounds error and then check the space to the right
            connected += 1 # Increase count of connected when a piece is found
            curr += 1 # Move one space right

        return connected # Return amount of consecutive pieces from looking left and right

    """ 
    Finds consecutive pieces in the positive diagonal (i.e. on the line y = x where ind is the origin)
    @param piece: The piece that we are looking for
    @param ind: The initial index of the piece
    @ret: The number of consecutive pieces
    """
    def look_pos_diag(self, piece, ind) -> int:
        connected = 0
        
        # Look up and right to find pieces
        curr = ind
        while (curr >= 7 and curr % 7 <= 5) and self.board[curr - 6] == piece: # Prevent out of bounds error and then check the space to the upper right
            connected += 1 # Increase count of connected when a piece is found
            curr -= 6 # Move one space up and right

        # Look down and left to find pieces 
        curr = ind
        while (curr <= 34 and curr % 7 >= 1) and self.board[curr + 6] == piece: # Prevent out of bounds error and then check the space to the lower left
            connected += 1 # Increase count of connected when a piece is found
            curr += 6 # Move one space down and left

        return connected # Return amount of consecutive pieces from looking up/right and down/left

    """ 
    Finds consecutive pieces in the negative diagonal (i.e. on the line y = -x where ind is the origin) 
    @param piece: The piece that we are looking for
    @param ind: The initial index of the piece
    @ret: The number of consecutive pieces
    """
    def look_neg_diag(self, piece, ind) -> int :
        connected = 0
        
        # Look up and left to find pieces
        curr = ind
        while (curr >= 7 and curr % 7 >= 1) and self.board[curr - 8] == piece: # Prevent out of bounds error and then check the space to the upper left
            connected += 1 # Increase count of connected when a piece is found
            curr -= 8 # Move one space up and left

        # Look down and right to find pieces
        curr = ind 
        while (curr <= 34 and curr % 7 <= 5) and self.board[curr + 8] == piece: # Prevent out of bounds error and then check the space to the lower right
            connected += 1 # Increase count of connected when a piece is found
            curr += 8 #  Move one space down and right

        return connected  # Return amount of consecutive pieces from looking up/left and down/right

    """
    Checks if a win exists within the board
    @ret: The integer representing the state
            - 0 if no win present
            - 1 if red has won
            - 2 is yellow has won
            - 3 if board full and no win
    """
    def win_exists(self) -> int:
        if self.board == None: # Check if the board is not set
            return 0 # No win if their is no board
    
        # Check all columns by searching the 2nd row and looking up and down for consecutive pieces
        for i in range(14, 21):
            
            # First, check if the space is occupied
            if self.board[i] == '0':
                continue
            
            # Get count of consecutive pieces above and below
            connected = 1 + self.look_vertical(self.board[i], i)
            if (connected >= 4): # Report winner if 4 of more connected pieces
                return int(self.board[i])
    
        # Check for horizontal and diagonal wins by checking each piece in the middle column
        for i in range(3, 39, 7):

            # FIrst check if the space is occupied
            if self.board[i] == '0': # No piece, so there won't be a winner
                continue

            # Get count of consecutive pieces left and right
            connected = 1 + self.look_horizontal(self.board[i], i)
            if (connected >= 4): # Report winner if 4 of more connected pieces
                return int(self.board[i])

            # Get count of consecutive pieces on the positive diagonal
            connected = 1 + self.look_pos_diag(self.board[i], i)
            if (connected >= 4): # Report winner if 4 of more connected pieces
                return int(self.board[i])

            # Get count of consecutive pieces on the negative diagonal
            connected = 1 + self.look_neg_diag(self.board[i], i)
            if (connected >= 4): # Report winner if 4 of more connected pieces
                return int(self.board[i])


        # No 4 consecutive pieces on the board, so check for tie
        if '0' not in self.board:
            return 3    
        return 0 # Just return no win

    def make_move(self, column):
        # Loop backwards through column until an empty space is shown
        for i in range(0, 6, -1):
            if self.board[i*7 + column] == 0:
                self.board[i*7 + column] = RED
                break
    
