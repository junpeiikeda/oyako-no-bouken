import pygame
from pygame.locals import *
import os
import sys
import random

# 定数定義

# 全体に関するもの
SELL = 50                                                     # 1マスの大きさ
BACKGROUND_COLOR = (255, 255, 255)                            # 背景色
WINDOW_SIZE_X = 24 * SELL                                     # 画面の横幅
WINDOW_SIZE_Y = 12 * SELL                                     # 画面の縦幅
SCR_RECT = Rect(0, 0, WINDOW_SIZE_X, WINDOW_SIZE_Y)           # rectオブジェクトとしての画面定義
GRAVITY = 0.2                                                 # 重力

# キャラクター
CHARACTOR_X = 9 * SELL                                        # キャラのｘ座標初期位置
CHARACTOR_Y = 9 * SELL                                        # キャラのｙ座標初期位置
CHARACTOR_SIZE_X = SELL / 5 * 3                               # キャラの横幅
CHARACTOR_SIZE_Y = SELL                                       # キャラの縦幅
CHARACTOR_SPEED = 2.5                                         # キャラの移動スピード
JUMP_SPEED = SELL / 7                                         # ジャンプの強さ

# ブロック
BLOCK_SIZE = SELL                                             # ブロックの一辺の大きさ

# やり
SPEAR_Y = SELL                                                # 槍の生成高度
SPEAR_SIZE_X = SELL / 3                                       # 槍の横幅
SPEAR_SIZE_Y = SELL                                           # 槍の縦幅
SPEAR_FALL_SPEED = 1                                          # 槍の降下速度

# こども
CHILD_X = 3 * SELL                                            # こどものｘ座標初期位置
CHILD_Y = 10 * SELL                                           # こどものｙ座標初期位置
CHILD_SIZE_X = CHARACTOR_SIZE_X * 0.8                         # こどもの横幅
CHILD_SIZE_Y = CHARACTOR_SIZE_Y * 0.8                         # こどもの縦幅
CHILD_SPEED = CHARACTOR_SPEED * 1.2                           # こどもの移動速度

# ゴール
GOAL_X = 21 * SELL                                            # ゴールのｘ座標位置
GOAL_Y = 1 * SELL                                             # ゴールのｙ座標位置
GOAL_SIZE_X = SELL                                            # ゴールの縦幅
GOAL_SIZE_Y = SELL                                            # ゴールの横幅

# ゲームクラス
class GAME:
    def __init__(self):
        game_flug = False   # ゲームプレイフラグ
        GAME.goal_flug_child = False    # こどものゴール判定
        GAME.goal_flug_charactor = False    # キャラのゴール判定
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("おやこ の ぼうけん")
        
        # 各種画像のロード
        self.background_image = load_image("background.png")    # 背景
        self.background_image =  pygame.transform.scale(self.background_image, (WINDOW_SIZE_X, WINDOW_SIZE_Y))
        self.bg_rect = self.background_image.get_rect()

        self.clear_image = load_image("clear.png")    # クリア画面
        self.clear_image =  pygame.transform.scale(self.clear_image, (WINDOW_SIZE_X, WINDOW_SIZE_Y))
        self.clear_rect = self.clear_image.get_rect()

        self.start_image = load_image("start.png")    # スタート画面
        self.start_image =  pygame.transform.scale(self.start_image, (WINDOW_SIZE_X, WINDOW_SIZE_Y))
        self.start_rect = self.start_image.get_rect()

        Charactor.left_image = load_image("character.png", (255, 255, 255))    # キャラクター（白色透過）
        Charactor.left_image = pygame.transform.scale(Charactor.left_image, (CHARACTOR_SIZE_X, CHARACTOR_SIZE_Y))   # 左向き
        Charactor.right_image = pygame.transform.flip(Charactor.left_image, 1, 0)   # 右向き

        Block.image = load_image("block.png")    # ブロック
        Block.image = pygame.transform.scale(Block.image, (BLOCK_SIZE, BLOCK_SIZE))

        Goal.image = load_image("goal.png", (255, 255, 255))    # ゴール（白色透過）
        Goal.image = pygame.transform.scale(Goal.image, (GOAL_SIZE_X, GOAL_SIZE_Y))

        Spear.image = load_image("spear.png", (255, 255, 255))    # やり（白色透過）
        Spear.image = pygame.transform.scale(Spear.image, (SPEAR_SIZE_X, SPEAR_SIZE_Y))

        Child.left_image = load_image("child.png", (255, 255, 255))    # こども（白色透過）
        Child.left_image = pygame.transform.scale(Child.left_image, (CHILD_SIZE_X, CHILD_SIZE_Y))   # 左向き
        Child.right_image = pygame.transform.flip(Child.left_image, 1, 0)   # 右向き
        
        while not game_flug:    # スタート画面
            screen.blit(self.start_image, self.start_rect)
            pygame.display.update()  
            for event in pygame.event.get():
                    if event.type == QUIT:  # ×ボタンで終了
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN and event.key == K_1:    # "1"で難易度「やさしい」
                        self.game_easy_level = 3    # ゲームのやさしさ
                        game_flug = True    # ゲームフラグたてる
                    elif event.type == KEYDOWN and event.key == K_2:    # "2"で難易度「ふつう」
                        self.game_easy_level = 2
                        game_flug = True
                    elif event.type == KEYDOWN and event.key == K_3:    # "3"で難易度「むづかしい」
                        self.game_easy_level = 1
                        game_flug = True

        # スプライトグループの作成（ゲーム内では一つしかないオブジェクトも今後の拡張性を考えグループにする）
        self.all = pygame.sprite.RenderUpdates()
        self.spears = pygame.sprite.Group()
        self.childlen = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        Charactor.objects = self.all
        Child.objects = self.all
        Goal.objects = self.all, self.goals
        Spear.objects = self.all, self.spears, self.blocks
        Block.objects = self.all, self.blocks
        
        Charactor((CHARACTOR_X ,CHARACTOR_Y), self.blocks, self.spears, self.goals)   # 衝突判定用に各種グループを引数に

        # オブジェクトの生成
        self.create_spears()
        self.create_blocks()
        self.create_goal()
        self.create_children()

        # メインループ
        clock = pygame.time.Clock()     # 時間の概念
        while True:
            clock.tick(60)      # 描画間隔
            self.update()       # オブジェクトの状態更新
            self.draw(screen)       # 描画
            pygame.display.update()     # 描画更新
            self.key_action()      # キー操作
            if GAME.goal_flug_charactor and GAME.goal_flug_child:       # キャラもこどももゴールしたら
                self.crear()        # クリア処理
    
    def crear(self):    # クリア処理
        while True:
            screen = pygame.display.set_mode(SCR_RECT.size)
            screen.blit(self.clear_image, self.clear_rect)  # クリア画面
            pygame.display.update()   
            for event in pygame.event.get():
                    if event.type == QUIT:    # バツで終了
                        pygame.quit()
                        sys.exit()

    def update(self):   # 状態更新
        self.all.update()
    
    def draw(self, screen):     # 描画
        screen.blit(self.background_image, self.bg_rect)
        self.create_spears()    # spearは独自描画
        self.all.draw(screen)

    def key_action(self):   # キー操作
        for event in pygame.event.get():    # バツで終了
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def create_spears(self):    # やりの生成
        num = random.randint(0, 70 * self.game_easy_level)    # やさしさレベルに応じた乱数生成
        if num == 13:    # 13が出れば
            spear_position_x = random.randint(0, WINDOW_SIZE_X)    # ウィンドウ内にやり生成座標設定
            Spear((spear_position_x, SPEAR_Y), self.spears, self.blocks)    # 生成
    
    def create_blocks(self):
        # 天井と床
        for x in range(24):
            Block((x * SELL, 0))
        for i in range(13):
            Block((i * SELL, 11 * SELL))
        for i in range(9):
            Block((15 * SELL + i * SELL, 11 * SELL))
        
        # 左右の壁
        for y in range(10):
            Block((0, y * SELL + SELL))
            Block((23 * SELL, y * SELL + SELL))
        
        # 空中ブロック
        for i  in range(4):
            Block((5 * SELL + i * SELL, 9 * SELL))
        for i in range(4):
            Block((14 * SELL, 5 * SELL + i * SELL))
        for i in range(3):
            Block((7 * SELL + i * SELL, 4 * SELL))
        Block((12 * SELL, 5 * SELL))
        for i in range(3):
            Block((14 * SELL + i * SELL, 5 * SELL))
        for i in range(2):
            Block((17 * SELL +  i * SELL, 7 * SELL))
        for i in range(2):
            Block((20 * SELL + i * SELL, 9 * SELL))
        Block((1 * SELL, 7 * SELL))
        Block((2 * SELL, 6 * SELL))
        Block((3 * SELL, 7 * SELL))
        Block((8 * SELL, 8 * SELL))
        Block((8 * SELL, 7 * SELL))
        Block((5 * SELL, 5 * SELL))
        Block((14 * SELL, 1 * SELL))
        Block((14 * SELL, 2 * SELL))
        Block((15 * SELL, 2 * SELL))
        Block((20 * SELL, 1 * SELL))
        Block((21 * SELL, 2 * SELL))
        Block((22 * SELL, 4 * SELL))
        Block((1 * SELL, 3 * SELL))
        Block((2 * SELL, 3 * SELL))
        Block((17 * SELL, 8 * SELL))
        Block((25 * SELL, 1 * SELL))
        Block((27 * SELL, 1 * SELL))
        Block((26 * SELL, 0 * SELL))
        Block((26 * SELL, 2 * SELL))
        Block((20 * SELL, 3 * SELL))
        Block((20 * SELL, 5 * SELL))
        Block((21 * SELL, 6 * SELL))

    def create_children(self):    # こども生成
        Child((CHILD_X, CHILD_Y), self.blocks, self.spears, self.goals)
    
    def create_goal(self):    # ゴール生成
        Goal((GOAL_X, GOAL_Y))

# ブロッククラス
class Block(pygame.sprite.Sprite):
    def __init__(self, position):    # rectオブジェクトとしての登録と位置の定義
        pygame.sprite.Sprite.__init__(self, self.objects)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

# ゴールクラス
class Goal(pygame.sprite.Sprite):
    def __init__(self, position):    # rectオブジェクトとしての登録と位置の定義
        pygame.sprite.Sprite.__init__(self, self.objects)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

# やりクラス
class Spear(pygame.sprite.Sprite):
    def __init__(self, position, spears, blocks):
        pygame.sprite.Sprite.__init__(self, self.objects)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.rect.x, self.rect.y = position[0], position[1]    # リストとして座標を保存
        self.spears = spears
        self.blocks = blocks

        # 浮動小数点込みの位置と速度の値
        self.floatpoint_x = float(self.rect.x)
        self.floatpoint_y = float(self.rect.y)
        self.floatpoint_vx = 0.0
        self.floatpoint_vy = 0.0
    
    def update(self):    # 描画更新
        if self.rect.y <= 13 * SELL:    # 画面下の一定ラインまで降下し続ける
            self.rect.move_ip(0, SPEAR_FALL_SPEED)

# こどもクラス
class Child(pygame.sprite.Sprite):
    def __init__(self, position, blocks, spears, goals):
        pygame.sprite.Sprite.__init__(self, self.objects)
        self.image = self.left_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]    # リストとして座標を保存
        self.blocks = blocks
        self.spears = spears
        self.goals = goals
        
        # 浮動小数点込みの位置と速度の値
        self.floatpoint_x = float(self.rect.x)
        self.floatpoint_y = float(self.rect.y)
        self.floatpoint_vx = 0.0
        self.floatpoint_vy = 0.0
        
        self.floor_flug = False    # 接地判定フラグ
        
    def update(self):
        pressed_keys = pygame.key.get_pressed()    # キーが押されたか
        if pressed_keys[K_RIGHT]:    # 右移動
            self.image = self.right_image
            self.floatpoint_vx = CHILD_SPEED
        elif pressed_keys[K_LEFT]:    # 左移動
            self.image = self.left_image
            self.floatpoint_vx = -CHILD_SPEED
        else:    # 何もなければ停止
            self.floatpoint_vx = 0.0
        
        if pressed_keys[K_UP]:    # ジャンプ（上のまとまりの中に入れない）
            if self.floor_flug:
                self.floatpoint_vy = - JUMP_SPEED  
                self.floor_flug = False

        if self.rect.y >= 14 * SELL:    # 下におちたらゲームオーバー
            print("GAMEOVER")
            pygame.quit()
            sys.exit()
        
        if not self.floor_flug:    # 空中に居たら重力かける
            self.floatpoint_vy += GRAVITY
        
        # 各種衝突判定処理
        self.collision_x()
        self.collision_y()
        self.collision()

        # 位置の更新
        self.rect.x = int(self.floatpoint_x)
        self.rect.y = int(self.floatpoint_y)
    
    def collision(self):    # 縦横問わない衝突判定
        for child in self.spears:    # やりは上からくるのでキャラの上からぶつからないと判定が発生しない
            collide = self.rect.colliderect(child.rect)    # 判定
            if collide:    # 衝突したらゲームオーバー
                self.game_flug = False
                print("GAMEOVER")
                pygame.quit()
                sys.exit()

        for goal in self.goals:    # ゴールとの衝突判定
            collide2 = self.rect.colliderect(goal.rect)    # 判定
            if collide2:  # 衝突したら画面外の囲いの中に入れ、ゴールフラグ立てる
                GAME.goal_flug_child = True
                self.floatpoint_x = 26 *SELL
                self.floatpoint_y = 1 * SELL
                self.floatpoint_vy = 0
                
    def collision_x(self):    # x方向の当たり判定
        newx = self.floatpoint_x + self.floatpoint_vx   # 更新後のx座標
        newrect = Rect(newx, self.floatpoint_y, CHILD_SIZE_X, CHILD_SIZE_Y)    # 更新後のrectオブジェクト
        for block in self.blocks:    # ブロックごと参照
            collide = newrect.colliderect(block.rect)    # 判定
            if collide:  # 衝突するブロックあり
                if self.floatpoint_vx > 0:    # 右に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.floatpoint_x = block.rect.left - CHILD_SIZE_X
                    self.floatpoint_vx = 0
                elif self.floatpoint_vx < 0:  # 左に移動中に衝突
                    self.floatpoint_x = block.rect.right
                    self.floatpoint_vx = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.floatpoint_x = newx
    
    def collision_y(self):    # y方向衝突判定
        newy = self.floatpoint_y + self.floatpoint_vy    # 更新後のy座標
        newrect = Rect(self.floatpoint_x, newy, CHILD_SIZE_X, CHILD_SIZE_Y)    # 更新後のrectオブジェクト
        for block in self.blocks:    # ブロックごとに参照
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突していれば
                if self.floatpoint_vy > 0:    # 下に移動中に衝突していれば
                    self.floatpoint_y = block.rect.top - CHILD_SIZE_Y    # めり込み直し
                    self.floatpoint_vy = 0    # 落下を止まる
                    self.floor_flug = True    # 接地フラグ
                elif self.floatpoint_vy < 0:  # 上に移動中に衝突していれば
                    self.floatpoint_y = block.rect.bottom
                    self.floatpoint_vy = 0
                break    # y方向に関して同時に二つのブロックに触れることはない
            else:    # 衝突鳴ければ
                self.floatpoint_y = newy    # 位置更新
                self.floor_flug = False

# キャラクタークラス
class Charactor(pygame.sprite.Sprite):
    def __init__(self, position, blocks, spears, goals):
        pygame.sprite.Sprite.__init__(self, self.objects)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]  # 座標をリストとしておく
        self.blocks = blocks
        self.spears = spears
        self.goals = goals
        
        # 浮動小数点込みの位置と速度の値
        self.floatpoint_x = float(self.rect.x)
        self.floatpoint_y = float(self.rect.y)
        self.floatpoint_vx = 0.0
        self.floatpoint_vy = 0.0
        
        self.floor_flug = False    # 接地フラグ
        
    def update(self):    # 更新
        pressed_keys = pygame.key.get_pressed()    # キー押されているか

        if pressed_keys[K_RIGHT]:    # 右移動
            self.image = self.right_image
            self.floatpoint_vx = CHARACTOR_SPEED
        elif pressed_keys[K_LEFT]:    # 左移動
            self.image = self.left_image
            self.floatpoint_vx = -CHARACTOR_SPEED
        else:    # 押されていなければ
            self.floatpoint_vx = 0.0    # 停止
        
        if pressed_keys[K_UP]:    # ジャンプ
            if self.floor_flug:    # 地面にいれば（空中ジャンプ不可）
                self.floatpoint_vy = - JUMP_SPEED  # 飛ぶ
                self.floor_flug = False    # 接地フラグオフ
        
        if self.rect.y >= 14 * SELL:    # 画面下に落ちればゲームオーバー
            print("GAMEOVER")
            pygame.quit()
            sys.exit()
        
        if not self.floor_flug:    # 滞空中は
            self.floatpoint_vy += GRAVITY  # 重力をかける
        
        # 各種衝突判定
        self.collision_x()
        self.collision_y()
        self.collision()
        
        # 浮動小数点込みの位置を整数として座標に戻す
        self.rect.x = int(self.floatpoint_x)
        self.rect.y = int(self.floatpoint_y)
    
    def collision(self):    # 縦横含む衝突判定
        for child in self.spears:    # やり
            collide = self.rect.colliderect(child.rect)
            if collide:  # 衝突したらゲームオーバー
                print("GAMEOVER")
                pygame.quit()
                sys.exit()

        for goal in self.goals:    # ゴールとの衝突判定
            collide = self.rect.colliderect(goal.rect)
            if collide:  # 衝突したら
                GAME.goal_flug_charactor = True    # キャラ用のゴールフラグを挙げ、画面外の囲いに移動
                self.floatpoint_x = 2 * SELL
                self.floatpoint_y = 10 * SELL
                self.floatpoint_vy = 0

    def collision_x(self):    # z方向当たり判定
        newx = self.floatpoint_x + self.floatpoint_vx   # 更新後の座標
        newrect = Rect(newx, self.floatpoint_y, CHARACTOR_SIZE_X, CHARACTOR_SIZE_Y)     # 更新「後のrectオブジェクト
        
        for block in self.blocks:    # ブロックごとに判定
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突していたら
                if self.floatpoint_vx > 0:    # 右に移動中に衝突したら
                    self.floatpoint_x = block.rect.left - CHARACTOR_SIZE_X    # めり込み戻し
                    self.floatpoint_vx = 0    # 止める
                elif self.floatpoint_vx < 0:  # 左に移動中に衝突したら
                    self.floatpoint_x = block.rect.right    # めり込み調整
                    self.floatpoint_vx = 0    # とまる
                break  # x方向に関して同時に二つのブロックに触れることはない
            else:    # 衝突ない場合
                self.floatpoint_x = newx    # 更新
    
    def collision_y(self):    # ｙ方向の衝突判定
        newy = self.floatpoint_y + self.floatpoint_vy    # 更新後のｙ座標
        newrect = Rect(self.floatpoint_x, newy, CHARACTOR_SIZE_X, CHARACTOR_SIZE_Y)    # 更新後のrectオブジェクト
        
        for block in self.blocks:    # ブロックごとに見る
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突していたら
                if self.floatpoint_vy > 0:    # 下に移動中に衝突していたら
                    self.floatpoint_y = block.rect.top - CHARACTOR_SIZE_Y    # めり込みなおし停止
                    self.floatpoint_vy = 0
                    self.floor_flug = True    # 接地フラグ
                elif self.floatpoint_vy < 0:  # 上に移動中に衝突したら
                    self.floatpoint_y = block.rect.bottom    # めり込みなおし停止
                    self.floatpoint_vy = 0
                break  # ｙ軸に関して同時に二つのブロックに触れることはない
            else:
                self.floatpoint_y = newy    # 何もなければ座標更新
                self.floor_flug = False    # 接地フラグオフ（滞空中）

def load_image(filename, colorkey = None):    # 画像ロード
    filename = os.path.join("data", filename)    # 参照先の指定
    image = pygame.image.load(filename)       # ロード
    image = image.convert()   #これ書かないと重くなる
    if colorkey is not None:    # 透過が指定されているか
        if colorkey is -1:
            colorkey = image.get_at((0,0))    # 透過処理
        image.set_colorkey(colorkey, RLEACCEL)
    return image    # ロード後の画像を返す


# 実行部
if __name__ == "__main__":
    GAME()
