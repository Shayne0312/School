function findRotationCount(arr) {
    let left = 0;
    let right = arr.length - 1;
  
    while (left <= right) {
      if (arr[left] <= arr[right]) {
        return left;
      }
  
      let mid = Math.floor((left + right) / 2);
      let next = (mid + 1) % arr.length;
      let prev = (mid + arr.length - 1) % arr.length;
  
      if (arr[mid] <= arr[next] && arr[mid] <= arr[prev]) {
        return mid;
      } else if (arr[mid] <= arr[right]) {
        right = mid - 1;
      } else if (arr[mid] >= arr[left]) {
        left = mid + 1;
      }
    }
  
    return -1;
  }

module.exports = findRotationCount