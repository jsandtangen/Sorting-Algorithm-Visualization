import pygame
import random
import math

# Initialiserer Pygame-biblioteket
pygame.init()

# Definerer en klasse for å håndtere alle tegneparametere for visualiseringen
class DrawInformation:
    # Definerer farger som RGB-tuple
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    # Definerer en liste med farger for gradienteffekt
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # Definerer skrifttyper for teksten
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    # Klargjør padding for sidene og toppen av vinduet
    SIDE_PAD = 100
    TOP_PAD = 150

    # Konstruktør for å initialisere vinduet og liste
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        # Setter opp Pygame-vinduet
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    # Metode for å sette og oppdatere listen som skal visualiseres
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)  # Finner minimum verdien i listen
        self.max_val = max(lst)  # Finner maksimum verdien i listen

        # Beregner bredde og høyde på blokkene som representerer elementene i listen
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2  # Beregner startposisjonen på x-aksen


# Funksjon for å tegne vinduet med informasjon om sortering
def draw(draw_info, algo_name, ascending, comparisons, swaps):
    # Fyller bakgrunnen med hvit farge
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Tegner tittelen på vinduet
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    # Tegner kontrollinformasjon
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    # Tegner informasjon om sorteringsalgoritmer
    sorting = draw_info.FONT.render("I - Insertion | B - Bubble | Q - Quick | M - Merge | S - Selection", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    # Tegner statistikk for antall sammenligninger og bytter
    stats = draw_info.FONT.render(f"Comparisons: {comparisons}, Swaps: {swaps}", 1, draw_info.BLACK)
    draw_info.window.blit(stats, (10, 10))

    # Tegner listen av tall ved hjelp av tegnefunksjonen
    draw_list(draw_info)
    pygame.display.update()  # Oppdaterer vinduet

# Funksjon for å tegne listen i vinduet
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst  # Henter listen

    # Hvis klaring av bakgrunn er nødvendig, tegner en rektangel for å fjerne tidligere tegning
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Tegner hver blokk i listen
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width  # Beregner x-posisjon
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height  # Beregner y-posisjon

        color = draw_info.GRADIENTS[i % 3]  # Får farge ved hjelp av gradient

        # Endrer farge hvis posisjonen er spesifisert
        if i in color_positions:
            color = color_positions[i]

        # Tegner rektanglet for hver blokk
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    # Oppdaterer bakgrunnen hvis nødvendig
    if clear_bg:
        pygame.display.update()

# Funksjon for å generere en tilfeldig liste
def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)  # Genererer tilfeldig tall
        lst.append(val)  # Legger til tallet i listen
    return lst  # Returnerer den genererte listen

# Bubble sort algoritme
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst  # Henter listen
    comparisons = 0  # Teller sammenligninger
    swaps = 0  # Teller bytter
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            comparisons += 1  # Øker sammenligningsantallet
            num1 = lst[j]
            num2 = lst[j + 1]

            # Sjekker om bytte er nødvendig i henhold til sorteringens rekkefølge
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                swaps += 1  # Øker bytteantallet
                lst[j], lst[j + 1] = lst[j + 1], lst[j]  # Utfører bytte
                # Tegner listen med fargede blokker for de som er byttet
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True  # Lar programmet pause for å vise endringene

    return lst  # Returnerer sortert liste

# Insertion sort algoritme
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    comparisons = 0
    swaps = 0
    for i in range(1, len(lst)):
        current = lst[i]  # Nåværende verdi å sette i riktig posisjon
        while True:
            # Sjekker om sortering logikken holder
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            comparisons += 1  # Øker sammenligningsantallet

            # Bryter ut av løkken hvis sorteringen er på plass
            if not ascending_sort and not descending_sort:
                break

            # Flytter tallene opp for å lage plass for det nåværende tallet
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            swaps += 1
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True  # Kort pause for å vise endringer
            
    return lst  # Returnerer sortert liste

# Quick sort algoritme
def quick_sort(draw_info, ascending=True):
    yield from quick_sort_helper(draw_info.lst, 0, len(draw_info.lst) - 1, draw_info, ascending)

# Hjelpefunksjon for å håndtere quick sort
def quick_sort_helper(lst, low, high, draw_info, ascending):
    if low < high:
        pi, comparisons, swaps = partition(lst, low, high, draw_info, ascending)  # Få parti for listen
        yield from quick_sort_helper(lst, low, pi - 1, draw_info, ascending)  # Sorter venstre del
        yield from quick_sort_helper(lst, pi + 1, high, draw_info, ascending)  # Sorter høyre del

# Partisjonerer listen for Quick Sort
def partition(lst, low, high, draw_info, ascending):
    pivot = lst[high]  # Velger pivotelementet
    i = low - 1
    comparisons = 0
    swaps = 0

    # Går gjennom og organiserer elementene
    for j in range(low, high):
        comparisons += 1  # Øker sammenligningsantallet
        if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]  # Utfører bytte
            swaps += 1
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)  # Tegner endringene
            yield True

    lst[i + 1], lst[high] = lst[high], lst[i + 1]  # Setter pivotelementet på riktig plass
    swaps += 1
    draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
    yield True
    
    return i + 1, comparisons, swaps  # Returnerer indeks og teller

# Merge sort algoritme
def merge_sort(draw_info, ascending=True):
    yield from merge_sort_helper(draw_info.lst, 0, len(draw_info.lst) - 1, draw_info, ascending)

# Hjelpefunksjon for merge sort
def merge_sort_helper(lst, left, right, draw_info, ascending):
    if left < right:
        mid = (left + right) // 2  # Finn midten av listen
        yield from merge_sort_helper(lst, left, mid, draw_info, ascending)  # Sorter venstre halvdel
        yield from merge_sort_helper(lst, mid + 1, right, draw_info, ascending)  # Sorter høyre halvdel
        yield from merge(lst, left, mid, right, draw_info, ascending)  # Merge de to halvdelene

# Merge to delte lister til en sortert liste
def merge(lst, left, mid, right, draw_info, ascending):
    left_copy = lst[left:mid + 1]  # Kopierer venstre halvdel
    right_copy = lst[mid + 1:right + 1]  # Kopierer høyre halvdel

    left_index = right_index = 0  # Initialiserer indeksene for kopiene
    sorted_index = left  # Indeksen for den sorterte listen

    # Sammenligner elementene i venstre og høyre halvdel
    while left_index < len(left_copy) and right_index < len(right_copy):
        # Sjekker forholdet for sortering
        if (left_copy[left_index] <= right_copy[right_index] and ascending) or \
           (left_copy[left_index] > right_copy[right_index] and not ascending):
            lst[sorted_index] = left_copy[left_index]
            left_index += 1
        else:
            lst[sorted_index] = right_copy[right_index]
            right_index += 1
        sorted_index += 1
        draw_list(draw_info, {}, True)  # Tegner den nye listen
        yield True

    # Fortsetter å sette inn resterende elementer fra venstre halvdel
    while left_index < len(left_copy):
        lst[sorted_index] = left_copy[left_index]
        left_index += 1
        sorted_index += 1
        draw_list(draw_info, {}, True)
        yield True

    # Fortsetter å sette inn resterende elementer fra høyre halvdel
    while right_index < len(right_copy):
        lst[sorted_index] = right_copy[right_index]
        right_index += 1
        sorted_index += 1
        draw_list(draw_info, {}, True)
        yield True

# Selection sort algoritme
def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst  # Henter listen
    comparisons = 0  # Teller sammenligninger
    swaps = 0  # Teller bytter
    for i in range(len(lst)):
        min_idx = i  # Anta at det nåværende elementet er det minste
        for j in range(i + 1, len(lst)):
            comparisons += 1  # Øker sammenligningsantallet
            # Sjekker om det nåværende elementet er mindre
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j  # Oppdaterer min_idx
            
        # Hvis det er nødvendig med bytte, gjør det
        if min_idx != i:
            swaps += 1
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)  # Tegner endringene
            yield True
            
    return lst  # Returnerer sortert liste

# Hovedfunksjon som kjører programmet
def main():
    run = True  # Flag for å kjøre hovedløyfen
    clock = pygame.time.Clock()  # Klokke for å styre FPS

    n = 50  # Initial størrelse på listen
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)  # Genererer startliste
    draw_info = DrawInformation(1400, 600, lst)  # Oppretter objekt for å håndtere tegning
    sorting = False  # Flag for å sjekke om sortering pågår
    ascending = True  # Avanseringsretning
    comparisons = 0  # Sammenligninger
    swaps = 0  # Bytter

    sorting_algorithm = bubble_sort  # Start med Bubble Sort
    sorting_algo_name = "Bubble Sort"  # Navn på sorteringsalgoritmen
    sorting_algorithm_generator = None  # Generator for sorteringsalgoritmen

    while run:
        clock.tick(60)  # Setter opp FPS

        if sorting:
            try:
                next(sorting_algorithm_generator)  # Kjør neste steg i sorteringen
            except StopIteration:
                sorting = False  # Hvis sorteringen er ferdig, sett flagget til False
        else:
            # Tegner informasjon i vinduet
            draw(draw_info, sorting_algo_name, ascending, comparisons, swaps)

        for event in pygame.event.get():  # Går gjennom alle Pygame-hendelser
            if event.type == pygame.QUIT:  # Sjekker for lukking av vindu
                run = False

            if event.type != pygame.KEYDOWN:  # Sjekker for tastetrykk
                continue

            # Håndterer forskjellige tastetrykk
            if event.key == pygame.K_r:  # R - Tilbakestill listen
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                comparisons = 0
                swaps = 0
            elif event.key == pygame.K_SPACE and not sorting:  # SPACE - Start sortering
                sorting = True
                comparisons = 0
                swaps = 0
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:  # A - Sorter i stigende
                ascending = True
            elif event.key == pygame.K_d and not sorting:  # D - Sorter i synkende
                ascending = False
            elif event.key == pygame.K_i and not sorting:  # I - Velg Insertion Sort
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:  # B - Velg Bubble Sort
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_q and not sorting:  # Q - Velg Quick Sort
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_m and not sorting:  # M - Velg Merge Sort
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_s and not sorting:  # S - Velg Selection Sort
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

    pygame.quit()  # Avslutt Pygame når programmet er ferdig

# Sørger for at hovedfunksjonen kjører når skriptet startes
if __name__ == "__main__":
    main()
