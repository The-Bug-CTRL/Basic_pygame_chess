import chess
import pygame
import os
import random

# Function to draw the chessboard using pygame
def draw_board(screen, board):
    for row in range(8):
        for col in range(8):
            square_color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(chess.square(col, row))
            if piece:
                piece_image = pygame.image.load(os.path.join("images", f"{piece.symbol()}.png" if piece.color == chess.WHITE else f"{piece.symbol()}.jpg"))
                piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE))


# Function to handle player's move with piece dragging
def handle_player_move(board, start, end):
    move = chess.Move.from_uci(f"{start}{end}")
    if move in board.legal_moves:
        board.push(move)
        return True
    return False

# Function to handle AI's move
def make_ai_move(board):
    legal_moves = list(board.legal_moves)
    ai_move = random.choice(legal_moves)
    return ai_move

# Main function to run the game
def main():
    pygame.init()

    global SQUARE_SIZE
    SQUARE_SIZE = 100
    WIDTH, HEIGHT = 8 * SQUARE_SIZE, 8 * SQUARE_SIZE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    board = chess.Board()

    clock = pygame.time.Clock()

    running = True
    player_turn = True
    dragging = False
    selected_square = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - (event.pos[1] // SQUARE_SIZE)
                square = chess.square(col, row)

                if board.piece_at(square) and board.piece_at(square).color == board.turn:
                    selected_square = square
                    dragging = True

            elif player_turn and event.type == pygame.MOUSEBUTTONUP and dragging:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - (event.pos[1] // SQUARE_SIZE)
                end_square = chess.square(col, row)

                if handle_player_move(board, chess.square_name(selected_square), chess.square_name(end_square)):
                    player_turn = False  # Switch to AI's turn

                dragging = False

        if not player_turn and not board.is_game_over():
            pygame.time.wait(500)
            ai_move = make_ai_move(board)
            print(f"AI Move: {ai_move.uci()}")
            board.push(ai_move)
            player_turn = True  # Switch back to player's turn

        screen.fill((255, 255, 255))
        draw_board(screen, board)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()