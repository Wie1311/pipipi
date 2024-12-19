import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ĐƯỜNG LÊN ĐỈNH OLYMPIA")

# Phông chữ
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Tải hình ảnh
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
character = pygame.image.load("character.png")
character = pygame.transform.scale(character, (50, 50))
monster = pygame.image.load("monster.png")
monster = pygame.transform.scale(monster, (100, 100))

# Biến trạng thái
game_state = "intro"  # intro -> story -> level1 -> level2 -> level3 -> level4 -> end
player_health = 3
monster_health = 3
current_level = 1
player_answer = ""

# Câu hỏi cho từng màn chơi
questions = {
    1: [
        {"question": "Ai đẹp trai nhất?", "answer": "huy"},
        {"question": "Trai đẹp tên gì?", "answer": "huy"},
    ],
    2: [
        {"question": "What is 10 - 6?", "answer": "4"},
        {"question": "What is 5 + 3?", "answer": "8"},
    ],
    3: [
        {"question": "Thủ đô của Việt Nam là?", "answer": "hanoi"},
        {"question": "3 x 4 = ?", "answer": "12"},
    ],
    4: [
        {"question": "Python được phát hành năm nào?", "answer": "1991"},
        {"question": "Tác giả của Python là?", "answer": "guido"},
    ],
}

current_question = random.choice(questions[1])

# Đồng hồ để điều khiển tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# Hàm hiển thị màn hình giới thiệu
def show_intro():
    screen.fill(WHITE)
    title_text = title_font.render("ĐƯỜNG LÊN ĐỈNH OLYMPIA", True, BLUE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(title_text, title_rect)

    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50))
    start_text = font.render("START", True, BLACK)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
    screen.blit(start_text, start_rect)
    pygame.display.flip()

# Hàm hiển thị cốt truyện
def show_story():
    screen.fill(WHITE)
    story_lines = [
        "Bạn là một nhà vô địch trong hành trình chinh phục Olympia.",
        "Mỗi màn chơi sẽ là một thử thách mới với những câu hỏi hóc búa.",
        "Hãy chuẩn bị sẵn sàng và chinh phục từng màn để đến đỉnh vinh quang!",
        "Nhấn phím bất kỳ để bắt đầu màn 1."
    ]
    for i, line in enumerate(story_lines):
        story_text = font.render(line, True, BLACK)
        story_rect = story_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + i * 40))
        screen.blit(story_text, story_rect)
    pygame.display.flip()

# Hàm hiển thị màn chơi
def show_level(level):
    screen.fill(WHITE)
    level_text = title_font.render(f"MÀN {level}", True, GREEN)
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(level_text, level_rect)
    pygame.display.flip()

# Hàm kết thúc trò chơi
def show_end(victory=True):
    screen.fill(WHITE)
    if victory:
        end_text = title_font.render("BẠN ĐÃ CHIẾN THẮNG!", True, GREEN)
    else:
        end_text = title_font.render("GAME OVER!", True, RED)
    end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(end_text, end_rect)
    pygame.display.flip()

# Vòng lặp chính
running = True
while running:
    if game_state == "intro":
        show_intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and
                        SCREEN_HEIGHT // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + 50):
                    game_state = "story"

    elif game_state == "story":
        show_story()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game_state = "level1"

    elif game_state.startswith("level"):
        level = int(game_state[-1])
        show_level(level)
        pygame.time.delay(2000)  # Chờ 2 giây trước khi vào trò chơi
        current_question = random.choice(questions[level])
        game_state = f"playing{level}"

    elif game_state.startswith("playing"):
        level = int(game_state[-1])
        # Logic màn chơi: nhân vật, quái vật, câu hỏi
        # Nếu quái vật thắng hoặc người chơi trả lời đúng hết câu hỏi
        # Cập nhật trạng thái trò chơi:
        if monster_health <= 0:
            if level < 4:
                game_state = f"level{level + 1}"
            else:
                game_state = "end"

    elif game_state == "end":
        show_end(victory=player_health > 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
