import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 3
BALL_SIZE = 4  

BLOCK_WIDTH = 12
BLOCK_HEIGHT = 4
BLOCK_SPACING_X = 2
BLOCK_SPACING_Y = 2
BLOCK_ROWS = 5
BLOCK_MARGIN_Y = 20

# 横方向の自動計算
BLOCK_COLS = (SCREEN_WIDTH + BLOCK_SPACING_X) // (BLOCK_WIDTH + BLOCK_SPACING_X)
total_blocks_width = BLOCK_COLS * BLOCK_WIDTH + (BLOCK_COLS - 1) * BLOCK_SPACING_X
BLOCK_MARGIN_X = (SCREEN_WIDTH - total_blocks_width) // 2

# ゲーム状態
STATE_MENU = 0
STATE_PLAY = 1
STATE_GAME_OVER = 2
STATE_GAME_CLEAR = 3

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Block Breaking")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.state = STATE_MENU
        self.paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_vx = 1.5
        self.ball_vy = -1.5
        self.blocks = []
        for row in range(BLOCK_ROWS):
            for col in range(BLOCK_COLS):
                x = BLOCK_MARGIN_X + col * (BLOCK_WIDTH + BLOCK_SPACING_X)
                y = BLOCK_MARGIN_Y + row * (BLOCK_HEIGHT + BLOCK_SPACING_Y)
                self.blocks.append((x, y, True))

    def update(self):
        if self.state == STATE_MENU:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_A):
                self.state = STATE_PLAY

        elif self.state == STATE_PLAY:
            self.update_play()

        elif self.state in (STATE_GAME_OVER, STATE_GAME_CLEAR):
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.reset()

    def update_play(self):
        # パドル操作
        if pyxel.btn(pyxel.KEY_LEFT):
            self.paddle_x -= 2.5
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.paddle_x += 2.5

        self.paddle_x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, self.paddle_x))

        # ボール移動
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # 壁反射
        if self.ball_x < 0 or self.ball_x > SCREEN_WIDTH - BALL_SIZE:
            self.ball_vx *= -1
        if self.ball_y < 0:
            self.ball_vy *= -1

        # パドル反射
        if (self.paddle_x <= self.ball_x <= self.paddle_x + PADDLE_WIDTH) and \
           (self.ball_y + BALL_SIZE >= SCREEN_HEIGHT - 10):
            self.ball_vy *= -1
            self.ball_y = SCREEN_HEIGHT - 10 - BALL_SIZE

        # ブロック衝突
        new_blocks = []
        for x, y, is_alive in self.blocks:
            if is_alive and x < self.ball_x + BALL_SIZE and self.ball_x < x + BLOCK_WIDTH and \
               y < self.ball_y + BALL_SIZE and self.ball_y < y + BLOCK_HEIGHT:
                self.ball_vy *= -1
                is_alive = False
            new_blocks.append((x, y, is_alive))
        self.blocks = new_blocks

        # ゲームオーバー判定
        if self.ball_y > SCREEN_HEIGHT:
            self.state = STATE_GAME_OVER

        # クリア判定
        if all(not alive for _, _, alive in self.blocks):
            self.state = STATE_GAME_CLEAR

    def draw(self):
        pyxel.cls(0)
        if self.state == STATE_MENU:
            text = "Press Any Key to Start"
            text_width = len(text) * 4
            text_x = (SCREEN_WIDTH - text_width) // 2
            text_y = (SCREEN_HEIGHT - 8) // 2
            pyxel.text(text_x, text_y, text, pyxel.frame_count % 16)
        elif self.state == STATE_PLAY:
            # パドル
            pyxel.rect(self.paddle_x, SCREEN_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT, 11)
            # ボール
            pyxel.circ(self.ball_x, self.ball_y, BALL_SIZE // 2, 7)
            # ブロック
            for x, y, is_alive in self.blocks:
                if is_alive:
                    pyxel.rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT, 9)
        elif self.state == STATE_GAME_OVER:
            pyxel.text(60, 50, "Game Over!", 8)
            pyxel.text(45, 70, "Press Space to Retry", 7)
        elif self.state == STATE_GAME_CLEAR:
            pyxel.text(60, 50, "You Win!", 10)
            pyxel.text(45, 70, "Press Space to Restart", 7)

if __name__ == "__main__":
    App()
