import argparse
import networkx as nx

class Solution:
  filename_real_input = 'real_input.txt'
  filename_test_input = 'test_input.txt'
  
  def __init__(self, test=False):
    self.filename = self.filename_test_input if test else self.filename_real_input
    self.file = open(self.filename,'r').read()
    self.lines = self.file.splitlines()

  def create_graph(self):
    NR, NC = len(self.lines), len(self.lines[0])

    board = set()
    Graph = nx.Graph()
    grid = self.lines

    directions = ['^', '>', 'v', '<']

    for r in range(NR):
      for c in range(NC):
        ch = grid[r][c]

        if ch == 'S':
          start = r,c,'>'
        elif ch  == 'E':
          end = r,c,'?'

        if ch != '#':
          board.add((r,c))

    for r in range(NR):
      for c in range (NC):
        if (r,c) in board:
          for dir in directions:
            Graph.add_node((r,c,dir))
          for i, direction in enumerate(directions):
            Graph.add_edge((r,c,direction), (r,c,directions[(i+1)%4]), weight = 1000)

          if (r - 1, c) in board:
            Graph.add_edge((r, c, '^'), (r - 1, c, '^'), weight=1)

          if (r + 1, c) in board:
            Graph.add_edge((r, c, 'v'), (r + 1, c, 'v'), weight=1)

          if (r, c - 1) in board:
            Graph.add_edge((r, c, '<'), (r, c - 1, '<'), weight=1)

          if (r, c + 1) in board:
            Graph.add_edge((r, c, '>'), (r, c + 1, '>'), weight=1)

    for dir in directions:
      Graph.add_edge((end[0],end[1],dir),end,weight=0)

    dist_from_start, _ = nx.single_source_dijkstra(Graph, source = start, weight = 'weight')
    dist_from_end, _ = nx.single_source_dijkstra(Graph, source = end, weight = 'weight')

    return dist_from_start, dist_from_end, start, end, Graph

  def part1(self):
    result =self.create_graph()
    end = result[3]
    dist_from_start = result[0]

    min_cost = dist_from_start[end]

    return min_cost
  
  def part2(self):
    result = self.create_graph()
    G = result[4]
    end = result[3]
    dist_from_start = result[0]
    dist_from_end = result[1]
    min_cost = dist_from_start[end]

    locs = { (r,c) for r,c, d in G.nodes() if min_cost ==(dist_from_start[r,c,d]+dist_from_end[r,c,d])}

    return len(locs)
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser('Solution file')
  parser.add_argument('-part', required=True, type=int, help='Part (1/2)')
  parser.add_argument('-test', required=True, type=str, help='Test mode (True/False)')
  args = parser.parse_args()
  test = True if args.test in ['True','true'] else False
  solution = Solution(test=test)
  result = solution.part1() if args.part == 1 else solution.part2()
  print(f'Result for Part=={args.part} & Test=={test} : {result}')
