import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_loop():
    global previous_trail
    previous_trail = []
    snake = [[10, 10], [11, 10], [12, 10]]
    direction = 'down'
    direction_change = False
    while True:
        clear_screen()
        print('  '.join(['#' * 20 for _ in range(20)]))
        for x, y in snake:
            print(' ', end='')
            for _ in range(20):
                if [x, y] in previous_trail:
                    print('o', end=' ')
                elif [x, y] in snake:
                    print('o', end=' ')
                else:
                    print('.', end=' ')
            print()
        print(f'Snake Direction: {direction}')
        if direction_change:
            direction = 'down' if direction == 'up' else 'up'
            direction_change = False
        command = input('Enter "q" to quit or press enter to continue: ')
        if command == 'q':
            break
        elif command == 'w':
            direction = 'up'
            direction_change = True
        elif command == 's':
            direction = 'down'
            direction_change = True
        elif command == 'a':
            direction = 'left'
            direction_change = True
        elif command == 'd':
            direction = 'right'
            direction_change = True
        if not check_collision(snake, direction):
            snake = update_trail(snake, direction)
            if direction == 'down' and snake[-1][1] == 19:
                direction = 'right'
            elif direction == 'right' and snake[-1][0] == 19:
                direction = 'up'
            elif direction == 'up' and snake[-1][0] == 0:
                direction = 'left'
            elif direction == 'left' and snake[-1][1] == 0:
                direction = 'down'
            if [snake[-1][0], snake[-1][1]] in snake[:-1] and direction == 'down':
                direction = 'right'
            elif [snake[-1][0], snake[-1][1]] in snake[:-1] and direction == 'right':
                direction = 'up'
            elif [snake[-1][0], snake[-1][1]] in snake[:-1] and direction == 'up':
                direction = 'left'
            elif [snake[-1][0], snake[-1][1]] in snake[:-1] and direction == 'left':
                direction = 'down'
            time.sleep(0.5)
        time.sleep(0.5)

previous_trail = []
game_loop()