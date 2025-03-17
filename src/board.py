"""
Team 19
Artifact: board.py
Purpose: For using the board and performing operations on it
Created: 3/17/25
Revised: 3/17/25
Preconditions: Ro-board is set up to have taken a picture from the board and a string has been made that represents the board
Postconditions: Ro-board knows if a win has occurred
Errors: None
Side Effects: None
Invariants: None
Faults: None
"""
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
    def __init__(self, board=None):
        self.board = board

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

        # No 4 consecutive pieces on the board, so report no win
        return 0
