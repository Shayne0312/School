function sortedFrequency(arr, num) {
    let firstIndex = findFirstIndex(arr, num);
    if (firstIndex == -1) {
      return 0;
    }
    let lastIndex = findLastIndex(arr, num);
    return lastIndex - firstIndex + 1;
  }
  
  function findFirstIndex(arr, num) {
    let left = 0;
    let right = arr.length - 1;
    let firstIndex = -1;
    while (left <= right) {
      let mid = Math.floor((left + right) / 2);
      if (arr[mid] >= num) {
        right = mid - 1;
      } else {
        left = mid + 1;
      }
      if (arr[mid] == num) {
        firstIndex = mid;
      }
    }
    return firstIndex;
  }
  
  function findLastIndex(arr, num) {
    let left = 0;
    let right = arr.length - 1;
    let lastIndex = -1;
    while (left <= right) {
      let mid = Math.floor((left + right) / 2);
      if (arr[mid] <= num) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
      if (arr[mid] == num) {
        lastIndex = mid;
      }
    }
    return lastIndex;
  }

module.exports = sortedFrequency