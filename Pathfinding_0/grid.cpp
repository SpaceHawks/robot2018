#include "grid.h"

Grid::Grid()
{
    for(int i=0;i<101;i++){
        for(int j=0;j<7;j++){
            grid[i][j] = 0.0;
        }
    }
    index = 0;
}

void Grid::incrementIndex()
{
    index++;
}

int Grid::getIndex()
{
    return index;
}

void Grid::insert(double item,  int i, int j)
{
    if(i < 101 && j < 7)
        grid[i][j] = item;
    else
        qDebug() << "Failed!";
}

double Grid::get(int i, int j)
{
    if(i < 101 && j < 7)
        return grid[i][j];
    else
        return 0.0;
}

void Grid::clear()
{
    for(int i=0;i<101;i++){
        for(int j=0;j<7;j++){
            grid[i][j] = 0.0;
        }
    }
    index = 0;
}

void Grid::display()
{
    double d0 = 0.0;
    double d1 = 0.0;
    double d2 = 0.0;
    double d3 = 0.0;
    double d4 = 0.0;
    double d5 = 0.0;
    double d6 = 0.0;
    for(int i=0;i<index;i++){
        d0 = grid[i][0];
        d1 = grid[i][1];
        d2 = grid[i][2];
        d3 = grid[i][3];
        d4 = grid[i][4];
        d5 = grid[i][5];
        d6 = grid[i][6];
        qDebug() << d0 << d1 << d2 << d3 << d4 << d5 << d6;
    }
}
