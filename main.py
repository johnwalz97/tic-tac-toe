import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

BOARD_SIZE = 350
PIECE_SIZE = 75

x = 'x'
o = 'o'
x_img = pygame.transform.scale(pygame.image.load('assets/x.png'), (PIECE_SIZE, PIECE_SIZE))
o_img = pygame.transform.scale(pygame.image.load('assets/o.png'), (PIECE_SIZE, PIECE_SIZE))

white = pygame.color.Color('white')
black = pygame.color.Color('black')
red = pygame.color.Color('red')


class Board:
    line_width = 5
    win = None

    def __init__(self, size):
        self.size = size
        self.surface = pygame.Surface((size, size))

        offset = (PIECE_SIZE // 2)
        beg = (int(size * .3333) // 2) - offset
        mid = (size // 2) - offset
        end = ((size // 2) + ((int(size * .3333) // 2) * 2)) - offset

        self.state = [
            [{'pos': (beg, beg), 'piece': None}, {'pos': (mid, beg), 'piece': None}, {'pos': (end, beg), 'piece': None}],
            [{'pos': (beg, mid), 'piece': None}, {'pos': (mid, mid), 'piece': None}, {'pos': (end, mid), 'piece': None}],
            [{'pos': (beg, end), 'piece': None}, {'pos': (mid, end), 'piece': None}, {'pos': (end, end), 'piece': None}],
        ]

    def check_win(self, piece):
        beg = (int(self.size * .3333) // 2)
        mid = (self.size // 2)
        end = ((self.size // 2) + ((int(self.size * .3333) // 2) * 2))

        if piece == self.state[0][0]['piece'] == self.state[0][1]['piece'] == self.state[0][2]['piece']:
            self.win = [(0, beg), (self.size, beg)]
        elif piece == self.state[1][0]['piece'] == self.state[1][1]['piece'] == self.state[1][2]['piece']:
            self.win = [(0, mid), (self.size, mid)]
        elif piece == self.state[2][0]['piece'] == self.state[2][1]['piece'] == self.state[2][2]['piece']:
            self.win = [(0, end), (self.size, end)]
        elif piece == self.state[0][0]['piece'] == self.state[1][0]['piece'] == self.state[2][0]['piece']:
            self.win = [(beg, 0), (beg, self.size)]
        elif piece == self.state[0][1]['piece'] == self.state[1][1]['piece'] == self.state[2][1]['piece']:
            self.win = [(mid, 0), (mid, self.size)]
        elif piece == self.state[0][2]['piece'] == self.state[1][2]['piece'] == self.state[2][2]['piece']:
            self.win = [(end, 0), (end, self.size)]
        elif piece == self.state[0][0]['piece'] == self.state[1][1]['piece'] == self.state[2][2]['piece']:
            self.win = [(0, 0), (self.size, self.size)]
        elif piece == self.state[0][2]['piece'] == self.state[1][1]['piece'] == self.state[2][0]['piece']:
            self.win = [(0, self.size), (self.size, 0)]

        return self.win

    def mark(self, pos, piece):
        x_coord = pos[0] - x_offset
        y_coord = pos[1] - y_offset
        if 0 < x_coord < self.size and 0 < y_coord < self.size:
            col = 0 if x_coord < int(self.size * .33) else 1 if x_coord < int(self.size * .66) else 2
            row = 0 if y_coord < int(self.size * .33) else 1 if y_coord < int(self.size * .66) else 2
            if not self.state[row][col]['piece']:
                self.state[row][col]['piece'] = piece
                return True
        return False

    def _draw_frame(self):
        one_third_board = int(self.size * .33)
        two_third_board = int(self.size * .66)

        pygame.draw.line(self.surface, black, (one_third_board, 0), (one_third_board, self.size), self.line_width)
        pygame.draw.line(self.surface, black, (two_third_board, 0), (two_third_board, self.size), self.line_width)
        pygame.draw.line(self.surface, black, (0, one_third_board), (self.size, one_third_board), self.line_width)
        pygame.draw.line(self.surface, black, (0, two_third_board), (self.size, two_third_board), self.line_width)

    def _draw_pieces(self):
        for row in self.state:
            for cell in row:
                if cell['piece'] == x:
                    self.surface.blit(x_img, cell['pos'])
                elif cell['piece'] == o:
                    self.surface.blit(o_img, cell['pos'])

    def _draw_win(self):
        image = pygame.Surface([self.size, self.size], pygame.SRCALPHA, 32)
        surface = image.convert_alpha(image)
        pygame.draw.line(surface, red, self.win[0], self.win[1], 8)
        self.surface.blit(surface, (0, 0))

    def draw(self):
        self.surface.fill(white)

        self._draw_frame()
        self._draw_pieces()
        if self.win:
            self._draw_win()


pygame.init()
running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
y_offset = (SCREEN_HEIGHT - BOARD_SIZE) // 2
x_offset = (SCREEN_WIDTH - BOARD_SIZE) // 2
center = x_offset, y_offset
board = Board(BOARD_SIZE)

player = x
win = False

while running and not win:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if board.mark(event.pos, player):
                win = board.check_win(player)
                player = o if player == x else x
        elif event.type == pygame.QUIT:
            running = False

    screen.fill(white)
    board.draw()
    screen.blit(board.surface, center)
    pygame.display.flip()

pygame.quit()
