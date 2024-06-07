# Name: Sean Yang
# OSU Email: yangsea@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 2024-06-06
# Description: This code implements a HashMap class with separate
#               chaining. This implementation contains methods that like
#               put, resize table, table load, empty buckets, get, contains
#               key, remove, get keys and values, clear, and find mode.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Update the key/value pair in the hash map. If key already exists,
        the associated value is replaced with new value. If not, both key
        and value is added.
        """
        # Check load factor.
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # Update value or add key and value.
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)
        node = bucket.contains(key)
        if node is not None:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of table if new capacity is 1 or more and a
        prime number. If not a prime number, change to next highest prime
        number.
        """
        # Check if new capacity is valid and change if needed.
        capacity = new_capacity
        if capacity < 1:
            return
        if not self._is_prime(capacity):
            capacity = self._next_prime(capacity)

        # Change table capacity.
        tempBuckets = self._buckets
        self._buckets = DynamicArray()
        for i in range(capacity):
            self._buckets.append(LinkedList())

        # Reassign values.
        self._size = 0
        oldCapacity = self._capacity
        self._capacity = capacity
        for i in range(oldCapacity):
            bucket = tempBuckets.get_at_index(i)
            for node in bucket:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Return the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets.
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Return the value associated with the given key. Return None if key
        is not in hash map.
        """
        index = self._hash_function(key) % self._capacity
        length = self._buckets.get_at_index(index).length()
        # If there are no keys.
        if length == 0:
            return None
        # Go through the keys at index.
        for node in self._buckets.get_at_index(index):
            if node.key == key:
                return node.value
        # If none is found.
        return None

    def contains_key(self, key: str) -> bool:
        """
        Return True if key is in hash map and False otherwise.
        """
        if self.get(key) is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Remove key and value from hash map. If not found, do nothing.
        """
        # Find index for key and remove.
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(index)
        for node in bucket:
            if node.key == key:
                bucket.remove(node.key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array with tuples of key/value pairs stored in the
        hash map.
        """
        da = DynamicArray()
        # Loop through to find buckets that are not empty.
        for i in range(self._capacity):
            bucket = self._buckets.get_at_index(i)
            if bucket.length() > 0:
                for node in bucket:
                    da.append((node.key, node.value))
        return da

    def clear(self) -> None:
        """
        Clear the contents of hash map.
        """
        for i in range(self._capacity):
            self._buckets.set_at_index(i, LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receive a dynamic array and return a tuple containing a dynamic array
    of the mode and the frequency.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mode = DynamicArray()
    freq = 1

    # Make copy of given dynamic array so that the original isn't changed.
    temp = DynamicArray()
    for i in range(da.length()):
        temp.append(da.get_at_index(i))

    # Set up map
    for i in range(temp.length()):
        val = temp.get_at_index(i)
        if map.contains_key(val):
            map.put(val, map.get(val) + 1)
            temp.set_at_index(i, None)
        else:
            map.put(val, 1)

    # Go through array and hash map and count frequency.
    for i in range(temp.length()):
        val = temp.get_at_index(i)
        if val is not None:
            count = map.get(val)
            if count > freq:
                freq = map.get(val)
                mode = DynamicArray()
                mode.append(val)
            elif count == freq:
                mode.append(val)

    return mode, freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
