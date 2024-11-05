/**
 * Assignment 5: Task 1 - Knowledge Circulation
 * author: Seasun Legaspi
 */
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

struct Island {
    string name;
    int population;
    int time_to_conduct_training;
    unordered_map<Island*, int> neighbors; // Neighbors with travel times
};

struct PathInfo {
    int current_time;
    Island* island;
    int total_population;
    vector<Island*> path; // Track islands visited

    bool operator<(const PathInfo& other) const {
        return total_population < other.total_population;
    }
};

int dijkstraKnowledgeCirculation(Island* start_island, int max_time) {
    // Max heap to store (total time, current island, total population reached, path taken)
    priority_queue<PathInfo> queue;
    queue.push({0, start_island, start_island->population, {start_island}});
    int max_population = 0;
    vector<Island*> max_path;
    unordered_set<Island*> visited;

    while (!queue.empty()) {
        auto [current_time, current_island, total_population, path] = queue.top();
        queue.pop();

        // Skip path if exceed max time
        if (current_time > max_time) continue;
        // Update maximum population reached and save the path if this path is better
        if (total_population > max_population) {
            max_population = total_population;
            max_path = path;
        }
        // Explore neighboring islands
        for (const auto& [neighbor, travel_time] : current_island->neighbors) {
            int new_time = current_time + travel_time + neighbor->time_to_conduct_training;
            int new_population = total_population + neighbor->population;

            // Only explore if unvisited
            if (visited.find(neighbor) == visited.end()) {
                // Create a new path with the neighbor added
                vector<Island*> new_path = path;
                new_path.push_back(neighbor);

                queue.push({new_time, neighbor, new_population, new_path});
                visited.insert(current_island); // Mark current island as visited
            }
        }
    }
    // Output the maximum population reached and the path taken
    cout << "Maximum population reached: " << max_population << endl;
    cout << "Islands visited: ";
    for (auto* island : max_path) {
        cout << island->name << " ";
    }
    cout << endl;

    return max_population;
}

int main() {
    //Island
    Island islandA {"Island A", 500, 2};
    Island islandB {"Island B", 1000, 3};
    Island islandC {"Island C", 200, 1};
    Island islandD {"Island D", 800, 2};

    // Neighbors and travel times
    islandA.neighbors = {{&islandB, 2}, {&islandC, 4}};
    islandB.neighbors = {{&islandA, 2}, {&islandC, 1}, {&islandD, 7}};
    islandC.neighbors = {{&islandA, 4}, {&islandB, 1}, {&islandD, 3}};
    islandD.neighbors = {{&islandB, 7}, {&islandC, 3}};

    int max_time = 10;
    dijkstraKnowledgeCirculation(&islandA, max_time);

    return 0;
}



