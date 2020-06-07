from copy import deepcopy


class Graph:

    # реалізація графа

    def __init__(self, vertex_num: int):
        self._vertex_num = vertex_num
        self._matrix = list()
        for i in range(vertex_num):
            self._matrix.append(list())
            for j in range(vertex_num):
                self._matrix[i].append(float('inf'))

    def addEdge(self, a: int, b: int, c: int):
        self._matrix[a][b] = c

    def __str__(self):
        string = ''
        for i in range(len(self._matrix)):
            for j in range(len(self._matrix)):
                if self._matrix[i][j]:
                    string += str(i) + "-" + str(j) + "\n"
        return string

    # алгоритм найближчого сусіда
    def closestNeighbour(self, first, start=-1, best=0, closed=list()):
        # вихід з рекурсії
        if start is None:
            way = ""
            for i in closed:
                way += str(i) + "->"
            last = closed[-1]
            return way + str(first) + " range:" + str(best + self._matrix[last][first])
        if start == -1:
            start = first
        best_way = float('inf')
        best_vertex = None
        # якщо всі вершини "закриті", то в змінну start буде передано None
        for i in range(len(self._matrix[start])):
            if i not in closed and self._matrix[start][i] < best_way:
                best_way = self._matrix[start][i]
                best_vertex = i
        closed.append(start)
        if best_way != float('inf'):
            best += best_way
        return self.closestNeighbour(first, best_vertex, best, closed)

    def make_path(self, start, best_pairs, result=0, main_string=''):
        # в кінці роботи наступного алгоритму ми матимемо список найкращих шляхів, цей метод потрібен для формування
        # відповіді
        if len(best_pairs) == 0:
            return main_string + main_string[0] + " range:" + str(result)
        next_start = None
        for i in range(len(best_pairs)):
            if best_pairs[i][0] == start:
                result += self._matrix[best_pairs[i][0]][best_pairs[i][1]]
                main_string += str(start) + "->"
                next_start = best_pairs[i][1]
                best_pairs.pop(i)
                break
        return self.make_path(next_start, best_pairs, result, main_string)

    def branch_and_bounds(self, start, size=0, matrix=None, best_pairs=list()):
        if matrix is None:
            matrix = deepcopy(self._matrix)
            size = len(matrix)
        # вихід з рекурсії, якщо матриця 2 на 2, то далі алгоритм не працюватиме, тому необхідно додати 2 шляхи,
        # серед тих, які залишаються в цій матриці і закінчити рекурсію
        if size == 2:
            prob_best_pairs=[]
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if matrix[i][j] != float('inf'):
                        prob_best_pairs.append([i, j])
            if len(prob_best_pairs) != 2:
                if prob_best_pairs[0][1] == prob_best_pairs[1][1] or prob_best_pairs[0][0] == prob_best_pairs[1][0]:
                    prob_best_pairs.pop(-2)
                else:
                    prob_best_pairs.pop(-1)
            for i in prob_best_pairs:
                best_pairs.append(i)
            return self.make_path(start, best_pairs)
        # пошук мінімальних значень по рядах для редукції по рядах
        min_rows = [float('inf')] * len(matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                min_rows[i] = min(min_rows[i], matrix[i][j])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if min_rows[i] != float('inf'):
                    matrix[i][j] -= min_rows[i]
        # пошук мінімальних значень по стовпцях для редукції по стовпцях
        min_cols = [float('inf')] * len(matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                min_cols[i] = min(min_cols[i], matrix[j][i])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if min_cols[i] != float('inf'):
                    matrix[j][i] -= min_cols[i]
        # оцінка нулів та пошук нуля з найбільшою оцінкою
        score = []
        for i in range(len(matrix)):
            score.append(list())
            for j in range(len(matrix)):
                score[i].append(float('inf'))
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:
                    minimal_r = float('inf')
                    minimal_c = float('inf')
                    for k in range(len(matrix)):
                        if k != j:
                            minimal_c = min(minimal_c, matrix[i][k])
                        if k != i:
                            minimal_r = min(minimal_r, matrix[k][j])
                    score[i][j] = minimal_c + minimal_r
        maximal = 0
        best_pair = [-1, -1]
        for i in range(len(score)):
            for j in range(len(score)):
                if score[i][j] != float('inf') and score[i][j] >= maximal:
                    best_pair[0] = i
                    best_pair[1] = j
        matrix[best_pair[1]][best_pair[0]] = float('inf')
        # редукція матриці (прибирання стовпця і рядка, яким належить нуль з найкращим рахунком) та редукція шляху,
        # який є оборотним для нуля з найбільшим рахунком
        for j in range(len(matrix)):
            matrix[best_pair[0]][j] = float('inf')
            matrix[j][best_pair[1]] = float('inf')
        best_pairs.append(best_pair)
        # рекурсивний виклик методу для вже редукованої матриціі
        return self.branch_and_bounds(start, size - 1, matrix, best_pairs)


if __name__ == "__main__":
    graph = Graph(4)
    graph.addEdge(0, 1, 1)
    graph.addEdge(0, 2, 1)
    graph.addEdge(0, 3, 1)
    graph.addEdge(1, 2, 11)
    graph.addEdge(1, 0, 1)
    graph.addEdge(1, 3, 8)
    graph.addEdge(2, 0, 12)
    graph.addEdge(2, 1, 1)
    graph.addEdge(2, 3, 10)
    graph.addEdge(3, 0, 11)
    graph.addEdge(3, 1, 8)
    graph.addEdge(3, 2, 10)
    print(graph.closestNeighbour(0))
    print(graph.branch_and_bounds(0))
