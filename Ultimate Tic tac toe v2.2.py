import pygame

darkmode = "n"
if "y" in darkmode:
    BLACK = (255, 255, 255)
    WHITE = (0, 0, 0)
    GREEN = (255, 0, 255)
    RED = (0, 255, 255)
    BLUE = (255, 255, 0)
else:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 255, 0)


amtrow = 9
amtcol = 9
# HEIGHT AND WIDTH NEED TO BE LARGER THAN MARGIN !!!
HEIGHT = 75
WIDTH = 75
MARGIN = 5
playcolour = [25, 250, 100]
grid = []
TotalGrid = []
totxsize = ((WIDTH + MARGIN) * amtrow) + 5 * MARGIN
totysize = ((HEIGHT + MARGIN) * amtcol) + 5 * MARGIN


def ResizePlayBox(playrect, allowedx, allowedy):
    if allowedx == -1 and allowedy == -1:
        playrect[0] = MARGIN
        playrect[1] = MARGIN
        playrect[2] = (3 * WIDTH + 4 * MARGIN) * 3
        playrect[3] = (3 * HEIGHT + 4 * MARGIN) * 3
    else:
        playrect[1] = allowedy * (MARGIN + HEIGHT) + 2 * MARGIN + ((allowedy // 3 - 1) * MARGIN)
        playrect[0] = allowedx * (MARGIN + WIDTH) + 2 * MARGIN + ((allowedx // 3 - 1) * MARGIN)
        playrect[2] = (MARGIN + WIDTH) * 3 + MARGIN
        playrect[3] = (MARGIN + HEIGHT) * 3 + MARGIN


def NextBox(Ccords, TotalGrid):
    boxFull = False
    if TotalGrid[Ccords[0] % 3][Ccords[1] % 3] != 0:
        return (-1, -1)
    else:
        return ((Ccords[0] % 3) * 3, (Ccords[1] % 3) * 3)


def SetWin(Grid, Team, TotalGrid):
    for x in range(amtrow):
        for y in range(amtcol):
            Grid[x][y] = Team
    for x in TotalGrid:
        for y in x:
            y = Team


def winSetter(OC, Team, Grid, TotalGrid):
    TotalGrid[OC[0] // 3][OC[1] // 3] = Team
    for x in range((OC[0] // 3) * 3, (OC[0] // 3) * 3 + 3):
        for y in range((OC[1] // 3) * 3, (OC[1] // 3) * 3 + 3):
            Grid[x][y] = Team


def GridReset(Grid):
    for x in range(amtrow):
        for y in range(amtcol):
            Grid[x][y] = 0


def PrintGrid(Grid):
    for x in Grid:
        print(x)
    print("")


def winCalc(Grid, TotalGrid):
    for x in range(amtrow):
        for y in range(amtcol):
            if Grid[x][y] != 0:
                if y < 6 and y > 1 and x < 6 and x > 1:
                    if Grid[x - 2][y] == Grid[x - 1][y] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                    if Grid[x][y - 2] == Grid[x][y - 1] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                    if Grid[x - 2][y - 2] == Grid[x - 1][y - 1] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                    if Grid[x + 2][y - 2] == Grid[x + 1][y - 1] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                if x > 1:
                    if Grid[x - 2][y] == Grid[x - 1][y] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                if y > 1:
                    if Grid[x][y - 2] == Grid[x][y - 1] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                if x > 1 and y > 1:
                    if Grid[x - 2][y - 2] == Grid[x - 1][y - 1] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
                    if Grid[x + 2][y - 2] == Grid[x + 1][y - 1] == Grid[x][y] != 0:
                        SetWin(Grid, Grid[x][y], TotalGrid)
                        return True
    return False


def CheckFull(Grid):
    for x in range(amtrow):
        for y in range(amtcol):
            if Grid[x][y] == 0:
                return False
    return True


def makemove(TotalGrid, Grid, player, Ccords):
    x = Ccords[0] // 3
    y = Ccords[1] // 3
    Grid[x][y] = player
    if winCalc(Grid, TotalGrid):
        return
    if CheckFull(Grid[x]):
        for row in Grid:
            if 0 in row:
                return
        for row in TotalGrid:
            if 0 in row:
                return
        print("DRAW!")
        GridReset(Grid)
        GridReset(TotalGrid)


def main():
    pygame.init()

    WINDOW_SIZE = [totxsize, totysize]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Ultimate Tic Tac Toe")

    done = False

    clock = pygame.time.Clock()

    for row in range(amtrow):
        grid.append([])
        for column in range(amtcol):
            grid[row].append(0)

    for row in range(3):
        TotalGrid.append([])
        for column in range(3):
            TotalGrid[row].append(0)

    player = 1

    playrect = [MARGIN, MARGIN, WIDTH, HEIGHT]

    Resized = False
    Ccords = (-1, -1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if not Resized:
                    ResizePlayBox(playrect, column, row)
                    Resized = True
                else:
                    if row < 3 and column < 3:
                        Ccords = NextBox((column, row), TotalGrid)
                    else:
                        Ccords = (-1, -1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    GridReset(grid)
                    GridReset(TotalGrid)

        if player == 2 and Ccords != (-1, -1):
            # Implementação do algoritmo Minimax para a IA

            def minimax(grid, depth, maximizing_player):
                if depth == 0 or winCalc(grid, TotalGrid) or CheckFull(grid):
                    if winCalc(grid, TotalGrid):
                        return -1
                    elif CheckFull(grid):
                        return 0
                    else:
                        return 1
                if maximizing_player:
                    max_eval = float('-inf')
                    for x in range(amtrow):
                        for y in range(amtcol):
                            if grid[x][y] == 0:
                                grid[x][y] = player
                                eval = minimax(grid, depth - 1, False)
                                grid[x][y] = 0
                                max_eval = max(eval, max_eval)
                    return max_eval
                else:
                    min_eval = float('inf')
                    for x in range(amtrow):
                        for y in range(amtcol):
                            if grid[x][y] == 0:
                                grid[x][y] = 3 - player
                                eval = minimax(grid, depth - 1, True)
                                grid[x][y] = 0
                                min_eval = min(eval, min_eval)
                    return min_eval

            best_score = float('-inf')
            best_move = None
            for x in range(amtrow):
                for y in range(amtcol):
                    if grid[x][y] == 0:
                        grid[x][y] = player
                        score = minimax(grid, 2, False)
                        grid[x][y] = 0
                        if score > best_score:
                            best_score = score
                            best_move = (x, y)

            if best_move:
                makemove(TotalGrid, grid, player, best_move)
                player = 3 - player

        screen.fill(BLACK)

        for row in range(amtrow):
            for column in range(amtcol):
                color = WHITE
                if grid[row][column] == 1:
                    color = RED
                elif grid[row][column] == 2:
                    color = BLUE
                pygame.draw.rect(
                    screen,
                    color,
                    [
                        (MARGIN + WIDTH) * column + MARGIN,
                        (MARGIN + HEIGHT) * row + MARGIN,
                        WIDTH,
                        HEIGHT,
                    ],
                )

        pygame.draw.rect(screen, GREEN, playrect)
        pygame.draw.rect(screen, GREEN, [MARGIN, MARGIN, WIDTH, HEIGHT])

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
