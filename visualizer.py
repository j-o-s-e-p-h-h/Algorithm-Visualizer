import math
import random

import pygame


pygame.init()


class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BACKGROUND_COLOR = WHITE
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont("comicsans", 30)
    LARGE_FONT = pygame.font.SysFont("comicsans", 40)

    side_pad = 100
    top_pad = 190

    def __init__(self, width, height, values):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(values)

    def set_list(self, values):
        self.list = values
        self.max_value = max(values)
        self.min_value = min(values)

        # Scale bar width and height from the current list so any reset still fits the window.
        value_range = self.max_value - self.min_value or 1
        self.block_width = max(1, round((self.width - self.side_pad) / len(values)))
        self.block_height = max(1, math.floor((self.height - self.top_pad) / value_range))
        self.start_x_coordinate = self.side_pad // 2


def generate_starting_list(length, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(length)]


def should_swap(first, second, ascending):
    return (first > second and ascending) or (first < second and not ascending)


def draw(draw_info, algorithm_name, ascending, sorting, highlights=None):
    if highlights is None:
        highlights = {}

    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render("Sorting Algorithm Visualizer", True, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start / Pause", True, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    direction = draw_info.FONT.render("A - Ascending | D - Descending", True, draw_info.BLACK)
    draw_info.window.blit(direction, (draw_info.width / 2 - direction.get_width() / 2, 80))

    algorithms = draw_info.FONT.render("B - Bubble | I - Insertion | S - Selection | C - Cocktail", True, draw_info.BLACK)
    draw_info.window.blit(algorithms, (draw_info.width / 2 - algorithms.get_width() / 2, 115))

    algorithms_two = draw_info.FONT.render("M - Merge | Q - Quick", True, draw_info.BLACK)
    draw_info.window.blit(algorithms_two, (draw_info.width / 2 - algorithms_two.get_width() / 2, 150))

    status_text = f"{algorithm_name} | {'Ascending' if ascending else 'Descending'}"
    if sorting:
        status_text += " | Sorting..."
    else:
        status_text += " | Ready"

    status = draw_info.FONT.render(status_text, True, draw_info.BLACK)
    draw_info.window.blit(status, (draw_info.width / 2 - status.get_width() / 2, 185))

    draw_list(draw_info, highlights)
    pygame.display.update()


def draw_list(draw_info, color_positions=None):
    if color_positions is None:
        color_positions = {}

    for index, value in enumerate(draw_info.list):
        x = draw_info.start_x_coordinate + index * draw_info.block_width
        # Higher values need to start closer to the top so the bar grows upward from the bottom edge.
        y = draw_info.height - (value - draw_info.min_value) * draw_info.block_height

        color = draw_info.GRADIENTS[index % len(draw_info.GRADIENTS)]
        if index in color_positions:
            color = color_positions[index]

        pygame.draw.rect(
            draw_info.window,
            color,
            (x, y, draw_info.block_width, draw_info.height),
        )


def bubble_sort(draw_info, ascending=True):
    values = draw_info.list

    for i in range(len(values) - 1):
        for j in range(len(values) - 1 - i):
            if should_swap(values[j], values[j + 1], ascending):
                values[j], values[j + 1] = values[j + 1], values[j]
                # Each yield returns the bars to highlight for a single animation step.
                yield {j: draw_info.GREEN, j + 1: draw_info.RED}
            else:
                yield {j: draw_info.YELLOW, j + 1: draw_info.GREEN}


def insertion_sort(draw_info, ascending=True):
    values = draw_info.list

    for i in range(1, len(values)):
        current_value = values[i]
        j = i

        while j > 0 and should_swap(values[j - 1], current_value, ascending):
            values[j] = values[j - 1]
            yield {j - 1: draw_info.YELLOW, j: draw_info.RED}
            j -= 1

        values[j] = current_value
        yield {j: draw_info.GREEN}


def selection_sort(draw_info, ascending=True):
    values = draw_info.list

    for i in range(len(values)):
        selected_index = i

        for j in range(i + 1, len(values)):
            if should_swap(values[selected_index], values[j], ascending):
                selected_index = j

            yield {i: draw_info.GREEN, selected_index: draw_info.YELLOW, j: draw_info.RED}

        if selected_index != i:
            values[i], values[selected_index] = values[selected_index], values[i]
            yield {i: draw_info.GREEN, selected_index: draw_info.RED}


def cocktail_sort(draw_info, ascending=True):
    values = draw_info.list
    start = 0
    end = len(values) - 1
    swapped = True

    while swapped:
        swapped = False

        for i in range(start, end):
            if should_swap(values[i], values[i + 1], ascending):
                values[i], values[i + 1] = values[i + 1], values[i]
                swapped = True
                yield {i: draw_info.GREEN, i + 1: draw_info.RED}
            else:
                yield {i: draw_info.YELLOW, i + 1: draw_info.GREEN}

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end - 1, start - 1, -1):
            if should_swap(values[i], values[i + 1], ascending):
                values[i], values[i + 1] = values[i + 1], values[i]
                swapped = True
                yield {i: draw_info.GREEN, i + 1: draw_info.RED}
            else:
                yield {i: draw_info.YELLOW, i + 1: draw_info.GREEN}

        start += 1


def merge_sort(draw_info, ascending=True):
    values = draw_info.list
    # The recursive helper still yields intermediate states, so merge sort animates one merge at a time.
    yield from merge_sort_range(values, 0, len(values) - 1, ascending, draw_info)


def merge_sort_range(values, left, right, ascending, draw_info):
    if left >= right:
        return

    middle = (left + right) // 2
    yield from merge_sort_range(values, left, middle, ascending, draw_info)
    yield from merge_sort_range(values, middle + 1, right, ascending, draw_info)
    yield from merge(values, left, middle, right, ascending, draw_info)


def merge(values, left, middle, right, ascending, draw_info):
    left_values = values[left : middle + 1]
    right_values = values[middle + 1 : right + 1]

    left_index = 0
    right_index = 0
    merged_index = left

    while left_index < len(left_values) and right_index < len(right_values):
        if (left_values[left_index] <= right_values[right_index] and ascending) or (
            left_values[left_index] >= right_values[right_index] and not ascending
        ):
            values[merged_index] = left_values[left_index]
            left_index += 1
        else:
            values[merged_index] = right_values[right_index]
            right_index += 1

        yield {merged_index: draw_info.GREEN, left: draw_info.YELLOW, right: draw_info.RED}
        merged_index += 1

    while left_index < len(left_values):
        values[merged_index] = left_values[left_index]
        yield {merged_index: draw_info.GREEN}
        left_index += 1
        merged_index += 1

    while right_index < len(right_values):
        values[merged_index] = right_values[right_index]
        yield {merged_index: draw_info.GREEN}
        right_index += 1
        merged_index += 1


def quick_sort(draw_info, ascending=True):
    values = draw_info.list
    yield from quick_sort_range(values, 0, len(values) - 1, ascending, draw_info)


def quick_sort_range(values, low, high, ascending, draw_info):
    if low >= high:
        return

    pivot_index = yield from partition(values, low, high, ascending, draw_info)
    yield from quick_sort_range(values, low, pivot_index - 1, ascending, draw_info)
    yield from quick_sort_range(values, pivot_index + 1, high, ascending, draw_info)


def partition(values, low, high, ascending, draw_info):
    # Quick sort keeps everything before "border" on the correct side of the pivot.
    pivot = values[high]
    border = low

    for j in range(low, high):
        yield {high: draw_info.YELLOW, j: draw_info.RED, border: draw_info.GREEN}

        if (values[j] <= pivot and ascending) or (values[j] >= pivot and not ascending):
            values[border], values[j] = values[j], values[border]
            yield {border: draw_info.GREEN, j: draw_info.RED}
            border += 1

    values[border], values[high] = values[high], values[border]
    yield {border: draw_info.GREEN, high: draw_info.RED}
    return border


SORTING_ALGORITHMS = {
    pygame.K_b: ("Bubble Sort", bubble_sort),
    pygame.K_i: ("Insertion Sort", insertion_sort),
    pygame.K_s: ("Selection Sort", selection_sort),
    pygame.K_c: ("Cocktail Sort", cocktail_sort),
    pygame.K_m: ("Merge Sort", merge_sort),
    pygame.K_q: ("Quick Sort", quick_sort),
}


def main():
    clock = pygame.time.Clock()

    list_size = 50
    min_value = 0
    max_value = 100

    values = generate_starting_list(list_size, min_value, max_value)
    draw_info = DrawInformation(800, 600, values)

    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None
    highlights = {}

    run = True
    while run:
        clock.tick(30)

        if sorting and sorting_algorithm_generator is not None:
            try:
                # Advance the generator one step per frame so the algorithm stays animated instead of finishing instantly.
                highlights = next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                sorting_algorithm_generator = None
                highlights = {}
        else:
            highlights = {}

        draw(draw_info, sorting_algorithm_name, ascending, sorting, highlights)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                values = generate_starting_list(list_size, min_value, max_value)
                draw_info.set_list(values)
                sorting = False
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_SPACE:
                if sorting:
                    sorting = False
                else:
                    if sorting_algorithm_generator is None:
                        # Build a fresh generator whenever we start or restart a sort.
                        sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                    sorting = True
            elif event.key == pygame.K_a and not sorting:
                ascending = True
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key == pygame.K_d and not sorting:
                ascending = False
                sorting_algorithm_generator = None
                highlights = {}
            elif event.key in SORTING_ALGORITHMS and not sorting:
                sorting_algorithm_name, sorting_algorithm = SORTING_ALGORITHMS[event.key]
                sorting_algorithm_generator = None
                highlights = {}

    pygame.quit()


if __name__ == "__main__":
    main()
