import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Hàm vẽ khung chứa chữ
def draw_text_box(text, font, color, x, y, width, height):
    # Vẽ khung chữ nhật
    pygame.draw.rect(screen, WHITE, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)  # Viền đen

    # Hiển thị chữ ở giữa khung
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ĐƯỜNG LÊN ĐỈNH OLYMPIA")

# Phông chữ
font = pygame.font.Font(None, 36)

# Tải âm thanh
pygame.mixer.music.load("background_music.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")
damage_sound = pygame.mixer.Sound("damage.mp3")
correct_sound = pygame.mixer.Sound("correct.mp3")

# Chạy âm thanh nền
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.3)  # Giảm âm lượng nền

# Biến cho khối
block_x = 400  # Vị trí ban đầu của khối trên trục X
block_y = 20  # Vị trí ban đầu của khối trên trục Y
block_width = 100  # Chiều rộng của khối
block_height = 100  # Chiều cao của khối
block_speed = 0.5  # Tốc độ di chuyển của khối
block_direction = 1  # Hướng di chuyển: 1 là phải, -1 là trái

# Cập nhật vị trí khối
block_x += block_speed * block_direction

# Đảo ngược hướng nếu khối chạm vào biên màn hình
if block_x <= 0 or block_x + block_width >= SCREEN_WIDTH:
    block_direction *= -1

# Hàm khởi động lại trò chơi
def restart_game():
    global player_health, monster_health, player_answer, character_x, character_y
    global monster_x, monster_y, monster_speed_x, monster_defeated, game_over, current_question
    
# Đặt lại trạng thái ban đầu
    player_health = 3  # Máu người chơi ban đầu
    monster_health = 3  # Máu quái vật ban đầu
    player_answer = ""  # Xóa câu trả lời của người chơi
    
# Đặt lại vị trí nhân vật
    character_x = SCREEN_WIDTH // 6 - character_width // 2
    character_y = 400 - character_height // 2
    monster_x = SCREEN_WIDTH // 2 - monster_width // 2
    monster_y = 400 - monster_height // 2  # Tốc độ ban đầu của quái vật
    character_speed = 5
    monster_speed_y = 0
    monster_speed_x = 3
    
# Trạng thái trò chơi
    monster_defeated = False
    game_over = False

# Lấy một câu hỏi ngẫu nhiên
    current_question = random.choice(questions)

# Tải hình ảnh khối
block_image = pygame.image.load("block.png")
block_image = pygame.transform.scale(block_image, (100, 20))  # Đặt kích thước khối

# Vẽ khối bằng hình ảnh
screen.blit(block_image, (block_x, block_y))

# Tải hình nền và tài nguyên
background = pygame.image.load("background.jpg")
background_width, background_height = background.get_size()

character = pygame.image.load("character.png")
character = pygame.transform.scale(character, (50, 50))

# Trạng thái game
game_state = "intro"
current_level = 1

# Vị trí và vận tốc quái vật
monster_x = 500
monster_y = SCREEN_HEIGHT // 2
monster_speed_x = 3
monster_speed_y = 0  # Quái vật chỉ di chuyển ngang

# Tải nhân vật
character = pygame.image.load("character.png")
character = pygame.transform.scale(character, (50, 50))
character_width, character_height = character.get_size()
monster = pygame.image.load("monster.png")
monster = pygame.transform.scale(monster, (100, 100))
monster_width, monster_height = character.get_size()

# Vị trí nhân vật
character_x = SCREEN_WIDTH // 6 - character_width // 2
character_y = 400 - character_height // 2
monster_x = SCREEN_WIDTH // 2 - monster_width // 2
monster_y = 400 - monster_height // 2

# Vận tốc nhân vật
character_speed = 5

# Câu hỏi của quái vật
questions = [
    {"question": "Ai đẹp trai nhất", "answer": "1"},
    {"question": "trai đẹp tên gì", "answer": "1"},
    {"question": "What is 10 - 6?", "answer": "1"},
]
current_question = random.choice(questions)


# Trạng thái trò chơi
player_answer = ""
monster_defeated = False
game_over = False

# Hệ thống máu
player_health = 3
monster_health = 3

# Tọa độ nền
bg_x = 0

# Đồng hồ để điều khiển tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60
# Vòng lặp trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Nhấn phím 'R' để restart
                    restart_game()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_answer.lower() == current_question["answer"].lower():
                        monster_health -= 1
                        correct_sound.play()
                        current_question = random.choice(questions)  # Câu hỏi mới
                        if monster_health <= 0:
                            monster_defeated = True
                            game_over = True
                    else:
                        player_health -= 1
                        damage_sound.play()
                        if player_health <= 0:
                            game_over = True
                    player_answer = ""  # Xóa câu trả lời
                elif event.key == pygame.K_BACKSPACE:
                    player_answer = player_answer[:-1]  # Xóa ký tự cuối
                else:
  
                    player_answer += event.unicode  # Thêm ký tự nhập
# Cập nhật vị trí khối
    block_x += block_speed * block_direction
    if block_x <= 0 or block_x + block_width >= SCREEN_WIDTH:
        block_direction *= -1
# Nhận phím bấm
    keys = pygame.key.get_pressed()

# Di chuyển nền theo chiều ngang
    if keys[pygame.K_LEFT]:
        if character_x > SCREEN_WIDTH // 4:
# Nhân vật di chuyển sang trái nếu còn khoảng cách để di chuyển
            character_x -= character_speed
        elif bg_x < 0:
# Cuộn nền sang phải
            bg_x += character_speed
    if keys[pygame.K_RIGHT]:
        if character_x < 3 * SCREEN_WIDTH // 4 - character_width:

# Nhân vật di chuyển sang phải nếu còn khoảng cách để di chuyển
            character_x += character_speed
        elif bg_x > -(background_width - SCREEN_WIDTH):

# Cuộn nền sang trái
            bg_x -= character_speed
# Cập nhật vị trí quái vật
    if not monster_defeated:
        monster_x += monster_speed_x

# Đổi hướng nếu chạm rìa màn hình
        if monster_x <= 0 or monster_x >= SCREEN_WIDTH - 100:
            monster_speed_x = -monster_speed_x
        if monster_y <= 0 or monster_y >= SCREEN_HEIGHT - 100:
            monster_speed_y = -monster_speed_y

# Kiểm tra va chạm với quái vật
    character_rect = pygame.Rect(character_x, character_y, 50, 50)
    monster_rect = pygame.Rect(monster_x, monster_y, 100, 100)
     
    if character_rect.colliderect(monster_rect):
            monster_speed_x = 0  # Quái vật dừng lại khi va chạm
            player_health -= 0  # Giảm máu nhân vật
            if player_health <= 0:
                game_over = True
# Hiển thị khung chứa câu hỏi khi cần
    if not monster_defeated and character_rect.colliderect(monster_rect):
        draw_text_box(
            text=current_question["question"],
            font=font,
            color=BLACK,
            x=50,
            y=100,
            width=700,
            height=50,
        )

# Hiển thị khung chứa câu trả lời
        draw_text_box(
            text=f"Your answer: {player_answer}",
            font=font,
            color=RED,
            x=50,
            y=200,
            width=700,
            height=50,
        )
# Hiển thị câu hỏi nếu nhân vật chạm vào quái vật
        question_active = True
    else:
        question_active = False
# Vẽ nền
    screen.fill(WHITE)
    screen.blit(background, (bg_x, 0))

# Vẽ khối di chuyển
    screen.blit(block_image, (block_x, block_y))  # Vẽ khối bằng hình ảnh
# Vẽ nhân vật
    screen.blit(character, (character_x, character_y))
# Vẽ quái vật
    if not monster_defeated:
        screen.blit(monster, (monster_x, monster_y))
# Hiển thị máu
    player_health_text = font.render(f"Player Health: {player_health}", True, BLACK)
    monster_health_text = font.render(f"Monster Health: {monster_health}", True, BLACK)
    screen.blit(player_health_text, (550, 10))
    screen.blit(monster_health_text, (550, 50))
# Hiển thị câu hỏi nếu cần
    if question_active and not monster_defeated:
        question_text = font.render(current_question["question"], True, BLACK)
        draw_text_box(
            text=current_question["question"],
            font=font,
            color=BLACK,
            x=50,
            y=100,
            width=700,
            height=50,
        )
        

# Hiển thị câu trả lời người chơi
        answer_text = font.render(f"Your answer: {player_answer}", True, RED)
        draw_text_box(
            text=f"Your answer: {player_answer}",
            font=font,
            color=RED,
            x=50,
            y=200,
            width=700,
            height=50,
        )
# Kiểm tra kết thúc trò chơi

    if game_over:
        if player_health <= 0:
            draw_text_box(
                text="Game Over! You Lost!",
                font=font,
                color=RED,
                x=SCREEN_WIDTH // 2 - 200,
                y=SCREEN_HEIGHT // 2 - 25,
                width=400,
                height=50,
            )
        elif monster_health <= 0:
            draw_text_box(
                text="You Won! Monster Defeated!",
                font=font,
                color=GREEN,
                x=SCREEN_WIDTH // 2 - 200,
                y=SCREEN_HEIGHT // 2 - 25,
                width=400,
                height=50,
            )
            draw_text_box(
            text="Press 'R' to Restart",
            font=font,
            color=BLACK,
            x=SCREEN_WIDTH // 2 - 200,
            y=SCREEN_HEIGHT // 2 + 50,
            width=400,
            height=50,
        )
    
# Cập nhật màn hình
    pygame.display.flip()

# Giới hạn tốc độ khung hình
    clock.tick(FPS)

# Thoát Pygame
pygame.quit()
sys.exit()
