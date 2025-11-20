import unittest
import pygame
from src.entities import Paddle, Ball, Brick
from src.game import Game, SCREEN_HEIGHT

class TestGameEntities(unittest.TestCase):
    def setUp(self):
        self.screen_width = 800
        self.paddle = Paddle(350, 550, 100, 20, (0, 255, 0), 10, self.screen_width)
        self.ball = Ball(400, 300, 10, (255, 255, 255), 5, -5)
        self.brick = Brick(100, 100, 75, 20, (255, 0, 0))

    def test_paddle_move_left(self):
        initial_x = self.paddle.rect.x
        self.paddle.move("left")
        self.assertEqual(self.paddle.rect.x, initial_x - self.paddle.speed)

    def test_paddle_move_right(self):
        initial_x = self.paddle.rect.x
        self.paddle.move("right")
        self.assertEqual(self.paddle.rect.x, initial_x + self.paddle.speed)

    def test_paddle_boundary_left(self):
        self.paddle.rect.x = 0
        self.paddle.move("left")
        self.assertEqual(self.paddle.rect.x, 0)

    def test_paddle_boundary_right(self):
        self.paddle.rect.right = self.screen_width
        self.paddle.move("right")
        self.assertEqual(self.paddle.rect.right, self.screen_width)

    def test_ball_move(self):
        initial_x = self.ball.rect.x
        initial_y = self.ball.rect.y
        self.ball.move()
        self.assertEqual(self.ball.rect.x, initial_x + self.ball.speed_x)
        self.assertEqual(self.ball.rect.y, initial_y + self.ball.speed_y)

    def test_brick_active(self):
        self.assertTrue(self.brick.active)

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Initialize pygame to avoid errors in Game init
        pygame.init()
        # Set display mode to avoid "No video mode has been set" error if Game init does it
        # But Game init does set_mode. We might need to mock it or just let it run if headless.
        # For simple logic tests, we can instantiate Game.
        self.game = Game()
        # Suppress window for tests if possible, or just ignore.

    def tearDown(self):
        pygame.quit()

    def test_initial_lives(self):
        self.assertEqual(self.game.lives, 3)

    def test_life_lost(self):
        initial_lives = self.game.lives
        # Force ball to bottom
        self.game.ball.rect.y = SCREEN_HEIGHT + 10
        self.game.update()
        self.assertEqual(self.game.lives, initial_lives - 1)
        self.assertFalse(self.game.game_over)

    def test_game_over_after_lives_lost(self):
        self.game.lives = 1
        self.game.ball.rect.y = SCREEN_HEIGHT + 10
        self.game.update()
        self.assertEqual(self.game.lives, 0)
        self.assertTrue(self.game.game_over)

if __name__ == '__main__':
    unittest.main()
