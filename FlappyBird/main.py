import pygame, sys, random

# các hàm cho trò chơi
# tạo floor 
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
# tạo hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) # chọn chiều cao ngẫu nhiên trong list pipe_height
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-730))
    return bottom_pipe, top_pipe
# hàm di chuyển ống - nhận list pipes sau đó di chuyển sang bên trái và trả lại list đó
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
# hàm vẽ ống lên màn hình
def draw_pipe(pipes):
    for pipe in pipes:
        # lật ống cho đối xứng nhau
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

# hàm xử lý va chạm
def check_collistion(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        hit_sound.play()
        return False
    return True
# hàm tạo xoay con chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
# hàm tạo chuyển động đập cánh con chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
# ham hien thi diem
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Socre: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,620))
        screen.blit(high_score_surface, high_score_rect)
# ham hien thi man hinh bat dau
def game_start(game_state):
    if game_state == 'game_start':
        screen.blit(game_start_surface, game_start_rect)
    else:
        game_active
# ham tinh diem        
def check_score(pipes,bird_rect):
    score = 0
    for pipe in pipes:
        if pipe <= bird_rect:
            score += 0.5
    return score    
# hàm cập nhật điểm cao
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# chỉnh âm thanh cho thích hợp
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

# tieu de
pygame.display.set_caption("Flappy Bird")

# khởi tạo cửa sổ chạy game
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# tạo các biến cho trò chơi
gravity = 0.5      
bird_movement = 0   
game_active = True  
game_start = True
high_score = 0     
# chèn background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
# chèn man hinh bat dau
game_start_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_start_rect = game_start_surface.get_rect(center=(216,384))
# chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# tạo con chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
# tạo hình chữ nhật xung quanh con chim
bird_rect = bird.get_rect(center = (100,384))
# tạo chuyen dong dap canh 
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
# tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# tạo sự kiện ống xuất hiện sau 1.2s
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
# Chiều cao của ống
pipe_height = [300, 350, 400]
# tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,384))
# chèn âm thanh
flap_sound = pygame.mixer.Sound('sounds/5_Flappy_Bird_sound_sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sounds/5_Flappy_Bird_sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('sounds/5_Flappy_Bird_sound_sfx_point.wav')
score_sound_countdown = 0
# vòng lặp của game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # ấn phím space thì con chim sẽ bay lên 1 khoảng -10 theo tọa độ của y
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                game_start = False
                bird_movement = 0
                bird_movement = -10
                flap_sound.play() 
            # reset lại game khi thua
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                # xóa những ống cũ và reset lại con chim
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                # reset điểm
                score = 0
                score_sound_countdown = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    # tọa độ backgroud
    screen.blit(bg,(0,0))
    if game_start:
        screen.blit(game_start_surface, game_start_rect)
        pipe_list.clear()
    elif game_active:
        # chim
        bird_movement += gravity 
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collistion(pipe_list)
        # ống
        pipe_list = move_pipe(pipe_list) 
        draw_pipe(pipe_list) 
        score = int(check_score(pipe_list,bird_rect))
        score_display('main_game') # hiển thị điểm
        # am thanh khi ghi diem
        if score_sound_countdown != score:
            score_sound.play()
            score_sound_countdown = score 
   
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    # sàn
    floor_x_pos -= 1
    draw_floor()
    # tạo floor chạy liên tục
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60) # fps = 60