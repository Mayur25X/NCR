#include <bits/stdc++.h>
using namespace std;
long long count_color[2];
void dfs(vector<int> graph[], int node, int parent, int color)
{
    ++count_color[color];
    for (int i = 0; i < graph[node].size(); ++i)
    {
        if (graph[node][i] != parent)
        {
            dfs(graph, graph[node][i], node, !color);
        }
    }
}
int getMaxEdges(vector<int> graph[], int n)
{
    dfs(graph, 1, 0, 0);
    return count_color[0] * count_color[1] - (n - 1);
}
int main()
{
    int n = 5;
    vector<int> graph[n + 1];
    graph[1].push_back(2);
    graph[1].push_back(3);
    graph[2].push_back(4);
    graph[3].push_back(5);
    cout << "Maximum edges = " << getMaxEdges(graph, n) << endl;
    return 0;
}
