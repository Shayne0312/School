function starOutGrid(grid) {
    // Identify the rows/columns and add the constructor.
    const rowsToStar = new Set();
    const colsToStar = new Set();
  
    // Find the rows and columns that need to be starred out
    for (let row = 0; row < grid.length; row++) {
      for (let col = 0; col < grid[row].length; col++) {
        if (grid[row][col] === '*') {
          rowsToStar.add(row);
          colsToStar.add(col);
        }
      }
    }
  
    // Star out the rows (width/leftright-rightleft)
    for (let row of rowsToStar) {
      for (let col = 0; col < grid[row].length; col++) {
        grid[row][col] = '*';
      }
    }
  
    // Star out the columns (height/updown-downup)
    for (let col of colsToStar) {
      for (let row = 0; row < grid.length; row++) {
        grid[row][col] = '*';
      }
    }
  
    return grid;
  }