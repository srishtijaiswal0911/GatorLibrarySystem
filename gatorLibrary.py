# Import necessary libraries
import time
import sys
from os.path import splitext

# Represents a node in the book structure
class Book_Node:
    # Constructor to initialize a Book_Node object
    def __init__(self, bookID, bookName, authorName, availabilityStatus):
        # Attributes to store book information
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorName
        self.availabilityStatus = availabilityStatus
        self.borrowedBy = None
        self.reservationHeap = Binary_Min_Heap()

    # Method to get the reservation heap
    def get_reservationHeap(self):
        reservationHeap = []
        # Extracting reservations from the heap
        while True:
            minentry = self.reservationHeap.remove_min()
            if minentry is not None:
                patronID = minentry[1]
                reservationHeap.append(patronID)
            else:
                break
        return reservationHeap

    # Method to add a reservation for a book
    def make_a_reservation(self, patronID, priorityNum):
        # Creating a reservation tuple with priority, patronID, and timestamp
        timestamp = time.time()
        reservation = (priorityNum, patronID, timestamp)
        # Inserting the reservation into the reservation heap
        self.reservationHeap.insert(reservation)

        # Limit the number of reservations to 20
        if len(self.reservationHeap.heap) > 20:
            return "Waitlist full"

    # Method to remove a reservation
    def cancel_reservation(self):
        return self.reservationHeap.remove_min() if self.reservationHeap.heap else None

# Represents the node in the Red-Black Tree
class Red_Black_Node:
    # Constructor to initialize a Red-Black Node
    def __init__(self, val: Book_Node):
        self.val = val
        self.red = False  # Red/Black indicator
        self.parent = None
        self.left = None
        self.right = None

# Represents the Red-Black Tree structure
class Red_Black_Tree:
    def __init__(self):
        # Initialize the nil node with default attributes
        self.nil = Red_Black_Node(Book_Node(0, None, None, None))
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil  # Initialize root as nil
        self.color_flip_count = 0  # Counter for counting the color flips

    # Insert book node
    def insert(self, val):
        inserted_node = Red_Black_Node(val)
        inserted_node.red = True  # The inserted node should be red
        inserted_node.parent = None
        inserted_node.left = self.nil
        inserted_node.right = self.nil

        parent = None
        current = self.root
        # Traverse the tree to find the appropriate position for insertion
        while current != self.nil:
            parent = current
            if inserted_node.val.bookID < current.val.bookID:
                current = current.left
            elif inserted_node.val.bookID > current.val.bookID:
                current = current.right
            else:
                return  # If the value already exists, do nothing

        # Set the parent for the inserted node
        inserted_node.parent = parent
        if parent is None:
            self.root = inserted_node
        elif inserted_node.val.bookID < parent.val.bookID:
            parent.left = inserted_node
        else:
            parent.right = inserted_node
        # Balance the tree after insertion
        self.balance_after_insert(inserted_node)

    # Delete book node
    def delete(self, val):
        # Store red-black node colors in dict_a for comparison
        dict_a = {}
        list1 = []
        node = self.root
        list1.append(node)
        while list1:
            current = list1.pop(0)
            dict_a[current.val.bookID] = 1 if current.red else 0
            if current.left:
                list1.append(current.left)
            if current.right:
                list1.append(current.right)
        # Find the node to be deleted
        r = self.search(val)
        if r is None:
            return
        q = r
        q_original_color = q.red
        # Re-position nodes after deletion
        if r.left == self.nil:
            p = r.right
            self.reposition(r, r.right)
        elif r.right == self.nil:
            p = r.left
            self.reposition(r, r.left)
        else:
            q = self.get_minimum(r.right)
            q_original_color = q.red
            p = q.right
            if q.parent == r:
                p.parent = q
            else:
                self.reposition(q, q.right)
                q.right = r.right
                q.right.parent = q
            self.reposition(r, q)
            q.left = r.left
            q.left.parent = q
            q.red = r.red

        # Balance the tree after deletion based on the original color
        if q_original_color == False:
            self.balance_after_delete(p, dict_a)
        else:
            # Compare red-black node colors before and after deletion
            dict_b = {}
            list1 = []
            node = self.root
            list1.append(node)
            while list1:
                current = list1.pop(0)
                dict_b[current.val.bookID] = 1 if current.red else 0
                if current.left:
                    list1.append(current.left)
                if current.right:
                    list1.append(current.right)
            diff = {p: dict_a[p] == dict_b[p] for p in dict_a if p in dict_b}
            counter = 0
            # Count the color flips
            for ele in diff.values():
                if ele == False:
                    counter += 1
            self.color_flip_count += counter

    # Left rotation at node p
    def left_rotation(self, p):
        # Perform left rotation at a given node
        q = p.right
        p.right = q.left
        if q.left != self.nil:
            q.left.parent = p

        q.parent = p.parent
        if p.parent == None:
            self.root = q
        elif p == p.parent.left:
            p.parent.left = q
        else:
            p.parent.right = q
        q.left = p
        p.parent = q

    # Right rotation at node p
    def right_rotation(self, p):
        # Perform right rotation at a given node
        q = p.left
        p.left = q.right
        if q.right != self.nil:
            q.right.parent = p

        q.parent = p.parent
        if p.parent == None:
            self.root = q
        elif p == p.parent.right:
            p.parent.right = q
        else:
            p.parent.left = q
        q.right = p
        p.parent = q

    # Balance tree after insertion
    def balance_after_insert(self, inserted_node):
        # Balance the tree after insertion of a node
        while inserted_node != self.root and inserted_node.parent.red:
            if inserted_node.parent == inserted_node.parent.parent.right:
                u = inserted_node.parent.parent.left  # Uncle
                if u.red:
                    # Case 1: Uncle is red
                    u.red = False
                    inserted_node.parent.red = False
                    inserted_node.parent.parent.red = True
                    if u == self.root or inserted_node.parent == self.root or inserted_node.parent.parent == self.root:
                        self.color_flip_count += 2  # Counting the color flip
                    else:
                        self.color_flip_count += 3  # Counting the color flip
                    inserted_node = inserted_node.parent.parent

                else:
                    # Case 2: Uncle is black
                    if inserted_node == inserted_node.parent.left:
                        inserted_node = inserted_node.parent
                        self.right_rotation(inserted_node)
                    inserted_node.parent.red = False
                    inserted_node.parent.parent.red = True
                    if inserted_node.parent == self.root or inserted_node.parent.parent == self.root:
                        if self.root.red == True:
                            self.color_flip_count += 2
                        else:
                            self.color_flip_count += 1  # Counting the color flip
                    else:
                        self.color_flip_count += 2  # Counting the color flip
                    self.left_rotation(inserted_node.parent.parent)
            else:
                u = inserted_node.parent.parent.right  # Uncle - Sibling of parent
                if u.red:
                    # Case 3: Uncle is red
                    u.red = False
                    inserted_node.parent.red = False
                    inserted_node.parent.parent.red = True
                    if u == self.root or inserted_node.parent == self.root or inserted_node.parent.parent == self.root:
                        self.color_flip_count += 2  # Counting the color flip
                    else:
                        self.color_flip_count += 3  # Counting the color flip
                    inserted_node = inserted_node.parent.parent

                else:
                    # Case 4: Uncle is black
                    if inserted_node == inserted_node.parent.right:
                        inserted_node = inserted_node.parent
                        self.left_rotation(inserted_node)
                    inserted_node.parent.red = False
                    inserted_node.parent.parent.red = True
                    if inserted_node.parent == self.root or inserted_node.parent.parent == self.root:
                        if self.root.red == True:
                            self.color_flip_count += 2
                        else:
                            self.color_flip_count += 1  # Counting the color flip
                    else:
                        self.color_flip_count += 2  # Counting the color flip
                    self.right_rotation(inserted_node.parent.parent)

        self.root.red = False  # Set the root node to black after balancing

    # Balance tree after deletion
    def balance_after_delete(self, p, dict_a):
        # Balance the tree after deletion of a node
        while p != self.root and p.red == False:
            if p == p.parent.left:
                w = p.parent.right
                if w.red:
                    # Case 1: Sibling (w) is red
                    w.red = False
                    p.parent.red = True
                    self.left_rotation(p.parent)
                    w = p.parent.right
                if w.left.red == False and w.right.red == False:
                    # Case 2: Both children of sibling are black
                    w.red = True
                    p = p.parent
                else:
                    if w.right.red == False:
                        # Case 3: Right child of sibling is black
                        w.left.red = False
                        w.red = True
                        self.right_rotation(w)
                        w = p.parent.right
                    w.red = p.parent.red
                    p.parent.red = False
                    w.right.red = False
                    self.left_rotation(p.parent)
                    p = self.root
            else:
                w = p.parent.left
                if w.red:
                    # Case 1: Sibling (w) is red
                    w.red = False
                    p.parent.red = True
                    self.right_rotation(p.parent)
                    w = p.parent.left
                if w.right.red == False and w.left.red == False:
                    # Case 2: Both children of sibling are black
                    w.red = True
                    p = p.parent
                else:
                    if w.left.red == False:
                        # Case 3: Left child of sibling is black
                        w.right.red = False
                        w.red = True
                        self.left_rotation(w)
                        w = p.parent.left
                    w.red = p.parent.red
                    p.parent.red = False
                    w.left.red = False
                    self.right_rotation(p.parent)
                    p = self.root

        p.red = False  # Set the color of the node to black after balancing
        # Store red-black node colors after deletion in dict_b
        dict_b = {}
        list1 = []
        node = self.root
        list1.append(node)
        while list1:
            current = list1.pop(0)
            dict_b[current.val.bookID] = 1 if current.red else 0
            if current.left:
                list1.append(current.left)
            if current.right:
                list1.append(current.right)
        # Compare red-black node colors before and after deletion
        diff = {p: dict_a[p] == dict_b[p] for p in dict_a if p in dict_b}
        counter = 0
        # Count the color flips
        for ele in diff.values():
            if ele == False:
                counter += 1
        self.color_flip_count += counter

    # Find node for given book ID
    def search(self, val):
        # Search for a node with a given book ID
        val = int(val)
        current = self.root
        while current != self.nil and val != current.val.bookID:
            if val < current.val.bookID:
                current = current.left
            elif val:
                current = current.right

        if current == self.nil:
            return None
        else:
            return current

    # Reposition a node
    def reposition(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Get the minimum value node in a subtree
    def get_minimum(self, p):
        while p.left != self.nil:
            p = p.left
        return p

class Reservation_Node:
    def __init__(self, patronID, priorityNum, timeOfReservation):
        self.patronID = patronID
        self.priority = priorityNum
        self.timeOfReservation = timeOfReservation


class Binary_Min_Heap:
    def __init__(self):
        # Initialize a Binary Min Heap
        self.heap = []

    def __iter__(self):
        # Allow iteration over the heap elements
        return iter(self.heap)

    def insert(self, element):
        # Insert an element into the heap and perform upward heapification
        self.heap.append(element)
        self.upward_heapify(len(self.heap) - 1)

    def pop(self):
        # Remove and return the minimum element from the heap and perform downward heapification
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        top = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.downward_heapify()
        return top

    def return_elements(self):
        # Return all elements in the heap
        return self.heap

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def remove_min(self):
        # Remove and return the minimum element from the heap and perform heapification
        if not self.heap:
            return None
        min_element = self.heap[0]
        last_element = self.heap.pop()
        if self.heap:
            self.heap[0] = last_element
            self.downward_heapify()
        return min_element

    def upward_heapify(self, current_index):
        # # Perform upward heapification to maintain heap properties
        while current_index > 0:
            parent_index = (current_index - 1) // 2
            if self.heap[parent_index][0]> self.heap[current_index][0] or (
                    self.heap[parent_index][0] == self.heap[current_index][0] and
                    self.heap[parent_index][2] > self.heap[current_index][2]):
                self.swap(parent_index, current_index)
                current_index = parent_index
            else:
                break
    
    def downward_heapify(self):
        # Perform downward heapification to maintain heap properties
        current_index = 0
        while True:
            left_child_index = 2 * current_index + 1
            right_child_index = 2 * current_index + 2
            smallest = current_index

            if left_child_index < len(self.heap) and (
                    self.heap[left_child_index][0] < self.heap[smallest][0] or (
                    self.heap[left_child_index][0] == self.heap[smallest][0] and
                    self.heap[left_child_index][2] < self.heap[smallest][2])):
                smallest = left_child_index

            if right_child_index < len(self.heap) and (
                    self.heap[right_child_index][0] < self.heap[smallest][0] or (
                    self.heap[right_child_index][0] == self.heap[smallest][0] and
                    self.heap[right_child_index][2] < self.heap[smallest][2])):
                smallest = right_child_index

            if smallest != current_index:
                self.swap(current_index, smallest)
                current_index = smallest
            else:
                break

# Represents the library system
class Library_System:
    def __init__(self):
        # Initialize the Library System with a Red-Black Tree for books and an empty patrons dictionary
        self.book_tree = Red_Black_Tree()
        self.patrons = {}
        
    def add_book(self, bookID, bookName, authorName, availabilityStatus):
        # Add a new book to the library
        new_book = Book_Node(bookID, bookName, authorName, availabilityStatus)
        self.book_tree.insert(new_book)
        
    def search_book(self, node, bookID):
        # Search for a particular book
        while node != None and bookID != node.bookID:
            if bookID < node.bookID:
                node = node.left
            else:
                node = node.right
        return node

    def color_flip_count(self):
        # Return the count of color flips in the book tree
        return self.book_tree.color_flip_count

    def insert_book(self, bookID, bookName, authorName, availabilityStatus, borrowedBy=None,
                    reservation_heap=None):
        new_book = Book_Node(bookID, bookName, authorName, availabilityStatus)
        new_book.availabilityStatus = availabilityStatus
        new_book.borrowedBy = borrowedBy
        if reservation_heap:
            new_book.reservationHeap.heap = reservation_heap
        self.book_tree.insert(new_book)

    def return_book(self, patronID, bookID):
        # Book returned after borrowing
        node = self.book_tree.search(bookID)
        opLine = ''
        if node is not None and node.val.availabilityStatus == '"No"' and node.val.borrowedBy == patronID:
            if len(node.val.reservationHeap.heap) > 0:
                reserved_patron_id = node.val.reservationHeap.heap.pop(0)
                node.val.borrowedBy = reserved_patron_id[1]
                opLine = f"Book {bookID} Returned by Patron {patronID}\n" \
                f"Book {bookID} Allotted to Patron {node.val.borrowedBy}" 
            else:
                node.val.availabilityStatus = '"Yes"'
                node.val.borrowedBy = None
                opLine = f"Book {bookID} Returned by Patron {patronID}"
        else:
            opLine = f"Book {bookID} cannot be returned by Patron {patronID}."
        return opLine

    def delete_book(self, bookID):
        # delete book node
        node = self.book_tree.search(bookID)
        if node is not None:
            if node.val.reservationHeap.heap:
                reservationHeap = node.val.get_reservationHeap()
                self.cancel_reservations(bookID, reservationHeap)
                opLine = f"Book {bookID} is no longer available. Reservations made by Patrons {', '.join(str(reservation) for reservation in reservationHeap)} have been cancelled!"
            else:
                opLine = f"Book {bookID} is no longer available."
            self.book_tree.delete(bookID)
        else:
            opLine = f"Book {bookID} not found in the library."
        return opLine
    
    def borrow_book(self, patronID, bookID, patron_reservation_priority):
        node = self.book_tree.search(bookID)
        if node is not None:
            if node.val.availabilityStatus == '"Yes"':
                node.val.availabilityStatus = '"No"'
                node.val.borrowedBy = patronID
                self.patrons
                return f"Book {bookID} Borrowed by Patron {patronID}"

            else:
                reservation_added = node.val.make_a_reservation(patronID, patron_reservation_priority)
                if reservation_added == "Waitlist full":
                    return f"Waitlist for Book {bookID} is full. Cannot add reservation for Patron {patronID}"
                else:
                    return f"Book {bookID} Reserved by Patron {patronID}"
        else:
            return f"Book {bookID} is not available for borrowing."

    def cancel_reservations(self, bookID, patrons):
        for patronID in patrons:
            patron = self.patrons.get(patronID, None)
            if patron is not None:
                patron.cancel_reservation(bookID)
    
    def print_book(self, bookID):
        # Print details of a specific book
        node = self.book_tree.search(bookID)
        if node is not None:
            patron_ids = [patronID[1] for patronID in node.val.reservationHeap.heap]
            details = (
                f"BookID = {node.val.bookID}\n"
                f"Title = {node.val.bookName}\n"
                f"Author = {node.val.authorName}\n"
                f"Availability = {node.val.availabilityStatus}\n"
                f"BorrowedBy = {node.val.borrowedBy}\n"
                f"Reservations = {patron_ids}"
            )
            return details
        else:
            return (f"Book {bookID} not found in the library.")

    def print_books(self, node, book_id1, book_id2):
        # Print details of multiple books
        book_details = []
        def process_book(book_node):
            patron_ids = [patronID[1] for patronID in book_node.val.reservationHeap.heap]
            details = (
                f"BookID = {book_node.val.bookID}\n"
                f"Title = {book_node.val.bookName}\n"
                f"Author = {book_node.val.authorName}\n"
                f"Availability = {book_node.val.availabilityStatus}\n"
                f"BorrowedBy = {book_node.val.borrowedBy}\n"
                f"Reservations = {patron_ids}"
            )
            book_details.append(details)
        def inorder_traversal(node):
            nonlocal book_details
            if node is not None:
                inorder_traversal(node.left)
                if isinstance(node.val, Book_Node) and book_id1 <= node.val.bookID <= book_id2:
                    process_book(node)
                inorder_traversal(node.right)
        inorder_traversal(node)
        return book_details

    def get_book_details(self, node):
        patron_ids = [patronID[1] for patronID in node.val.reservationHeap.heap]
        return (
            f"BookID = {node.val.bookID}\n"
            f"Title = {node.val.bookName}\n"
            f"Author = {node.val.authorName}\n"
            f"Availability = {node.val.availabilityStatus}\n"
            f"BorrowedBy = {node.val.borrowedBy}\n"
            f"Reservations = {patron_ids}"
        )
        
    def find_closest_book(self, node, target_id):
        closest_lower, closest_higher = self.find_closest_book_helper(node, target_id)

        book_details = []

        if closest_lower is not None and closest_higher is not None:
            distance_lower = abs(target_id - closest_lower.val.bookID)
            distance_higher = abs(target_id - closest_higher.val.bookID)

            if distance_lower < distance_higher:
                details = self.get_book_details(closest_lower)
                book_details.append(details)
            elif distance_higher < distance_lower:
                details = self.get_book_details(closest_higher)
                book_details.append(details)
            else:
                if closest_lower.val.bookID == closest_higher.val.bookID:
                    details = self.get_book_details(closest_lower)
                    book_details.append(details)
                else :
                    details1 = self.get_book_details(closest_lower)
                    details2 = self.get_book_details(closest_higher)
                    book_details.append(details1)
                    book_details.append(details2)

        elif closest_lower is not None:
            details = self.get_book_details(closest_lower)
            book_details.append(details)
        elif closest_higher is not None:
            details = self.get_book_details(closest_higher)
            book_details.append(details)

        return book_details

    def find_closest_book_helper(self, node, target_id, closest_lower=None, closest_higher=None):
        while node.val.bookID != 0:
            if node.val.bookID == target_id:
                return node, node
            elif node.val.bookID < target_id:
                closest_lower = node
                node = node.right
            else:
                closest_higher = node
                node = node.left
        return closest_lower, closest_higher
    
    def quit(self):
        # Exit the library system
        exit()

def main(input_filename):
    library = Library_System()
    with open(input_filename, "r") as file:
        lines = file.readlines()
        output_lines = []

        def parse_command(command_string):
            parts = command_string.split('(')
            command = parts[0].strip()

            if len(parts) > 1:
                arguments = parts[1].rstrip(')').split(',')
                arguments = [arg.strip() for arg in arguments]
                return command, arguments
            else:
                return command, []

        for line in lines:
            list1 = []
            node = library.book_tree.root
            list1.append(node)
            while list1:
                current = list1.pop(0)
                if current.left:
                    list1.append(current.left)
                if current.right:
                    list1.append(current.right)

            line = line.strip()
            output_line = None

            if line == "Quit()":
                output_line = f"Program Terminated!!"
                output_lines.append(output_line)
                break

            else:

                command, *args = parse_command(line)
                args = args[0]

                if command == "InsertBook":
                    bookID, title, author, availabilityStatus = args[0],args[1],args[2],args[3]
                    library.insert_book(int(bookID), title, author, availabilityStatus, None, None)

                elif command == "PrintBook":
                    bookID = args[0]
                    output_line = library.print_book(bookID)

                elif command == "PrintBooks":
                    book_id1, book_id2 = args[0], args[1]
                    books = library.print_books(library.book_tree.root, int(book_id1), int(book_id2))
                    all_books = [
                        f"{book}\n" for book in books]
                    output_line = '\n'.join(all_books)

                elif command == "FindClosestBook":
                    target_id = args[0]
                    closest_books = library.find_closest_book(library.book_tree.root, int(target_id))
                    all_closest_books = [
                        f"{book}\n" for book in closest_books]
                    output_line = '\n'.join(all_closest_books)

                elif command == "BorrowBook":
                    patronID, bookID, priority = args[0], args[1], args[2]
                    output_line = library.borrow_book(int(patronID), int(bookID), int(priority))

                elif command == "ReturnBook":
                    patronID, bookID = args
                    output_line = library.return_book(int(patronID), int(bookID))

                elif command == "DeleteBook":
                    bookID = args[0]
                    output_line = library.delete_book(int(bookID))

                elif command == "ColorFlipCount":
                    output_line = f"Colour Flip Count: {library.book_tree.color_flip_count}"

            if output_line is not None:
                output_lines.append(output_line)
                output_lines.append("\n")

    try:
        output_filename = splitext(input_filename)[0] + "_output_file.txt"
        with open(output_filename, 'w') as output_file:
            for line in output_lines:
                output_file.write(str(line) + '\n')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 gatorLibrary.py input_filename")
        sys.exit(1)

    input_filename = sys.argv[1]
    main(input_filename)
