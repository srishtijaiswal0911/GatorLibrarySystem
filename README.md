# Library Management System
This is a library management system that allows efficient cataloging and managing of a library's book collection and providing services to patrons.

## Features

1. Catalog books - Add, delete, search books using a Red-Black Tree
2. Borrow and Return - Patrons can borrow available books and return when done
3. Waitlist Reservations - Waitlisting allowed through priority min heaps when books unavailable
4. Print Book Details - Print information on single or range of book IDs
5. Find Closest Books - Locate closest book IDs to a given ID
6. Track Color Flips - Analytics on Red-Black Tree rotations

## Data Structures

### Red-Black Tree
- Used to catalog books uniquely identified by ID
- Enables logN time complexity for search, insert, delete
- Balanced tree structure through rotations and color flips

### Binary Min Heap
- Implements priority-based reservation waitlist
- Minimum priority reservation placed at root for easy access
- Allows logN inserts and removes

## Classes
The main classes are:

- `BookNode` - Represents a node in book catalog
- `RedBlackNode` - Node in Red-Black Tree
- `RedBlackTree` - Red-Black Tree implementation
- `ReservationNode` - Node in reservation min heap
- `BinaryMinHeap` - Priority reservation heap
- `LibrarySystem` - Main class managing operations

## Getting Started

### Prerequisites
- Python 3

### Run Program
`python gatorLibrary.py inputfile.txt`

It takes input commands from input text file and writes output to a text file.

## Documentation
The detailed documentation for classes and methods is available in the project report.