import pygame
import os
import glob
from src.entities import Paddle, Ball, Brick

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
PADDLE_COLOR = (0, 255, 0)
BALL_COLOR = (255, 255, 255)
BRICK_COLORS = [
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255)     # Blue
]
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
PADDLE_SPEED = 6
BALL_SPEED_X = 4
BALL_SPEED_Y = -4
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
BRICK_OFFSET_LEFT = 35

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.running = True
        self.running = True
        # Try to load a Japanese font
        font_path = None
        
        # Use glob to avoid unicode normalization issues with filenames
        potential_patterns = [
            "/System/Library/Fonts/*Hiragino*W3.ttc", # Hiragino Sans / Kaku Gothic
            "/System/Library/Fonts/AppleGothic.ttf",  # Older but reliable
            "/System/Library/Fonts/*Heiti*.ttc",      # Fallback
            "/System/Library/Fonts/*Gothic*.ttf",     # Generic Gothic
        ]
        
        for pattern in potential_patterns:
            matches = glob.glob(pattern)
            if matches:
                font_path = matches[0]
                break
        
        # If still not found, try match_font
        if not font_path:
            font_names = ["hiraginosans", "hiraginokakugothicpron", "hiraginominchopron", "applegothic", "msgothic", "meiryo"]
            for name in font_names:
                path = pygame.font.match_font(name)
                if path and os.path.exists(path):
                    font_path = path
                    break
        
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, 24)
            except:
                self.font = pygame.font.Font(None, 24)
        else:
            # Fallback to system font if no specific match found
            self.font = pygame.font.SysFont("Hiragino Sans", 24)

        self.reset_game()

    def reset_game(self):
        self.paddle = Paddle(
            (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
            SCREEN_HEIGHT - 50,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_COLOR,
            PADDLE_SPEED,
            SCREEN_WIDTH
        )
        self.ball = Ball(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            BALL_RADIUS,
            BALL_COLOR,
            BALL_SPEED_X,
            BALL_SPEED_Y
        )
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING)
                y = BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                self.bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, color))
        
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.won = False

    def reset_ball_paddle(self):
        self.paddle = Paddle(
            (SCREEN_WIDTH - PADDLE_WIDTH) // 2,
            SCREEN_HEIGHT - 50,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_COLOR,
            PADDLE_SPEED,
            SCREEN_WIDTH
        )
        self.ball = Ball(
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            BALL_RADIUS,
            BALL_COLOR,
            BALL_SPEED_X,
            BALL_SPEED_Y
        )

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (self.game_over or self.won):
                    self.reset_game()

        keys = pygame.key.get_pressed()
        if not self.game_over and not self.won:
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

    def update(self):
        if self.game_over or self.won:
            return

        self.ball.move()

        # Wall collision
        if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:
            self.ball.speed_x *= -1
        if self.ball.rect.top <= 0:
            self.ball.speed_y *= -1
        
        # Game Over / Life Lost
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.reset_ball_paddle()
            else:
                self.game_over = True

        # Paddle collision
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y *= -1
            # Prevent ball from getting stuck inside paddle
            self.ball.rect.bottom = self.paddle.rect.top

        # Brick collision
        for brick in self.bricks:
            if brick.active and self.ball.rect.colliderect(brick.rect):
                brick.active = False
                self.ball.speed_y *= -1
                self.score += 10
                break # Only hit one brick at a time
        
        # Win condition
        if all(not brick.active for brick in self.bricks):
            self.won = True

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        
        score_text = self.font.render(f"スコア: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"残機: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

        if self.game_over:
            game_over_text = self.font.render("ゲームオーバー - Rキーでリスタート", True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))
        
        if self.won:
            won_text = self.font.render("クリア！ - Rキーでリスタート", True, (0, 255, 0))
            self.screen.blit(won_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
