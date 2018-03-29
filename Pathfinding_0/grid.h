#ifndef GRID_H
#define GRID_H

#include <QDebug>

class Grid
{
public:
    Grid();

private:
    double grid[1000][7];
    int index;

public:
    void incrementIndex();
    int getIndex();
    void insert(double item, int i, int j);
    double get(int i, int j);
    void clear();
    void display();

};

#endif // GRID_H
