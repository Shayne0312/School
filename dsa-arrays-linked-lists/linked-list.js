class Node {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
}

class LinkedList {
  constructor(vals = []) {
    this.head = null;
    this.tail = null;
    this.length = 0;
    for (let val of vals) this.push(val);
  }

  /** push(val): add new value to end of list. */
  push(val) {
    const newNode = new Node(val);
    if (this.head === null) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      this.tail.next = newNode;
      this.tail = newNode;
    }
    this.length++;
  }

  /** unshift(val): add new value to start of list. */
  unshift(val) {
    const newNode = new Node(val);
    newNode.next = this.head;
    this.head = newNode;
    if (this.tail === null) {
      this.tail = newNode;
    }
    this.length++;
  }

  /** pop(): return & remove tail value. Throws error if list is empty. */
  pop() {
    if (this.length === 0) {
      throw new Error("Cannot pop from an empty list");
    }
  
    const val = this.tail.val;
  
    if (this.length === 1) {
      this.head = null;
      this.tail = null;
    } else {
      let currentNode = this.head;
      while (currentNode.next !== this.tail) {
        currentNode = currentNode.next;
      }
      currentNode.next = null;
      this.tail = currentNode;
    }
  
    this.length--;
    return val;
  }

  /** shift(): return & remove head value. Throws error if list is empty. */
  shift() {
    if (this.length === 0) {
      throw new Error("Cannot shift from an empty list");
    }
    const val = this.head.val;
    this.head = this.head.next;
    this.length--;
    if (this.length === 0) {
      this.tail = null;
    }
    return val;
  }

  /** getAt(idx): get val at idx. */
  getAt(idx) {
    if (idx < 0 || idx >= this.length) {
      throw new Error("Index out of bounds");
    }
    let node = this.head;
    for (let i = 0; i < idx; i++) {
      node = node.next;
    }
    return node.val;
  }

  /** setAt(idx, val): set val at idx to val */
  setAt(idx, val) {
    if (idx < 0 || idx >= this.length) {
      throw new Error("Index out of bounds");
    }
    let node = this.head;
    for (let i = 0; i < idx; i++) {
      node = node.next;
    }
    node.val = val;
  }

  /** insertAt(idx, val): add node w/val before idx. */
  insertAt(idx, val) {
    if (idx > this.length || idx < 0) {
      throw new Error("Invalid index.");
    }

    if (idx === 0) return this.unshift(val);
    if (idx === this.length) return this.push(val);
    let prev = this.head;
    for (let i = 0; i < idx - 1; i++) {
      prev = prev.next;
    }
    let newNode = new Node(val);
    newNode.next = prev.next;
    prev.next = newNode;

    this.length += 1;
  }

  /** removeAt(idx): return & remove item at idx, */
  removeAt(idx) {
    if (idx < 0 || idx >= this.length) {
      throw new Error("Index out of bounds");
    }
    if (idx === 0) {
      return this.pop();
    } else {
      const prevNode = this.getAt(idx - 1);
      const nodeToRemove = prevNode.next;
      prevNode.next = nodeToRemove.next;
      this.length--;
      return nodeToRemove.val;
    }
  }

  /** average(): return an average of all values in the list */
  average() {
    if (this.length === 0) {
      return 0;
    }
    let sum = 0;
    let node = this.head;
    while (node !== null) {
      sum += node.val;
      node = node.next;
    }
    return sum / this.length;
  }
}