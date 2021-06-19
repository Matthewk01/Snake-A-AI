import heapq


def get_moves():
    return [(0, 1), (1, 0), (0, -1), (-1, 0)]


def update_snake_tail(snake_tail, position):
    new_snake_tail = snake_tail.copy()
    if snake_tail:
        new_snake_tail.popleft()
    new_snake_tail.append((position[0] * 51, position[1] * 51))
    return new_snake_tail


class PlanState:
    def __init__(self, value, current_position, current_snake_tail, current_seen, current_reverse_path,
                 current_distance):
        self.value = value
        self.position = current_position
        self.snake_tail = current_snake_tail
        self.seen = current_seen
        self.reverse_path = current_reverse_path
        self.distance = current_distance

    def __lt__(self, other):
        return self.value < other.value


class SnakeAi:
    def __init__(self, board, snake, apples):
        self.board = board
        self.snake = snake
        self.apples = apples
        self.plan = []

    def make_plan(self):
        snake_current_position = (self.snake.rect.x // 51, self.snake.rect.y // 51)
        apple_position = self.apples[0].rect.x // 51, self.apples[0].rect.y // 51
        snake_movement_plan = self.aStar(snake_current_position, apple_position, self.snake.tail)
        if not snake_movement_plan:
            return []

        plan = []
        position_tmp = snake_movement_plan[apple_position]
        while True:
            plan.append(position_tmp[1])
            if position_tmp[0] == snake_current_position:
                break
            position_tmp = snake_movement_plan[position_tmp[0]]
        # List of actions for snake
        self.plan = plan
        return plan

    def dfs_search(self, from_position, reverse_path, seen, goal_position, snake_tail):
        stack = [from_position]

        while stack:
            current_position = stack.pop()
            if current_position == goal_position:
                return True
            for move in get_moves():
                next_position = (current_position[0] + move[0], current_position[1] + move[1])
                if next_position not in seen and self.is_move_valid(next_position, snake_tail):
                    seen.add(next_position)
                    reverse_path[next_position] = (current_position, move)
                    stack.append(next_position)
        return False

    def bfs_search(self, from_position, reverse_path, seen, goal_position, snake_tail):
        queue = [(from_position, snake_tail)]
        count = 0
        while queue:
            count += 1
            if count > 40:
                return True
            current_state = queue.pop(0)
            current_position = current_state[0]
            current_snake_tail = current_state[1]
            if current_position == goal_position:
                return True
            for move in get_moves():
                next_position = (current_position[0] + move[0], current_position[1] + move[1])
                next_snake_tail = update_snake_tail(snake_tail, next_position)
                if next_position not in seen and self.is_move_valid(next_position, current_snake_tail):
                    seen.add(next_position)
                    reverse_path[next_position] = (current_position, move)
                    queue.append((next_position, next_snake_tail))
        return False

    def aStar(self, from_position, goal_position, snake_tail):
        priorityQueue = []
        distance = {from_position: 0}
        reverse_path = {}
        seen = set(from_position)
        init_state = PlanState(self.get_manhattan_distance_to_apple(from_position), from_position, snake_tail, seen,
                               reverse_path, distance)
        heapq.heappush(priorityQueue, init_state)
        WEIGHT = 1

        while len(priorityQueue):
            current_state = heapq.heappop(priorityQueue)
            current_position = current_state.position
            current_snake_tail = current_state.snake_tail
            current_seen = current_state.seen
            current_reverse_path = current_state.reverse_path
            current_distance = current_state.distance
            if current_position == goal_position:
                # if can get out return
                reverse_path_tmp = {}
                seen_tmp = set(current_position)
                if current_snake_tail:
                    end_of_tail_position = (current_snake_tail[0][0] // 51, current_snake_tail[0][1] // 51)
                    if self.bfs_search(current_position, reverse_path_tmp, seen_tmp, end_of_tail_position,
                                       current_snake_tail.copy()):
                        return current_reverse_path
                else:
                    return current_reverse_path
            for move in get_moves():
                next_position = (current_position[0] + move[0], current_position[1] + move[1])
                if self.is_move_valid(next_position, current_snake_tail):
                    next_snake_tail = update_snake_tail(current_snake_tail, next_position)
                    next_reverse_path = current_reverse_path.copy()
                    next_distance = current_distance.copy()
                    if next_position not in current_seen:
                        next_seen = current_seen.copy()
                        next_distance[next_position] = next_distance[current_position] + WEIGHT
                        next_reverse_path[next_position] = (current_position, move)
                        next_seen.add(next_position)
                        next_state = PlanState(self.get_manhattan_distance_to_apple(next_position) + next_distance[
                            next_position], next_position, next_snake_tail, next_seen,
                                               next_reverse_path, next_distance)
                        heapq.heappush(priorityQueue, next_state)
                    # Relaxation
                    elif current_distance[next_position] > current_distance[current_position] + WEIGHT:
                        next_distance[next_position] = next_distance[current_position] + WEIGHT
                        next_reverse_path[next_position] = (current_position, move)
                        next_state = PlanState(self.get_manhattan_distance_to_apple(next_position) + next_distance[
                            next_position], next_position, next_snake_tail, current_seen,
                                               next_reverse_path, next_distance)
                        heapq.heappush(priorityQueue, next_state)
        return []

    def get_manhattan_distance_to_apple(self, from_position):
        apple_position = self.apples[0].rect.x // 51, self.apples[0].rect.y // 51
        return abs(from_position[0] - apple_position[0]) + abs(from_position[1] - apple_position[1])

    def is_move_valid(self, move, snake_tail):
        x, y = move
        if not self.board.is_position_valid(move):
            return False
        if (x * 51, y * 51) in snake_tail:
            return False
        return True

    def update(self):
        next_direction = (1, 0)
        if not self.plan:
            self.make_plan()
        # If plan can't be found go to first safe possible position
        if not self.plan:
            for move in get_moves():
                next_position = (self.snake.rect.x // 51 + move[0], self.snake.rect.y // 51 + move[1])
                if self.is_move_valid(next_position, self.snake.tail):
                    next_direction = move
        else:
            next_direction = self.plan.pop()
        self.snake.change_direction(next_direction)
